""" PR Prophet -- The one and only 
by: @ChickenMon84 """

import os
import asyncio
from dotenv import load_dotenv
import streamlit as st
import openai
from PIL import Image

# Load environment variables
load_dotenv()

# Set OpenAI API key from Streamlit secrets
openai.api_key = os.getenv("OPENAI_KEY2")
openai.organization = os.getenv("OPENAI_ORG2")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-0613"

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
            FULL_RESPONSE = ""

        for response in openai.ChatCompletion.create(
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
