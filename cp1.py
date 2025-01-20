#Chat

import warnings
warnings.filterwarnings('ignore')
                                        
import os
import streamlit as st
from openai import OpenAI
import requests
# from langdetect import detect



import io
from audio_recorder_streamlit import audio_recorder
import speech_recognition as speech

showErrorDetails = False


listener = speech.Recognizer()



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
    
    header {display: none !important;}
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    footer, .stFooter {display: none !important;}
    div._container_gzau3_1 {display:none !important;}
    div._profileContainer_gzau3_53 {display:none !important;}
    </style>
    """,
    unsafe_allow_html=True
)



hide_streamlit_styles = """
    <style>
    footer {display:none !important;color:#ffffff !important;height:1px !important; font-size:1pt !important;}
    footer: hover{display:none !important;}
    div._profilePreview_gzau3_63{display:none !important;color:#ffffff !important;height:1px !important; font-size:1pt !important;}
    
    </style>
"""
st.markdown(hide_streamlit_styles, unsafe_allow_html=True)



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

# Show title and description.

st.write(
    "Hi, I am Isha!!!"
)

st.write("A Conversational ChatBot built by CancePro. As a part of our Research we have collected information from renowned Cancer research institutes research documents. Ask a question in the below box, get relevant information and be Healthy by taking precautions.")



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
file_content = read_file('Cancer_Information.txt')

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
            # margin-bottom:0px !important;
            color:#ffffff;
            # background-color: #ab2f2f !important;
        }

        .st-emotion-cache-1vk188h {background-color: rgb(171 47 47) !important; }

        .st-c3 {background:#ab2f2f; background-color: #ab2f2f !important;}

        .stHorizontalBlock.st-emotion-cache-ocqkz7{
            position: fixed;
            margin-top: 22%;
            background-color: #6c0606;
            height: 100px;
            padding-top: 2%;
            width:55%;
            color:#ffffff;
            z-index: 9999;
            padding-right: 10px;
            padding-left: 10px;
        }
        

        /* Smartphones (portrait) */
        @media (max-width: 480px) {
            .stHorizontalBlock.st-emotion-cache-ocqkz7.eiemyj0{
                z-index:9999;
                display: flex;
                flex-wrap: wrap;
                -webkit-box-flex: 1;
                flex-grow: 1;
                -webkit-box-align: stretch;
                align-items: stretch;
                # gap: 0.1rem;
                width: 95%;
                height:110px;
                padding-right:7px;
                padding-left:7px;
                padding-top:20px;
                # box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 1px;
                background-color: #ffffff !important;
                color:#ffffff;
                position: fixed;
                margin-top: 75%;
                /* margin-left: -100px;
            }
        }

        @media (min-width: 481px) and (max-width: 768px) {
            .stHorizontalBlock.st-emotion-cache-ocqkz7.eiemyj0{
                z-index:9999;
                display: flex;
                flex-wrap: wrap;
                -webkit-box-flex: 1;
                flex-grow: 1;
                -webkit-box-align: stretch;
                align-items: stretch;
                # gap: 0.1rem;
                width: 95%;
                height:110px;
                padding-right:7px;
                padding-left:7px;
                padding-top:20px;
                # box-shadow: rgba(3, 102, 214, 0.3) 0px 0px 0px 1px;
                background-color: #ffffff !important;
                color:#ffffff;
                position: fixed;
                margin-top: 50%;
                /* margin-left: -100px;
            }
        }

        /* Desktops */
        @media (min-width: 769px) {
            .stHorizontalBlock.st-emotion-cache-ocqkz7{
                position: fixed;
                margin-top: 13%;
                background-color: #ff4b4b;
                height: 100px;
                padding-top: 2%;
                z-index: 9999;
                padding-right: 10px;
                padding-left: 10px;
            }
        
    </style>
    """,
    unsafe_allow_html=True
)


def bars():
    col1, col2 = st.columns([9, 1])
    # prompt.clear()
    prompt = None
    with col1: prompt1 = st.chat_input(placeholder="Type or Use Mic To Ask Question.")
    with col2:
        # try:
        # audio_data.clear()
        audio_bytes = None
        def audio_recorder():
            audio_bytes = audio_recorder(
              text="",
              recording_color="red",
              neutral_color="green",
              icon_name="microphone",
              icon_size="2x",
            )
            if audio_bytes:
              # st.write("Prompt taken thru voice...")
              audio_file = io.BytesIO(audio_bytes)
              recognizer = speech.Recognizer()
              with speech.AudioFile(audio_file) as source:
                  audio_data = recognizer.record(source)  # Read the entire audio file
                  prompt2 = recognizer.recognize_google(audio_data).lower()
              
              # audio_data.clear()
              audio_data = None

              return prompt2
      
        if audio_bytes: = audio_recorder()
            prompt = prompt2
        else:
            prompt = prompt1
    
    return prompt


  
# st.markdown("""
#     <style>
#         [data-testid="column"]:nth-child(1){
#             background-color: none;
#         }
            
#         [data-testid="column"]:nth-child(2){
#             background-color: none;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )

if prompt := bars():
  # if detect(prompt) == "en": 
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)
        
        
    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
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
      

      st.write("   ")
    
      st.write("   ")
      st.write("   ")
      st.write("   ")
      st.write("   ")
      st.write("   ")
      st.write("   ")
    
      st.write("   ")
        
    st.session_state.messages.append({"role": "assistant", "content": response})
# prompt.clear()
prompt = None
# del prompt
