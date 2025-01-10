import os
import streamlit as st
from openai import OpenAI
import requests

st.markdown(
    """
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    div._container_gzau3_1 {visibility:hidden;}
    div._profileContainer_gzau3_53 {visibility:hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

response = requests.get('https://canceproit.pythonanywhere.com/ttthais')
data = response.json()
take_this = data[0]

# Show title and description.
st.title("CancePro")
st.write(
    "Our information relies on well known Cancer research institutes research documents that are publicly available. Ask a question in the below box, get relevant information."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# openai_api_key = st.text_input("OpenAI API Key", type="password")
# Setting the API key

# st.write(
#     "Has environment variables been set:",
#     os.environ["OPENAI_API_KEY"] == st.secrets["abcd_keyyy"]
# )
# st.write(st.secrets["abcd_keyyy"])
os.environ["OPENAI_API_KEY"] = take_this
api_key = take_this


# Create an OpenAI client.
client = OpenAI()

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
