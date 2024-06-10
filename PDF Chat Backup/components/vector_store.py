from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS

def get_vectorstore(text_chunks, config):
    if not text_chunks:
        return None

    embeddings = OpenAIEmbeddings(openai_api_key=config["OPENAI_API_KEY"])
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore