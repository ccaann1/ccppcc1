import os
import streamlit as st
from openai import OpenAI
import requests


st.markdown(
    """
    <style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
    }
    .main .block-container { padding: 0rem; }

    .main .block-container { padding-top: 0rem; }

    .navbar {
        overflow: hidden;
        margin-bottom:20px;
        border-bottom:2px solid #48c6e0;
    }
    .navbar a {
        float: left;
        display: block;
        color: #48c6e0;
        text-align: center;
        padding: 10px 10px;
        text-decoration: none;
    }
    .navbar a:hover {
        color: black;
        border-bottom:1px solid #48c6e0;        
    }
    .navbar .logo {
        float: left;        
    }
    .navbar .menu {
        float: right;
    }
    .navbar .menu a {
        display: inline-block;
    }
    @media screen and (max-width: 600px) {
        .navbar a {
            float: none;
            display: block;
            text-align: left;
        }
        .navbar .menu {
            float: none;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <style>
    header {display: none;}
    #MainMenu {display: none;}
    footer {display: none !important;}
    footer, .stFooter {display: none !important;}
    div._container_gzau3_1 {display:none !important;}
    div._profileContainer_gzau3_53 {display:none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <script>
    const footer = document.querySelector('footer');
    if (footer) {
        footer.style.display = 'none';
    }
    </script>
    """,
    unsafe_allow_html=True
)

response = requests.get('https://canceproit.pythonanywhere.com/ttthais')
data = response.json()
take_this = data[0]

st.markdown(
    """
    <div class="navbar">
        <div class="logo">
            <img src="https://www.cancepro.com/img/icon/CancePro_Icon.png" alt="Logo" style="height: 60px;">
        </div>
        <div class="menu">
            <a href="https://www.cancepro.com/">Go Home</a>
            <a href="#">Ask Me </a>
            <a href="https://canceproxr.streamlit.app/">X-Ray Analysis</a>
            <a href="https://canceproresearch.streamlit.app/">Cancer Research</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



# Show title and description.

st.write(
    "We have collected information from renowned Cancer research institutes research documents that are publicly available. Ask a question in the below box, get relevant information."
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

# Function to read content from a text file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Read the content from your text file (update the path as needed)
file_content = read_file('hari.txt')

# Display the content from the text file as an initial message if it hasn't been added yet
if file_content and not any(msg['role'] == 'assistant' and msg['content'] == file_content for msg in st.session_state.messages):
    st.session_state.messages.append({"role": "assistant", "content": file_content})

# Display the existing chat messages via `st.chat_message`.
if len(st.session_state.messages) > 1:
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            # st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
st.markdown(
    """
    <style>
        div.stTextInput > div > div > input {
            margin-bottom:0px !important;
            background-color: transparent; /* This removes the background color */
        }
    </style>
    """,
    unsafe_allow_html=True
)

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

# st.markdown(
#     """
#     <style>
#         .footer-note{
#             float:middle;
#             text-align:center;
#             display: block;
#             color: #48c6e0;
#             position:relative;
#             bottom:-150px;
#             text-decoration: none;
#         }
#         .footer-note a:hover {
#             color: black;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown(
#     """
#     <div>
#         <!-- Footer Area -->
#             <div class="footer-note">
#                 <p> © Copyright 2024,2025  |  All Rights Reserved by <a href="https://www.cancepro.com/">cancepro.com</a> </p>			
#             </div>
#         <!--/ End Footer Area -->
#     </div>
#     """,
#     unsafe_allow_html=True
# )
