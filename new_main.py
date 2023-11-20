""" PR Prophet -- The one and only 
by: @ChickenMon84 """

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from PIL import Image
from utils.tts import text_to_speech

# Load environment variables
load_dotenv()

# Set OpenAI API key from Streamlit secrets
api_key = os.getenv("OPENAI_KEY2")
organization = os.getenv("OPENAI_ORG2")

client = OpenAI(api_key=api_key, organization=organization)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

new_prompt = [{"role": "system", "content" : """
        You are a PR Prophet, answering questions about public relations
        and marketing as if you were a prophet in the Bible.  It's meant
        to be a light a playful way for pr and marketing professionals to
        get advice about their craft.  Keep your answers brief almost like
        a two paragraph daily devotional."""}]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = new_prompt

prophet = Image.open("./resources/Prophet.jpeg")

async def stream_pr():
    """ Main function for PR Prophet """
    st.markdown("""
                <h3 style='text-align: center; color: #f6bd60;'>PR Prophet.
                Ask and ye shall receive. 🔮</h3>
                """, unsafe_allow_html=True)
    st.text("")
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar=prophet):
                st.markdown(message["content"])
        elif message["role"] == "user":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What questions doest thou have?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Load the prophet image for the avatar
        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar=prophet):
            message_placeholder = st.empty()
            #FULL_RESPONSE = ""

        # Generate the full response from the chat model
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages= [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=1,
            max_tokens=250
        )
        prophet_response = response.choices[0].message.content
        
        message_placeholder.markdown(prophet_response)
        st.session_state.messages.append({"role": "assistant", "content": prophet_response})
        
        # Now that we have the full response, we can send it to the TTS service
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = text_to_speech(
            text=prophet_response
        )
        response.stream_to_file(speech_file_path)

        # Provide a way for Streamlit to play the audio file
        audio_file = open(speech_file_path, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")


if __name__ == "__main__":
    asyncio.run(stream_pr())
