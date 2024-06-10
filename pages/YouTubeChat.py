import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain,LLMChain
from langchain_openai import OpenAI,ChatOpenAI
from utils.htmlTemplates import css, bot_template, user_template, header_template, file_upload_template
from openai import OpenAI as baseOpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.prompts import PromptTemplate
from utils.config import load_config
from audio_recorder_streamlit import audio_recorder
from components.text_processing import get_text_chunks
from components.vector_store import get_vectorstore
from components.conversation import get_conversation_chain
from components.handle_audio import get_handle_audio
from components.yt_text_processing import get_yt_text,get_youtube_id



def main():
    # loading config files (contains API key) to the main file. 
    config = load_config()
    client = baseOpenAI()
    # using streamlit to set the application page title
    st.set_page_config(page_title="Ask Youtube Video", layout="wide")
    st.write(css, unsafe_allow_html=True)  

    # check if the current session contains pre-existing conversation
    if "ytconversation" not in st.session_state:
        st.session_state.ytconversation = None
    # check if the current session contains pre-existing chat history
    if "ytchat_history" not in st.session_state:
        st.session_state.ytchat_history = None
    if 'ytflag' not in st.session_state:
        st.session_state.ytflag=0

    st.header("Query a Youtube Video")
    st.write(header_template, unsafe_allow_html=True)  # Render the header template
    audio_bytes = audio_recorder(energy_threshold=(5.0))
    user_question = st.text_input("Ask a question about the Video:")
    if st.button("reset"):
        st.session_state.ytflag=0
        audio_bytes=None
        user_question=None
    # is user asks a question, generate response
    if audio_bytes and st.session_state.ytflag!=1:
        st.audio(audio_bytes, format="audio/wav")
        txt=get_handle_audio(audio_bytes,client) 
        st.session_state.ytflag=1
        if st.session_state.ytconversation:
            response = st.session_state.ytconversation({'question': txt})
            st.session_state.ytchat_history = response['chat_history'] 
    elif user_question:
        if st.session_state.ytconversation:
            response = st.session_state.ytconversation({'question': user_question})
            st.session_state.ytchat_history = response['chat_history']
        

    # session for the chat between the user and the PDF(s)
    st.write('<div class="chat-messages">', unsafe_allow_html=True)
    if st.session_state.ytchat_history:
        # check if it is a user question or a response to the question
        for i, message in enumerate(st.session_state.ytchat_history):
            if i % 2 == 0:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)
        

    with st.sidebar:
        video_url = st.text_input('Add the desired Youtube video ID or URL here.')
        if st.button("Process", key="process_button"):        
            with st.spinner("Processing"):
                if video_url :
                    video_id = get_youtube_id(video_url)
                raw_text = get_yt_text(video_id)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks,config)

                if vectorstore is not None:
                    st.session_state.ytconversation = get_conversation_chain(vectorstore, config)
                else:
                    st.warning("No text found in the uploaded PDF documents.")

if __name__ == '__main__':
    main()
