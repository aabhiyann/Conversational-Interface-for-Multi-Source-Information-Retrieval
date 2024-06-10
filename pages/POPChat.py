import streamlit as st
from PyPDF2 import PdfReader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain,LLMChain
from utils.htmlTemplates import css, bot_template, user_template,file_upload_template
from langchain_community.chat_models import ChatOllama


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=7500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    vectorstore = Chroma.from_texts(texts=text_chunks,embedding=OllamaEmbeddings(model="nomic-embed-text"))
    return vectorstore


def get_conversation_chain(vectorstore):
    local_model="mistral"
    llm=ChatOllama(model=local_model)
 
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def main():
    
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.markdown("PDF Chat")
    st.sidebar.markdown("PDF Chat")
    st.write(css, unsafe_allow_html=True)

    if "popconversation" not in st.session_state:
        st.session_state.popconversation = None
    if "popchat_history" not in st.session_state:
        st.session_state.popchat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        if st.session_state.popconversation:
            response = st.session_state.popconversation({'question': user_question})
            st.session_state.popchat_history = response['chat_history']

    # session for the chat between the user and the PDF(s)
    st.write('<div class="chat-messages">', unsafe_allow_html=True)
    if st.session_state.popchat_history:
        # check if it is a user question or a response to the question
        for i, message in enumerate(st.session_state.popchat_history):
            if i % 2 == 0:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.write(file_upload_template, unsafe_allow_html=True)
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'",type="pdf", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                if vectorstore is not None:
                    st.session_state.popconversation = get_conversation_chain(vectorstore)
                else:
                    st.warning("No text found in the uploaded PDF documents.")

if __name__ == '__main__':
    main()
