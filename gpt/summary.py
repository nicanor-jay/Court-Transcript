"""Script to summarise court transcripts using GPT-API."""
from openai import OpenAI
from dotenv import load_dotenv
import json
import time


load_dotenv()
openai = OpenAI()

def get_extract_headings_prompt() -> str:
    """Return the extract headings system prompt."""
    return """You are a UK legal data extraction assistant.
    You will be given a python-style list of headers from a court transcript.
    Return a list of headers from the input, where the content of the headers will help deduce the following:
    Summary: [a concise description of what the hearing was about, maximum 1000 characters]
    Ruling: [which party the court ruled in favour of (one word answer e.g. Defendant)]
    Anomalies: [whether anything irregular happened in the context of a normal court hearing]
    Give the list in the following format: "'heading1','heading2','heading3'"
    """


def get_summarise_prompt() -> str:
    """Return the summarise system prompt."""
    return """ You are a UK legal data extraction assistant.
    You will be given a python-style dictionary where headings will be mapped to their corresponding content for a single transcript.
    Redact all personal information about the parties involved.
    Your task is to carefully extract and return the following fields:
    Summary: [a concise description of what the hearing was about, maximum 1000 characters]
    Ruling: [which party the court ruled in favour of (one word answer e.g. Defendant)]
    Anomalies: [whether anything irregular happened in the context of a normal court hearing]
    If any field is missing, write "Not Found".
    Return your output strictly in this JSON format:
    {
    "summary": "...",
    "ruling": "...",
    "anomaly": "..."
    }
    """


def create_query_messages(system_prompt: str, user_prompt: str) -> list[dict]:
    """Create messages to make a request to GPT-API."""
    if not (isinstance(system_prompt, str) and isinstance(user_prompt, str)):
        raise TypeError("Both system and user prompts must be of type string.")
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]


def get_query_results(query_messages: list[dict]) -> str:
    """Get the results from the query request made to GPT-API"""
    response = openai.chat.completions.create(
        model = "gpt-4.1-nano",
        messages = query_messages
    )
    return response.choices[0].message.content


## Batch processing functions

def create_batch_request(query_messages: list[dict], citation: str) -> dict:
    """Create a GPT-API request for batch processing."""
    return {"custom_id": citation, "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4.1-nano", "messages": query_messages}}


def insert_request(request: str, filename: str) -> None:
    """Insert a request into the .jsonl file for batch processing."""
    with open(filename, 'a') as file:
        json_request = json.dumps(request)
        file.write(json_request + "\n")


def upload_batch_file(filename: str):
    """Upload files for Batch API."""
    batch_input_file = openai.files.create(
        file=open(filename, "rb"),
        purpose="batch"
    )
    return batch_input_file


def run_batch_requests(batch_input_file):
    """Run requests in input file via batch processing."""
    batch = openai.batches.create(
        input_file_id=batch_input_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
    )
    return batch


# timeout parameter default value will be amended once tested on larger batch sizes.
def wait_for_batch(batch_id: str, poll_interval: int = 20, timeout: int = 300):
    """Poll batch until processing has finished."""
    waited = 0
    while waited < timeout:
        batch = openai.batches.retrieve(batch_id)

        status = batch.status
        print(f"[Batch {batch_id}] Status: {status} (waited {waited}s)")

        if status == "completed":
            return batch
        elif status in ["failed", "cancelled", "expired"]:
            raise RuntimeError(f"Batch {batch_id} ended with status: {status}")
        
        time.sleep(poll_interval)
        waited += poll_interval
    
    raise TimeoutError(f"Batch {batch_id} did not complete within {timeout}s")


def get_batch_meaningful_headers(batch_id: str) -> dict:
    """Return a dictionary mapping the unique case citation to a list of meaningful headers retrieved from the GPT-API request."""
    batch = wait_for_batch(batch_id)

    response = openai.files.content(batch.output_file_id)
    headers_dict = {}
    for line in response.text.splitlines():
        response_obj = json.loads(line)

        custom_id = response_obj.get("custom_id")
        headers_list = response_obj.get("response", {}).get("body", {}).get(
            "choices", [])[0].get("message", {}).get("content")
        
        headers_dict[custom_id] = headers_list

    return headers_dict


def get_batch_summaries(batch_id: str) -> dict:
    """Return the transcript summary responses from the GPT-API request."""
    batch = wait_for_batch(batch_id)

    if not batch.output_file_id:
        raise ValueError("Batch not finished processing yet or no output file detected.")
    response = openai.files.content(batch.output_file_id)
    summary_dict = {}
    for line in response.text.splitlines():
        response_obj = json.loads(line)

        custom_id = response_obj.get("custom_id")
        summary = response_obj.get("response", {}).get("body", {}).get(
            "choices", [])[0].get("message", {}).get("content")
        
        # Ensure summary is a dict (parse it to be JSON-like if text)
        if isinstance(summary, str):
            try:
                summary = json.loads(summary)
            except json.JSONDecodeError:
                summary = {"summary": summary}

        summary_dict[custom_id] = {
            "summary": summary.get("summary"),
            "ruling": summary.get("ruling"),
            "anomaly": summary.get("anomaly")
        }
    
    return summary_dict

def extract_meaningful_headers(transcripts: list[dict], filename: str, citation: str) -> dict:
    """Return necessary headers needed to summarise each court transcript.
    transcripts: list of dictionaries where each dictionary represents the headings mapped to
    their text for a single transcript
    
    """

    # Setup .jsonl file with individual requests
    for transcript in transcripts:
        query_message = create_query_messages(
            get_extract_headings_prompt(), transcript)
        request = create_batch_request(query_message, citation)
        insert_request(request, filename)

    # Upload batch file to openai and run the batch process.
    batch_input_file = upload_batch_file(filename)
    batch = run_batch_requests(batch_input_file)

    return get_batch_meaningful_headers(batch.id)


def summarise(transcripts: list[dict], filename: str, citation: str):
    """Return summarised data for each court transcript.
    transcript_text: a list of dictionaries where each dictionary represents the meaningful headings mapped to
    their text for a single transcript
    """

    # Setup .jsonl file with individual requests
    for transcript in transcripts:
        query_message = create_query_messages(
            get_summarise_prompt(), transcript)
        request = create_batch_request(query_message, citation)
        insert_request(request, filename)

    # Upload batch file to openai and run the batch process.
    batch_input_file = upload_batch_file(filename)
    batch = run_batch_requests(batch_input_file)

    return get_batch_summaries(batch.id)