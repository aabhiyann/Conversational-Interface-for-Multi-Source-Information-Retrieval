import streamlit as st
from InstructorEmbedding import INSTRUCTOR
from langchain_community.vectorstores.faiss import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain,LLMChain
from langchain_openai import OpenAI,ChatOpenAI
from utils.htmlTemplates import css, bot_template, user_template, header_template, file_upload_template
from utils.config import load_config
from components.pdf_processing import get_pdf_text
from components.text_processing import get_text_chunks
from components.vector_store import get_vectorstore
from components.conversation import get_conversation_chain

# main function
def main():
    # loading config files (contains API key) to the main file. 
    config = load_config()

    # using streamlit to set the application page title
    st.set_page_config(page_title="Ask questions to PDFs", page_icon="🧾")
    st.write(css, unsafe_allow_html=True)  

    # check if the current session contains pre-existing conversation
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    # check if the current session contains pre-existing chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Ask questions to PDFs")
    st.write(header_template, unsafe_allow_html=True)  # Render the header template

    user_question = st.text_input("Enter your questions to the document(s) here: ")
    # is user asks a question, generate response
    if user_question:
        if st.session_state.conversation:
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']

    # session for the chat between the user and the PDF(s)
    st.write('<div class="chat-messages">', unsafe_allow_html=True)
    if st.session_state.chat_history:
        # check if it is a user question or a response to the question
        for i, message in enumerate(reversed(st.session_state.chat_history)):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)
        

    # sidebar to upload PDF(s)
    with st.sidebar:
        st.write(file_upload_template, unsafe_allow_html=True)  # Render the file upload instructions
        pdf_docs = st.file_uploader("", accept_multiple_files=True, key="file_uploader")
        if st.button("Process", key="process_button"):        
            with st.spinner("Processing your document"):
                raw_text = get_pdf_text(pdf_docs) # use get_pdf_text function to extract text information from the pdf
                text_group = get_text_chunks(raw_text) # use get_text_chunks function to group the raw text into multiple groups
                vectorstore = get_vectorstore(text_group, config) # use get_vectorstore function to store the vector values for these text groups

                if vectorstore is not None:
                    st.session_state.conversation = get_conversation_chain(vectorstore, config)
                else:
                    st.warning("No text found in the uploaded PDF documents.")

if __name__ == '__main__':
    main()