""" Chat services utilities """
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))
from app.utils.run_utils import poll_run_status  # noqa: E402 

# Load environment variables
load_dotenv()

# Set OpenAI API key from Streamlit secrets
OPENAI_API_KEY = os.getenv("OPENAI_KEY2")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG2")

# Set up the client
client = OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID, max_retries=3, timeout=10)

# Set the initial prompt
INITIAL_PROMPT = [{"role": "system", "content" : """
        You are a PR Prophet, answering questions about public relations
        and marketing as if you were a an ancient prophet foretelling of the
        dangers of integrating too much AI to fast into the PR world.  You are working
        with another LLM that utilizes different tools to help the user, so while
        they are waiting on the return values from the other model, you are going to
        provide the user with different "did you knows" about the PR industry.  This
        could include history, different approaches by different countries and culture,
        notable figures, etc.  Keep your answers short and succint, engaging the
        user while the other model is working."""}]

openai_models = ["gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k"]

def get_chat_response(thread_id: str, run_id: str):
    """ Get chat response """
    messages = [
        {
            "role": "system",
            "content": f'{INITIAL_PROMPT}'
        }
    ]
    # While the run status is not complete, keep polling the run status
    poll_response = poll_run_status(run_id, thread_id)
    while poll_response["final_status"] != "complete":
      # Iterate through the models
      for model in openai_models:
        try:
            response = client.chat.completions.create(
              model=model,
              messages= [{"role": m["role"], "content": m["content"]} for m in messages],
              temperature=1,
              max_tokens=300,
            )
            response = response.choices[0].message.content
            yield response
            # Poll the run status
            poll_response = poll_run_status(run_id, thread_id)
            # If the run status is complete, break out of the loop
            if poll_response["final_status"] == "complete":
              break
        
        except TimeoutError as e:
              print(f"OpenAI API error: {e}")
              continue
  