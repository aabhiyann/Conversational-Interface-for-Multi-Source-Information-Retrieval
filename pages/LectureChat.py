import streamlit as st
from dotenv import load_dotenv
from utils.config import load_config
from st_audiorec import st_audiorec
from utils.htmlTemplates import css, bot_template, user_template
import io
from langchain.chains import ConversationalRetrievalChain
from openai import OpenAI as baseOpenAI
from components.vector_store import get_vectorstore
from components.text_processing import get_text_chunks
from components.conversation import get_conversation_chain
from components.handle_audio import get_handle_audio
from components.pdf_processing import create_pdf




def main():
    config = load_config()
    client = baseOpenAI()
    
    st.set_page_config(page_title="Ask a recording", layout="wide")
    st.write(css, unsafe_allow_html=True)  
    st.header("Ask a recording 📺")

    if "lectureconversation" not in st.session_state:
        st.session_state.lectureconversation = None
    if "lecturechat_history" not in st.session_state:
        st.session_state.lecturechat_history = None

    st.subheader("Record & transcribe")

    wav_audio_data = st_audiorec()

    st.header("Query a Lecture/Recording")

    user_question = st.text_input("Ask a question about the recording:")
    if user_question:
        if st.session_state.lectureconversation:
            response = st.session_state.lectureconversation({'question': user_question})
            st.session_state.lecturechat_history = response['chat_history']

    st.write('<div class="chat-messages">', unsafe_allow_html=True)
    if st.session_state.lecturechat_history:
        for i, message in enumerate(st.session_state.lecturechat_history):
            if i % 2 == 0:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)


    with st.sidebar: 
        if wav_audio_data is not None:
            st.audio(wav_audio_data, format='wav')
        if st.button("Process"):
            with st.spinner("Processing"):
                
                raw_text = get_handle_audio(wav_audio_data,client)
                
                text_chunks = get_text_chunks(raw_text)
                st.write(text_chunks)
                vectorstore = get_vectorstore(text_chunks,config)

                if vectorstore is not None:
                    st.session_state.lectureconversation = get_conversation_chain(vectorstore, config)
                else:
                    st.warning("No text found in the uploaded PDF documents.")

                newpdf=create_pdf(raw_text)
                st.download_button(label="Export_Report",
                    data=io.BytesIO(newpdf),
                    file_name="Notes.pdf")
 

if __name__ == '__main__':
    main()