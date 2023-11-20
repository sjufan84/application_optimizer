""" Endpoint for all chat interactions """
import os
import sys
from typing import List
import logging
from fastapi import APIRouter, UploadFile, File
from dotenv import load_dotenv  
from openai import OpenAI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))

from app.models.runs import CreateThreadRunRequest, CreateMessageRunRequest  # noqa: E402
from app.utils.assistant_utils import upload_files  # noqa: E402
from app.utils.run_utils import poll_run_status  # noqa: E402
#from app.services.chat_service import get_chat_response  # noqa: E402 

router = APIRouter()

# Load the environment variables
load_dotenv()

# Get the OpenAI API key and organization ID from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_KEY2")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG2")

# Set up the client
client = OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID, max_retries=3, timeout=10)

# Define the primary endpoint.  Start with the create thread and run endpoint
@router.post("/create_thread_run",
            summary="Create a thread and run", 
            description='This endpoint creates a new thread and runs it using\
            the provided assistant_id and thread. The run status is then polled\
            and the response is returned.  The response is a JSON object formatted as\
            {"message" : "The message response from the run", "tool_return_values" :\
            "A JSON object containing the tools used and their return values"}')
async def create_thread_run(create_run_request: CreateThreadRunRequest, thread_id: str=None):
  """ Create a thread and run """
  run = client.beta.threads.create_and_run(
  assistant_id=create_run_request.assistant_id,
  thread={
    "messages": [
        {
          "role" : "user",
          "content" : create_run_request.message_content, 
    }]}   
  )
  # Poll the run status
  response = poll_run_status(run_id=run.id, thread_id=run.thread_id)

  return response
  
# Define the endpoint to add a message to the thread and run
@router.post("/add_message_and_run", 
            summary="Add a message to a thread and run", 
            description='This endpoint adds a message to an existing\
            thread and runs it. The message is created with the provided\
            thread_id, role, content, and file_ids. The run status\
            is then polled and the response is returned. The response\
            is a JSON object formatted as\
            {"message" : "The message response from the run", "tool_return_values" :\
            "A JSON object containing the tools used and their return values"}')
async def add_message_and_run(message_request: CreateMessageRunRequest):
    """ Add a message to the thread and run """
    
    # Create and send the message
    message = client.beta.threads.messages.create(
        message_request.thread_id,
        content=message_request.message_content,
        role="user",
    )
    # Log the message
    logging.info(f"Message created: {message}")

    # Create the run
    run = client.beta.threads.runs.create(
        assistant_id=message_request.assistant_id,
        thread_id=message_request.thread_id
    )
    # Poll the run status
    response = poll_run_status(run_id=run.id, thread_id=run.thread_id)

    return response

# Define an endpoint allow the user to upload an image file and return extracted text
@router.post("/extract_text_from_image", 
            summary="Extract text from an image", 
            description='This endpoint extracts text from an image.\
            The image is uploaded and the text is extracted using\
            Google Cloud Vision. The extracted text is returned.')
async def extract_text_from_image(files: List[UploadFile] = File(None)):
    """ Extract text from an image """
    # If there are uploaded files, pass them to the upload_files function
    #if files:
    #    file_contents = [await file.read() for file in files]
    # Extract the text from the image
    #extracted_text = await extract_image_text(file_contents)
    # Format the extracted text
    #formatted_text = format_recipe(extracted_text)

    #return formatted_text

# Create upload_files endpoint
@router.post("/upload_files", 
            summary="Upload files", 
            description='This endpoint uploads files to the cloud.\
            The files are uploaded and the file IDs are returned.')
async def upload_assistant_files(files: List[UploadFile] = File(None)):
  """ Upload files to OpenAI and return the file IDs """
  file_contents = [await file.read() for file in files]
  file_ids = await upload_files(file_contents)
  return file_ids
