""" PR Prophet -- The one and only 
by: @ChickenMon84 """
import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from utils.chat_utils import create_thread_run, add_message_and_run
from utils.assistant_utils import upload_files, create_assistant_files
# Load environment variables
load_dotenv()

# Create the OpenAI client
api_key = os.getenv("OPENAI_KEY2")
organization = os.getenv("OPENAI_ORG2")

client = OpenAI(api_key=api_key, organization=organization, timeout=10, max_retries=3)


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

def process_uploaded_files(uploaded_files):
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with st.form(key=uploaded_file.name):
                st.write(f"Metadata for {uploaded_file.name}")
                file_category = st.selectbox("File category:", ["Resume", "Job Description"], key=f"category_{uploaded_file.name}")
                file_description = st.text_area("Short description (optional):", key=f"desc_{uploaded_file.name}")
                submit_metadata = st.form_submit_button("Submit Metadata")
                file_contents = [file.read() for file in uploaded_files]

                if submit_metadata:
                    handle_file_upload(file_contents, file_category, file_description)

def handle_file_upload(file_contents, category, description):
    file_content = [content for content in file_contents]
    response = upload_files(files=file_content)
    file_ids = response
    
    if "file_metadata" not in st.session_state:
        st.session_state.file_metadata = {}
    st.session_state.file_metadata[response[0]] = {"category": category, "description": description}
    
    create_assistant_file(file_ids)

def create_assistant_file(file_ids):
  for file_id in file_ids:
    assistant_file = client.beta.assistants.files.create(assistant_id=st.session_state.assistant_id, file_id=file_id)
    st.session_state.assistant_files.append(assistant_file)

def process_pasted_text(text):
    if text:
        # Here you can add logic to process or store the pasted text
        if "pasted_texts" not in st.session_state:
            st.session_state.pasted_texts = []
        st.session_state.pasted_texts.append(text)
        # Convert the text to bytes
        text_bytes = text.encode("utf-8")
        # Upload the file contents and the metadata to the assistant
        file_ids = upload_files([text_bytes])
        # Assistant files creation
        assistant_files = create_assistant_files(file_ids=file_ids)
        # Append the assistant files to the session state
        st.session_state.assistant_files = st.session_state.assistant_files + assistant_files

        return file_ids 

def process_user_input(input_text):
    if input_text:
        st.session_state.messages.append({"role": "user", "content": input_text})
        response = create_thread_or_add_message(input_text)
        st.session_state.messages.append({"role": "assistant", "content": response["message"]})

def create_thread_or_add_message(input_text):
    thread_id = st.session_state.get("thread_id")
    file_ids = st.session_state.get("file_ids")

    if thread_id is None:
        response = create_thread_run(message_content=input_text, file_ids=file_ids)
        st.session_state.thread_id = response["thread_id"]
    else:
        response = add_message_and_run(message_content=input_text, thread_id=thread_id, file_ids=file_ids)

    return response

def main():
    """ Main function for Application Optimizer """
    st.title("Application Optimizer")

    # Initialize session state variables if they don't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "file_ids" not in st.session_state:  
        st.session_state.file_ids = []
    if "assistant_files" not in st.session_state:
        st.session_state.assistant_files = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None
    if "assistant_id" not in st.session_state:
        st.session_state.assistant_id = "asst_FNbc0H90UCKiCu7DR41Ot3Mp"

    # Sidebar for file uploads and text input
    with st.sidebar:
        st.header("Upload Files and Text")
        uploaded_files = st.file_uploader("Upload your files here:", accept_multiple_files=True)
        process_uploaded_files(uploaded_files)

        pasted_text = st.text_area("Or paste text here:", height=200)
        if st.button("Submit Text"):
            process_pasted_text(pasted_text)
        
    # Chat input
    user_input = st.text_input("Type your message here...")
    if st.button("Send"):
        process_user_input(user_input)
        display_chat_interface()

def display_example_prompts():
    """ Display example prompts to guide the user """
    st.markdown("##### To get started, begin your chat below. You can simply start a chat with a question or at any time upload any relevant files that you want to be considered in the optimization process.")
    # List some example prompts
    st.markdown("###### Example prompts:")
    st.markdown("**1. What are the top 3 things I should do to optimize my application?**")
    st.markdown("**2. What keywords from the job description should I include in my application?**")
    st.markdown("**3. What areas can I help the applicant improve in their application?**")
    st.markdown("**4. From 1 to 10, how would you rate the applicant's fit for the job?**")

def display_chat_interface():
    # Clear existing chat display
    st.empty()

    # Display example prompts only if there are no messages
    if not st.session_state.messages:
        display_example_prompts()

    # Display chat messages
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        elif message["role"] == "user":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        


if __name__ == "__main__":
    main()
    