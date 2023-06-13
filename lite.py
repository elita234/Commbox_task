import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import SeleniumURLLoader  # UnstructuredURLLoader
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import openai_QA_util_wrapper as Util


os.environ["OPENAI_API_KEY"] = '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'
llm = OpenAI()
char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)


st.title("Question Answering with URL/PDF Input")
st.write("Enter a URL or file path, along with a question, to get the answer.")
input_type = st.selectbox("Input Type", ("URL", "PDF"))
if input_type == 'URL':
    input_path = st.text_input("Enter URL")
else:
    input_path = st.text_input("Enter file path")


question = st.text_input("Enter Your Question")
submit_button = st.button("Get Answer")


if submit_button:
    print(input_path)

    if input_type == "URL":
        docs = Util.load_web_content(input_path)
    else:
        docs = Util.load_pdf_content(input_path)


    answer = Util.ask_question(docs, question)

    st.subheader("Answer:")
    st.write(answer)



###  streamlit run lite.py ###
