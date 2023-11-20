""" Helper functions to generate the correct assistant instructions """
# Initial imports
import sys
from typing import List
import os
from openai import OpenAI
from fastapi import UploadFile
from dotenv import load_dotenv
# Add the path of the package to the system path
sys.path.append('C:/Users/sjufa/OneDrive/Desktop/Current Projects/pr_prophet/backend')

# Load environment variables
load_dotenv()

# Set OpenAI API key
api_key = os.getenv("OPENAI_KEY2")
organization = os.getenv("OPENAI_ORG2")

# Set up the client
client = OpenAI(api_key=api_key, organization=organization, max_retries=3, timeout=10)

# Define a function to receive and upload files to the assistant
async def upload_files(files: List[UploadFile]):
    """ Takes in the list of file objects and uploads them to the assistant """
    file_ids_list = []
    for file in files:
        # Upload the file
        response = client.files.create(file=file, purpose="assistants")
        # Append the file url to the list
        file_id = response.id
        file_ids_list.append(file_id)

    return file_ids_list
