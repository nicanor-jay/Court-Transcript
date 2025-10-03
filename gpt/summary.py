"""Script to summarise court transcripts using GPT-API."""
from openai import OpenAI
from dotenv import load_dotenv
import json
import time


load_dotenv()
openai = OpenAI()

def get_extract_headings_prompt() -> str:
    return """You are a UK legal data extraction assistant.
    You will be given a list of headers from a court transcript.
    You must return a list of headers that you believe will contain the necessary information in the transcript to deduce the following:
    Summary: [a concise description of what the hearing was about, maximum 1000 characters]
    Ruling: [which party the court ruled in favour of (one word answer e.g. Defendant)]
    Anomalies: [whether anything irregular happened in the context of a normal court hearing]
    Give the list in the following format: "'heading1','heading2','heading3'"
    """


def get_summarise_prompt() -> str:
    return """ You are a UK legal data extraction assistant.
    I will provide you with the raw text or HTML content of a webpage containing information about a court hearing.
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


# Currently hard-coded, will depend on web-scraping output
# Would take the web-scraped output as an input

def get_user_prompt() -> str:
    """Generate a user prompt to give as input to GPT-API"""
    user_prompt = """Decision: The appeal is dismissed.

REASONS

Background

Paragraph1.
This is an appeal against the Respondent’s decision to refuse the Appellant’s application for registration at Level 1 under Schedule 6 of the Immigration and Asylum Act 1999 (“the Act”) in the categories of ‘immigration’ and ‘asylum and protection’.

Paragraph2.
The Office of the Immigration Services Commissioner (now known as the Immigration Advice Authority (“IAA)”) regulates immigration advisers, ensuring that immigration advice is only provided by those who are determined to be fit and competent to provide such advice.

Paragraph3.
On 15th April 2024, the Appellant, who was a qualified solicitor and held a current practising certificate at the time, applied to the Respondent for registration as an immigration adviser at Level 1, which is the entry level for providing basic immigration advice.

Paragraph4.
On 24th April 2024, the Appellant requested an exemption from the Level 1 Competency Assessment. That request was refused by the Respondent on 25th April 2024, and the Appellant was notified of the date for his Level 1 Competency Assessment on 15th May 2024.

Paragraph5.
The Competency Assessment has two parts to it, with Section One comprising of multiple-choice questions, and Section Two comprising of scenario-based questions. The answers to Section One are not subjective in nature and are marked as either a pass (correct answer) or fail (for an incorrect answer) The minimum mark required to pass each section is 60%. Both sections of the Competency Assessment must be passed in order to pass the overall assessment.

Paragraph6.
On 29th May 2024, the Appellant sat the Level 1 Immigration Assessment and scored marks of 55% (11 out of 20) for Section One, and 93% (28 out of 30) for Section Two. Despite scoring over the 60% pass mark for Section Two, he failed to achieve the 60% pass mark required for Section One. The Immigration Services Commissioner therefore wrote to him on 20th June 2024, informing him that he had failed to demonstrate sufficient competence in achieving the 60% pass mark in both sections of the assessment, and that consequently his application for registration had been refused.

Paragraph7.
On 5th July 2024, the Appellant submitted his Notice of Appeal to this Tribunal by email, together with other documents, including a copy of his practising certificate for the year 2023/2024 from the Solicitors Regulation Authority, a degree certificate from the University of Buckingham dated 2007, confirmation that he had passed his Solicitors Qualifying Exam (Assessment 1 and 2) in 2023, and a Turkish document which was not translated.

Notice of Appeal

Paragraph8.
In his Notice of Appeal, the Appellant explained that he is a dual-qualified lawyer with over 17 years legal experience, having completed his law degree at the University of Buckingham in 2007, and having spent several years working in law firms from 2007 to 2011. Thereafter, he qualified as an Attorney-at-law in Turkey and became registered with the Istanbul Bar Association in 2011, and subsequently practised law through his own law firm, Canko Law Firm, between 2012 and 2023. Having qualified as a solicitor in England & Wales in 2023, he has been employed by his law firm, Canko Consultancy Limited, trading as Canko Law Firm, in Newcastle.

Paragraph9.
In his notice of Appeal, the Appellant submits the following:

(i)
That his close failure on Section One of the assessment should not form the sole basis for refusing his application for registration at Level 1.

(ii)
That his score of 93% in Section Two of the assessment should have been taken into account.

Paragraph10.
The outcome the Appellant seeks is for the refusal to be overturned and his application for registration at Level 1 to be accepted by the Respondent.

The Law

Paragraph11.
The Immigration and Asylum Act 1999 provides a scheme for the regulation of immigration advisors. The Office of the Immigration Services Commissioner (now known as the Immigration Advice Authority) is established by section 83 of the Act and the Commissioner has a general duty to promote good practice by those who provide immigration advice of immigration services. The Commissioner additionally has certain regulatory functions as set out in Schedule 5 of the Act.

Paragraph12.
Section 83(5) of the Immigration and Asylum Act 1999 provides as follows:

“The Commissioner must exercise his functions so as to secure, so far as is reasonably practicable, that those who provide immigration advice or immigration services –

(a)
Are fit and competent to do so;

(b)
Act in the best interests of their clients;

…”

Paragraph13.
Section 84(1) of the Act provides that “No person may provide immigration advice or immigration services unless he is a qualified person.”. A qualified person is defined by section 84(2) to include:

“(a)
a Registered person,

(b)
authorised by a designated professional body to practise as a member of the profession whose members the body regulates,

(ba) a person authorised to provide immigration advice or immigration services by a designated qualifying regulator,

(c)
…

(d)
…

(e)
[a person] acting on behalf of, and under the supervision of, a person within any of paragraphs (a) to (ba) (whether or not under a contract of employment).”

Paragraph14.
The reference to a registered person in section 84(2) is a reference to a person who is registered with the Commissioner under section 85 of the Act. A person’s entitlement to provide immigration advice or immigration services by virtue of section 84(2)(ba) “is subject to any limitation on that person’s authorisation imposed by the regulatory arrangements of the designated qualifying regulator in question…” section 84(3A)). By section 86A of the Act, a “designated qualifying regulator” includes:

(a)
The Law Society;

(b)
The Institute of Legal Executives;

(c)
The General Council of the Bar.

Paragraph16.
By section 85 of the Act, the Commissioner must prepare and maintain a register of those persons registered by him/her to provide immigration advice and immigration services. The system of registration is established under Schedule 6 of the Act. If the Commissioner considers that an applicant for registration is “competent and otherwise fit to provide immigration advice and immigration services, he/she must register the applicant.”. Equally, the Commissioner must cancel a persons’ registration if he or she “is no longer competent or otherwise unfit to provide immigration advice or immigration services.”. The Act does not provide any further assistance with a definition of what is meant by “competent or otherwise [un]fit”.

Paragraph17.
An appeal process is provided for under section 87 of the Act, so that “any person aggrieved by a relevant decision of the Commissioner may appeal to the First-tier Tribunal against the decision.” (section 87(2)).

Paragraph18.
The refusal of an application for registration made under paragraph 1 of Schedule 6 of the Act is a ‘relevant decision’ for the purposes of an appeal.

Paragraph19.
The appeal is a full appeal and not simply a review of the exercise by the Commissioner of his/her decision-making power. In an appeal, the Tribunal must determine for itself whether the Commissioner’s decision was right and, in the circumstances of the case, determine whether the applicant is, as of the date of the Tribunal hearing, fit and competent to provide immigration advice and services to the specified level. In doing so, the Tribunal will consider all relevant admissible evidence, whether or not it was known to or taken into account by the Commissioner when making his/her decision (Visa Joy Ltd v Immigration Services Commissioner [2017] EWCA Civ 1473). The burden is on the Appellant, with the standard of proof being on the balance of probabilities.

Preliminary issue: Rule 14 Order

Paragraph20.
Following the refusal of the Appellant’s application for registration at Level 1, he made a Freedom of Information Request under the Freedom of Information Act 2000, requesting the following:

“Respondent is requested to submit the Level 1 Immigration Assessment that I completed on May 29th 2024, along with my responses to both sections (MCQ and written questions).”

Paragraph21.
The Respondent subsequently provided the following response:

“We do not provide a copy of the marked papers. This is stated in the OISC General marking scheme for OISC assessments: “Specific feedback is not offered to candidates nor does the OISC provide copies of answer scripts or question papers following assessments:

Additionally, this information is exempt pursuant to paragraph 25(1) of Schedule 2 to the Data protection Act 2018.

Furthermore, it is important to note that the OISC will not disclose the exam marking scheme, questions or any candidate’s assessment paper. This is to protect the integrity of the Respondent’s competence assessment process.”

Paragraph22.
Considering the Appellant’s information request and the fact that his grounds of appeal relate to his competence assessment, the Respondent made an application for an Order under Rule 14 of The Tribunal Procedure (First-tier Tribunal) (General Regulatory Chamber) Rules 2009 to enable the Tribunal have sight of the documents, but on the basis that the information is not disclosed to the Appellant or any other person.

Paragraph23.
A Rule 14 Order was made by the Tribunal on 19th June 2025, stipulating that the material would be held in a Closed Bundle pursuant to rule 14(6). Whilst this is not an appeal against a Decision Notice of the Information Commissioner, and the appeal is strictly related to the Appellant’s appeal against the refusal of his application for registration, we consider that providing the information to the Appellant would compromise the integrity of the competence assessment process and would consequently cause the Respondent serious harm. In view of this, we consider that the Rule 14 Order is both necessary and proportionate in the circumstances of this case, and it will remain in force until further Order.

Paragraph24.
The Tribunal is not aware of an appeal or application being submitted by the Appellant in respect of any complaint to, or Decision Notice of, the Information Commissioner. Should he remain dissatisfied with the information he requested being withheld, the proper course would be to make a complaint to the Information Commissioner. For the purposes of this appeal hearing, however, the Tribunal has confined its decision to the question of whether the decision to refuse registration was wrong, and whether the Appellant is fit and competent to provide immigration advice and services at Level 1.

Evidence

Paragraph25.
The parties were agreeable to the determination of this appeal on the papers, that is to say, without an oral hearing. We are satisfied, pursuant to Rule 32(1)(b) of the Tribunal Procedure (First-tier Tribunal) (General Regulatory Chamber) Rules 2009, that we can properly determine the issues without a hearing.

Paragraph26.
For the purposes of determining this appeal, we have considered the following documents:

(a)
Refusal of Application for Regulation by Immigration Services Commissioner, dated 20th June 2024.

(b)
Notice of Appeal, dated 5th July 2024, and accompanying documents (13 pages).

(c)
Respondent’s application to strike out under Rule 8(3)(c) and accompanying bundle of 9th August 2024 (91 pages).

(d)
Respondent’s Response of 9th August 2024 to the Notice of Appeal and accompanying bundle (12 pages).

(e)
Appellant’s Reply to the Respondent’s application to strike out, dated 13th August 2024, and accompanying documents (30 pages).

(f)
Appellant’s ‘List of Legal Issues’, dated 13th August 2024 (3 pages).

(g)
Appellant’s further Response to Application to Strike Out, dated 30th September 2024, and accompanying bundle (37 Pages).

(h)
Witness statement of Stefanie Jones, dated 5th February 2025.

(i)
CLOSED bundle containing Appellant’s marked Competency Assessment and application for Rule 14 Order, dated 30th April 2024 (37 pages).

Submissions advanced by the Appellant

Paragraph26.
In essence, the Appellant submits that as a qualified and experienced lawyer, who held a practising certificate from the Solicitors Regulation Authority (SRA) at the time of his application, that his competence should have been assessed by reference to that experience, and not by way of a competence assessment, which he submits is designed to assess those without formal legal qualifications and experience. A summary of his submissions is as follows:

(a)
That in the case of LLB-qualified solicitors, the Respondent is required to establish a separate assessment pathway, which should include a clear exemption process that does not necessitate a written assessment.

(b)
That the Level 1 application does not impose any specific entry requirements, and consequently those without legal qualifications or experience may and should have to apply and be assessed by way of a written competence assessment.

(c)
That subjecting experienced practitioners to additional written examination imposes an unreasonable burden on the practitioner and undermines the rigorous legal education and professional training that these individuals have already successfully completed.

(d)
That he was granted exemptions by the SRA from both the SQE2 exam and the two-year post qualification experience requirement to become a solicitor in England and Wales, and it is unreasonable for the OISC to refuse to consider granting an exemption.

(e)
That under section 84(1) of the Immigration and Asylum Act 1999, a solicitor is recognised as a ‘qualified’ individual authorised to provide immigration services, but the OISC guidelines require that solicitors work under the supervision of either an SRA-regulated law firm or an OISC-regulated firm. It is inconsistent and illogical that he is deemed competent to work within an OISC-regulated firm without a competence assessment, but he is required to complete one in order to become OISC regulated himself.

(f)
That his application to the Respondent for an exemption, dated 24th April 2024, was rejected the very next day on 25th April 2024 without proper justification, thereby demonstrating that it had not been properly considered.

(g)
That rejecting his application on the basis of competence when he is a dual-qualified lawyer with his level of experience is inconceivable.

(h)
That he was only given 13 days’ notice of the date for his competence assessment, and he should have been permitted more time for preparation.

(i)
That his professional qualifications and experience demonstrate that his competence is far in excess of the requirements for a Level 1 immigration advisor.

(j)
That although he failed Section One of the competence assessment by one mark, he achieved a 93% score in the scenario-based section, demonstrating his ability to apply legal principles to real-world situations, which is a core requirement for any legal profession.

(k)
That disregarding his qualifications and experience on the basis that this comes from an overseas jurisdiction would be unjust and discriminatory practice.

Submissions advanced on behalf of the Respondent

Paragraph27.
A summary of the Respondent’s submissions is as follows:

(a)
The Level 1 competence assessment paper has two sections to it. The minimum mark required to pass on each section is 60%. The Appellant failed Section One of the assessment and therefore did not satisfy the Respondent of his competency to the required standard.

(b)
That whilst Level 1, Section Two assessment papers are subject to moderation if the total marks awarded are up to 5% below the pass mark and up to 3% over the pass mark, Section One comprises of multiple-choice questions only and the answers are marked as either a pass or fail. The answers are not subjective and there is therefore no scope for moderation.

(c)
The decision to refuse the Appellant’s application was taken following his failure to pass the Level competence assessment of 29th May 2024 in accordance with section 83(5)(a) of the Act, on the basis that he did not satisfy the Respondent that he was fit and competent to provide immigration advice or immigration services.

Witness Statement of Stephanie Jones

Paragraph28.
In her statement of 5th February 2025, Stephanie Jones states that following the Appellant’s application for registration at Level 1 being submitted, and his application being reviewed, the decision was taken to submit him for the Level 1 assessment. She refers to his submitted competence statement as showing previous experience as a solicitor in the areas of employment and family law, but it failed to demonstrate that he had any experience in UK immigration law.

Paragraph29.
Before his assessment, the Appellant emailed to request an exemption from taking it, based upon his experience. However, he was informed that he did not meet the criteria nor did he hold the IAAS qualification that would exempt him from the assessment. Additionally, he did not include details of any UK immigration training that had been undertaken within the last 12 months.

Paragraph30.
Whilst the Appellant subsequently provided evidence of training with the Free Movement on the topic of ‘Introduction to Immigration, Asylum, Nationality and more’, having completed that course in May 2024, this does not provide him with an exemption from the Level 1 competence assessment.

Paragraph31.
In addition to detailing the Appellant’s scores in the Level 1 competence assessment and referring to the IAA Competence Assessment Process Guidance (2023), which stipulates that “If an applicant is unable to pass both sections of their Level 1 Assessment, then their application for regulation will be refused.”, she explains that that the assessment paper is designed to cover immigration theory within the IAA’s guidance on competence at Level 1, and the multiple-choice questions are written based upon the syllabus provided on the IAA website and the IAA resource book. She states that the Appellant would have been aware of this.

Paragraph32.
She refers to the IAA guidance on borderline papers, which states as follows:

“All borderline papers will be referred for higher moderation before a final result is agreed. If after moderation, candidates are still deemed to have fallen short of the minimum expectations for written communication then they are likely to fail overall.

Level 1, Section 2 assessment papers are subject to moderation if the total marks awarded are up to 5% below the pass mark and up to 3% over the pass mark.”

Paragraph33.
However, she points out that as Section 1 of the assessment comprises of multiple-choice questions only, the answers are determined by HJT Training Limited to be either a pass or fail, as the answers are not subjective in nature and there is no scope for moderation of that section of the assessment.

Paragraph34.
The online platform used to permit applicants to take the assessment remotely is named Janison and it marks the multiple-choice questions in an automated fashion. There have not been any issues with the automated process. However, despite it not being standard practice to review Level 1, Section 1 marks, the lead assessor was asked to review the Appellant’s marks. This was carried out to rule out any error with the automated marking of the paper. The lead assessor has confirmed that there was no issue with the marking of section 1 of the paper and that the marks awarded to the Appellant (55%) were correct.

Paragraph35.
Each assessment paper is written by a qualified immigration practitioner at HJT, which is then independently reviewed by the assessment review team within the IAA to ensure that it meets the Level 1 guidance on competence and syllabus. The review team will then relay any feedback back to HJT as required.

Discussion and Decision

Paragraph36.
The role of the Immigration Services Commissioner was created by Parliament when section 83 of the Immigration and Asylum Act 1999 came into force on 30th October 2000, and it is the general duty of the Commissioner to promote good practice by those who provide immigration advice or immigration services.

Paragraph37.
Section 84(2) of the Act permits a person to provide immigration advice and/or services without being regulated by the IAA if they are authorised to practise by a Designated Qualifying Regulator (DQR) (section 84(2)(b) of the Act). This of course includes the Solicitors Regulation Authority, as the SRA derives its regulatory authority from the Law Society, a DQR. The SRA maintains restrictions upon solicitors practising in certain fields, including immigration advice and services. The Appellant is of course a solicitor and is therefore bound by the standards and regulations which the SRA imposes upon him. In this instance, as the Appellant recognises in his Reply under Rule 24, he is not permitted to provide immigration advice and/or services without successfully passing the competence assessment, unless he is providing those services from an SRA-regulated law firm or an OISC (now IAA) regulated firm. Whilst he points to the guidance provided by the IAA as conflicting with the requirements of section 84(1) of the Act, it is the SRA which imposes this restriction upon him, as his Designated Qualifying Regulator, and not the IAA. The IAA Guidance merely replicates these restrictions.

Paragraph38.
Despite the Appellant’s assertion that the Respondent is required to establish a separate assessment pathway for those who have qualified as solicitors, we have been shown no Rule or law which supports this proposition, and it appears that this is merely a bold assertion or a suggestion. The Tribunal certainly has no power to require the Commissioner to establish such a scheme.

Paragraph39.
Although the SRA granted the Appellant exemptions from taking the SQE2 exam and the requirement to gain two years’ post-qualification experience when providing him with his practising certificate in 2023, this does negate the restrictions which the SRA imposes upon those seeking to provide immigration advice and/or services. He was therefore required to make an application for registration to the IAA, which he clearly recognised by having made the application for registration in 2024. The fact that the Appellant is disgruntled by having failed Section One of the competence assessment and does not now consider that he should be required to take a written assessment, is of no assistance to him. Indeed, the Commissioner is tasked by Parliament with ensuring that those who provide immigration advice or immigrations services are fit and competent to do so, and upon an application being made, in the absence of any suitable experience or demonstrated competence in the field, whether the applicant is a qualified lawyer or not, the Commissioner is entitled to require that person to take a competence assessment. In this instance, the Appellant provided no evidence to the Commissioner of any relevant, recent experience of immigration or asylum training in England and Wales. The evidence he did provide was in relation to his experience of domestic employment and family law. Had he completed one of the Law Society’s Immigration and Asylum Accreditation Scheme (IAAS) examinations, then he may have been granted an exemption from taking a competence assessment, as detailed within the 2023 OISC (IAA) Guidance Notes for Applications for Registration. We do not consider that requiring an applicant to have suitable experience within the jurisdiction they wish to practice in as being in any way discriminatory.

Paragraph40.
It is important to recognise that Parliament created the role of the Immigration Services Commissioner, as it felt that this area of law required better regulation and standards to be enforced. The Commissioner is tasked by Parliament with ensuring that professional standards and good practice are maintained, and the competence assessments provide the Commissioner with a way of testing an applicant’s competence before they are placed on the register. The Appellant in this instance failed to meet the minimum standard of 60% in Section One of his competence assessment, and as is detailed within the OISC Guidance, an applicant is required to pass both sections of in order to pass the assessment, and if they don’t their application will be refused. All candidates are subject to the same requirements and marking criteria, and there is no subjective element to Section One. This is so regardless of any candidate’s performance in Section Two.

Paragraph41.
We are satisfied that the statement of Stephanie Jones correctly sets out how the automated process marks Section One answers as either pass or fail, and that in addition to that system, which has not been shown to have any issues, the Appellant’s answers were checked by the lead assessor, who confirmed that the 55% mark scored was correct.

Paragraph42.
Having taken account of all the evidence produced in support of the Appellant’s case that he is competent to provide immigration advice and services to the required standard, including his examination results, his practising certificate from the SRA, his experience as a lawyer, and other documentation he provided, we conclude that the Appellant has not demonstrated his competence to provide immigration advice and services to the required standard for registration at Level 1. We do not find that the Appellant has demonstrated that the IAA’s decision to refuse registration was wrong. For the reasons set above, we dismiss the appeal.

Signed: Date:

Judge Armstrong-Holmes 17th September 2025"""
    return user_prompt


# create/import function to retrieve headings/sub-headings from transcript

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

# Function will be removed once unique hearing identifier is given from metadata

def get_last_request_id(filename: str) -> int:
    """Get the id of the last request in the .jsonl file."""
    with open(filename, 'r') as file:
        last_request = ""
        for line in file:
            last_request = line
        if last_request:
            request_obj = json.loads(last_request)
            custom_id = request_obj.get("custom_id", 0)
            id_number = int(custom_id.split("-")[1])
            return id_number
    return 0


def create_batch_request(query_messages: list[dict], filename: str) -> dict:
    """Create a GPT-API request for batch processing."""
    return {"custom_id": f"request-{get_last_request_id(filename) + 1}", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4.1-nano", "messages": query_messages}}

# Change custom id to be unique to the specific court hearing (case id/reference number ideally)

def insert_request(request: str, filename: str) -> None:
    """Insert a request into the .jsonl file for batch processing"""
    with open(filename, 'a') as file:
        json_request = json.dumps(request)
        file.write(json_request + "\n")


def upload_batch_file(filename: str):
    """Upload files for Batch API"""
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


def wait_for_batch(batch_id: str, poll_interval: int = 20, timeout: int = 300):
    """Poll batch until processing has finished"""
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
    """Return the meaningful headers responses from the GPT-API request."""
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

def extract_meaningful_headers(headers: list, filename: str):
    """Return necessary headers needed to summarise each court transcript."""

    # Setup .jsonl file with individual requests
    for header_list in headers:
        query_message = create_query_messages(
            get_extract_headings_prompt(), header_list)
        request = create_batch_request(query_message, filename)
        insert_request(request, filename)

    # Upload batch file to openai and run the batch process.
    batch_input_file = upload_batch_file(filename)
    batch = run_batch_requests(batch_input_file)

    return get_batch_meaningful_headers(batch.id)


def summarise(transcript_text: list[dict], filename: str):
    """Return necessary headers needed to summarise each court transcript."""

    # Setup .jsonl file with individual requests
    for text in transcript_text: # for loop logic is currently a placeholder, will be fixed once I have the finalised webscraped output
        query_message = create_query_messages(
            get_summarise_prompt(), text)
        request = create_batch_request(query_message, filename)
        insert_request(request, filename)

    # Upload batch file to openai and run the batch process.
    batch_input_file = upload_batch_file(filename)
    batch = run_batch_requests(batch_input_file)

    return get_batch_summaries(batch.id)


if __name__ == "__main__":
    load_dotenv()

    # For a given list of transcript headers:
        # create an extract header query message
        # create a batch request with that query message
        # insert batch request into jsonl file

    # repeat above for each transcript
    # run batch process
    # give output back to Arshin

    # For each each block of transcript text:
        # Create a summarise query message
        # create a batch request with that query message
        # insert batch request into jsonl file

    # repeat above for each transcript
    # run batch process
    # list of summarised transcripts

    batch_input_file = upload_batch_file("requests.jsonl")

    batch = run_batch_requests(batch_input_file)
    
    summaries = get_batch_summaries(batch.id)

    print(summaries)


    # check how many batch requests there are

    # print(openai.batches.list(limit=1))


