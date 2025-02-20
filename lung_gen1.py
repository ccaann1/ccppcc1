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
from langdetect import detect

showErrorDetails = False

listener = speech.Recognizer()



get_this_id = st.query_params.get("passer")  
if get_this_id:
    get_this_id = get_this_id.lower()
    
    if get_this_id == 'english' or get_this_id == 'spanish' or get_this_id == 'hindi':	
        response = requests.get('https://canceproit.pythonanywhere.com/hereignore')
        data = response.json()
        take_this = data[0]
        # Show title and description.
        if get_this_id == 'english':
            E_Main_Head = "Hi, I am Isha!!!"
            E_Sub_Text = "A Conversational ChatBot built by CancePro. As a part of our Research we have collected information from renowned Cancer research institutes research documents. Ask a question in the below box, get relevant information and be Healthy by taking precautions."
            box_text = "Type or Use Mic To Ask Question."

        if get_this_id == 'hindi':
            E_Main_Head = "नमस्कार, मैं ईशा हूँ!!!"
            E_Sub_Text = "केंसप्रो द्वारा निर्मित एक संवादी चैटबॉट। हमारे शोध के एक भाग के रूप में हमने प्रसिद्ध कैंसर अनुसंधान संस्थानों के शोध दस्तावेजों से जानकारी एकत्र की है। नीचे दिए गए बॉक्स में एक प्रश्न पूछें, प्रासंगिक जानकारी प्राप्त करें और सावधानी बरतते हुए स्वस्थ रहें।  "
            box_text = " प्रश्न पूछने के लिए माइक लिखें या उपयोग करें. "

        if get_this_id == 'spanish':
            E_Main_Head = " Hola, soy Isha!!  "
            E_Sub_Text = " Un ChatBot Conversacional creado por CancePro. Como parte de nuestra investigación, hemos recopilado información de documentos de investigación de reconocidos institutos de investigación del cáncer. Haga una pregunta en el cuadro a continuación, obtenga información relevante y esté saludable tomando precauciones.  "
            box_text = " Escriba o use el micrófono para hacer una pregunta. "

        st.write(E_Main_Head)

        st.write(E_Sub_Text)

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
        
        def bars():
            col1, col2 = st.columns([9, 1])
            # prompt.clear()
            prompt = None
            with col1: prompt1 = st.chat_input(placeholder=box_text)
            with col2:
                # try:
                # audio_data.clear()
                audio_bytes = None
                def audio_recorderr():
                    try:
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
                                prompt2 = recognizer.recognize_google(audio_data)
                            
                            # audio_data.clear()
                            audio_data = None
                        
                        return prompt2
                    
                    except:
                        pass
                        # st.write('I am Ready to take input. Click again on Microphone.')
                
                prompt2 = audio_recorderr()
            
            if prompt1 is not None:
                prompt = prompt1
            
            else:
                prompt = prompt2
            
            # st.write(prompt)
            
            return prompt

        prompt = bars()

        if prompt:
            user_q_lang = detect(prompt)
            
            if user_q_lang == 'en':
                now_get_this_id = 'English'

            elif user_q_lang == 'es':
                now_get_this_id = 'Spanish'

            elif user_q_lang == 'hi':
                now_get_this_id = 'Hindi'

            else:
                now_get_this_id = 'English'
                # st.write('We are working on increasing our Language base. Will help you too in coming days.')

            # if detect(prompt) == "en": 
            # Store and display the current prompt.
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)
                
                
            # Generate a response using the OpenAI API.
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant to tell only about Cancer and health related questions. While responding back, please respond in {now_get_this_id} language, whereever required feel free to use math characters please do not use other language characters. Always remember, you have to respond very politely. You are lastly trained in First Week of January 2025. Your name is Isha developed by CancePro and you were launched on January 10, 2025 for the first time. CancePro launched on May 15, 2024. CancePro is to find Cancer Probability in Food Using AI. Also you can get inputs through voice, if any user asks about your input capabilities tell that you are capable to take inputs through text or listening their audio or voice."},
                ]
                +[
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


    else:
        st.write('We are working on increasing our Language base. Will help you too in coming days.')
        # Create the button
        if st.button('English'):
            target_url = 'https://canceprochat.streamlit.app/?passer=english'
            st.write(f'Redirecting to [this page]({target_url})...')
            st.markdown(f'<meta http-equiv="refresh" content="0;url={target_url}">', unsafe_allow_html=True)

        if st.button('हिंदी'):
            target_url = 'https://canceprochat.streamlit.app/?passer=hindi'
            st.write(f'Redirecting to [this page]({target_url})...')
            st.markdown(f'<meta http-equiv="refresh" content="0;url={target_url}">', unsafe_allow_html=True)

        if st.button('Española'):
            target_url = 'https://canceprochat.streamlit.app/?passer=spanish'
            st.write(f'Redirecting to [this page]({target_url})...')
            st.markdown(f'<meta http-equiv="refresh" content="0;url={target_url}">', unsafe_allow_html=True)

        
