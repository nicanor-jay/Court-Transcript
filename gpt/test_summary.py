# pylint: skip-file

""""Tests for summary.py GPT-API querying"""

import pytest
import json
import io
from unittest.mock import mock_open, patch, MagicMock

from summary import create_query_messages, create_batch_request, insert_request, upload_batch_file, run_batch_requests

def test_create_query_messages_valid_prompt_type():
    """Check that a query message has string prompts stored in the content keys"""
    test_query_message = create_query_messages(
        "Act as a maths teacher and add the given numbers", "1, 2, 3")
    assert isinstance(test_query_message[0]["content"], str)
    assert isinstance(test_query_message[1]["content"], str)


def test_create_query_messages_invalid_prompt_type():
    """Check that a query message does not have a non-string value stored in the content keys"""
    with pytest.raises(TypeError):
        create_query_messages("Act as a maths teacher and add the given numbers",
                              124)


def test_create_query_messages_invalid_prompt_type_2():
    """Check that a query message does not have a non-string value stored in the content keys"""
    with pytest.raises(TypeError):
        create_query_messages(["Act", "as", "a", "maths", "teacher"],
                              124)


def test_create_batch_request_valid_request():
    """Check whether the function correctly creates a valid batch request"""
    query_messages = [{"role": "user", "content": "Hello"}]
    with patch("summary.get_last_request_id", return_value=3): # return value for custom id will be amended once I have unique hearing identifier
        result = create_batch_request(query_messages, "testfile")
    assert "custom_id" in result
    assert result["body"]["messages"] == query_messages
    assert result["body"]["model"] == "gpt-4.1-nano"


def test_insert_request():
    """Check whether a batch request is successfully inserted into a jsonl file"""
    mock_data = {"test": "data"}
    mock = mock_open()
    with patch("builtins.open", mock):
        insert_request(mock_data, "fake_file.jsonl")
    # Check if the file was opened once in append mode
    mock.assert_called_once_with("fake_file.jsonl", "a")
    handle = mock()
    # Check if request was written once to the jsonl file
    handle.write.assert_called_once_with(json.dumps(mock_data) + "\n")


def test_upload_batch_file():
    """Check if the jsonl batch file successfully uploads to GPT-API"""
    fake_response = MagicMock()
    fake_response.id = "file-12345"
    fake_response.filename = "test.jsonl"
    mock_files_create = patch("summary.openai.files.create", return_value=fake_response)
    
    with patch("builtins.open", mock_open(read_data=b"fake data")):

        result = upload_batch_file("test.jsonl")

    mock_files_create.assert_called_once()

    assert result.id == "file-12345"
    assert result.filename == "test.jsonl"


def test_run_batch_request():
    """Check whether a batch request successfully runs"""
    fake_batch = {"id": "batch-12345", "status": "queued"}
    mock_openai_batches_create = patch("openai.batches.create", return_value=fake_batch)
    result = run_batch_requests({"id": "file-12345"})
    assert result == fake_batch
    mock_openai_batches_create.assert_called_once()


def test_wait_for_batch():
    """Check whether a successful batch is correctly polled"""
    pass