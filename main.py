""" PR Prophet -- The one and only 
by: @ChickenMon84 """
import os
import asyncio
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from PIL import Image

# Load environment variables
load_dotenv()

# Create the OpenAI client
api_key = os.getenv("OPENAI_KEY2")
organization = os.getenv("OPENAI_ORG2")

client = OpenAI(api_key=api_key, organization=organization, timeout=10, max_retries=3)


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"

if "messages" not in st.session_state:
    st.session_state.messages = []

def main():
    """ Main function for Application Optimizer """
    st.markdown("""
                <h3 style='text-align: center; color: #f6bd60;'>PR Prophet.
                Welcome to the application optimizer</h3>
                """, unsafe_allow_html=True)
    st.text("")
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        elif message["role"] == "user":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Let's get started!"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Load the prophet image for the avatar
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages= [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
            temperature=1,
            max_tokens=100
            ):
            FULL_RESPONSE += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(FULL_RESPONSE + "▌")
        message_placeholder.markdown(FULL_RESPONSE)
        st.session_state.messages.append({"role": "assistant", "content": FULL_RESPONSE})
if __name__ == "__main__":
    asyncio.run(stream_pr())
