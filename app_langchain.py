import streamlit as st
import random
import time
import os
import base64
import requests
import time
from langchain.prompts import PromptTemplate
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

llm_api_host = os.environ["LLM_API_HOST"]

os.environ["OPENAI_API_KEY"] = "sk-"
os.environ["OPENAI_API_BASE"] = f"http://{llm_api_host}/v1"
os.environ["OPENAI_API_HOST"] = f"http://{llm_api_host}"

def get_metadata():
    resp = requests.get(f"http://{llm_api_host}/v1/models")
    if resp.status_code == 200:
        return resp.json()["data"][0]["metadata"]
    return None

metadata = get_metadata()
html_content = f"""
    <div style="display: flex; align-items: center;">
        <img src="https://avatars.githubusercontent.com/u/9976052?s=50&v=4">
        <h2 style="margin: 0 0 0 10px;">Weave AI Chat ({metadata["model_name"]})</h2>
    </div>
"""
st.markdown(html_content, unsafe_allow_html=True)

with open('typing.css') as f:
    css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
tying_dots = """
<div id="typing-container" class="typing">
    <div class="typing__dot"></div>
    <div class="typing__dot"></div>
    <div class="typing__dot"></div>
</div>
"""    

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Message here ..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # message_placeholder = st.markdown(
        #    f'<img src="data:image/gif;base64,{data_url}" width="32" height="32" style="vertical-align: super;" alt="gif">',
        #    unsafe_allow_html=True,
        # )
        message_placeholder = st.markdown(tying_dots, unsafe_allow_html=True)
        full_response = ""

        chat = ChatOpenAI(temperature = 0.1, max_tokens=512)
        messages = [
            SystemMessage(
                content=f"You are an opensource LLM model {metadata['model_name']} deployed and managed by Weave AI, a tool developed by Weaveworks."
            ),
            HumanMessage(
                content=user_input
            ),
        ]
        start_time = time.time()
        result = chat(messages)
        assistant_response = result.content    
        end_time = time.time()
        duration = end_time - start_time
        formatted_duration = f"{int(duration)}s.{int((duration % 1) * 1000)}ms"        
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(f"{full_response}<small style='color: grey;'> ({formatted_duration})</small>", unsafe_allow_html=True)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})