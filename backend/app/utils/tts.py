import os
from openai import OpenAI
from dotenv import load_dotenv  

# Load the environment variables
load_dotenv()

# Load the API key from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_KEY2")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG2")

# Initialize the client with your API key
client = OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID)

audio_file_path = "resources/temp_audio.mp3"

def transcribe(audio_file_path):
    # Create an audio file for transcription

    # Open the audio file
    with open(audio_file_path, "rb") as audio_file:
        # Transcribe the audio to text
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcript['text']

def get_assistant_response(user_text):
    # Process the text with your assistant logic here
    # For example, let's just echo the user text
    assistant_response = f"Received your message: {user_text}"
    return assistant_response

def text_to_speech(text, voice="alloy"):
    # Convert the text to speech and save as an audio file
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    return response    
