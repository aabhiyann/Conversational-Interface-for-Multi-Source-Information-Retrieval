import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from utils.htmlTemplates import css, bot_template, user_template, header_template, file_upload_template
from openai import OpenAI as baseOpenAI
from utils.config import load_config
from audio_recorder_streamlit import audio_recorder
from components.text_processing import get_text_chunks
from components.vector_store import get_vectorstore
from components.conversation import get_conversation_chain
from components.handle_audio import get_handle_audio




def main():
    # loading config files (contains API key) to the main file. 
    config = load_config()
    client = baseOpenAI()
    # using streamlit to set the application page title
    st.set_page_config(page_title="Ask Youtube Video", layout="wide")
    st.write(css, unsafe_allow_html=True)  

    # check if the current session contains pre-existing conversation
    if "recconversation" not in st.session_state:
        st.session_state.recconversation = None
    # check if the current session contains pre-existing chat history
    if "recchat_history" not in st.session_state:
        st.session_state.recchat_history = None
    if 'aflag' not in st.session_state:
        st.session_state.aflag=0

    st.header("Query a Recording")
    st.write(header_template, unsafe_allow_html=True)  # Render the header template
    audio_bytes = audio_recorder(energy_threshold=(5.0))
    user_question = st.text_input("Ask a question about the Video:")
    if st.button("reset audio"):
        st.session_state.aflag=0
        audio_bytes=None
        user_question=None
    # is user asks a question, generate response
    if audio_bytes and st.session_state.aflag!=1:
        st.audio(audio_bytes, format="audio/wav")
        txt=get_handle_audio(audio_bytes,client) 
        st.session_state.aflag=1
        if st.session_state.recconversation:
            response = st.session_state.recconversation({'question': txt})
            st.session_state.recchat_history = response['chat_history'] 
    elif user_question:
        if st.session_state.recconversation:
            response = st.session_state.recconversation({'question': user_question})
            st.session_state.recchat_history = response['chat_history']
        

    # session for the chat between the user and the PDF(s)
    st.write('<div class="chat-messages">', unsafe_allow_html=True)
    if st.session_state.recchat_history:
        # check if it is a user question or a response to the question
        for i, message in enumerate(st.session_state.recchat_history):
            if i % 2 == 0:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)
        

    with st.sidebar:
        audiorec = st.file_uploader("Upload an audio file", type=["wav","mp3"])
        if st.button("Process", key="process_button"):        
            with st.spinner("Processing"):

                raw_text = get_handle_audio(audiorec.read(),client)
                st.write(raw_text)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks,config)

                if vectorstore is not None:
                    st.session_state.recconversation = get_conversation_chain(vectorstore, config)
                else:
                    st.warning("No text found in the uploaded PDF documents.")

if __name__ == '__main__':
    main()
