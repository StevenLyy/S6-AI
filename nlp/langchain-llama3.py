import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA


ollama = Ollama(base_url='http://localhost:11434', model='llama3')

def generate_response(file, input_text):
    with open(file.name, 'wb') as f:
        f.write(file.getvalue())
    loader = PyPDFLoader(file.name)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectordb = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())
    qachain = RetrievalQA.from_chain_type(ollama, retriever=vectordb.as_retriever())

    response = qachain({"query": input_text})

    st.info(response['result'])


st.title('Ask a question about a PDF document')

with st.form('my_form'):
    local_file = st.file_uploader('Upload a PDF file', type=['pdf'])
    query_text = st.text_area('Enter query:', 'Ask a question about the document')
    submitted = st.form_submit_button('Submit')
    if submitted and local_file is not None:
        generate_response(local_file, query_text)
    elif submitted:
        st.warning('Please upload a file first')