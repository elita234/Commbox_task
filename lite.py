import streamlit as st
import openai_QA_util_wrapper as Util

st.title("Question Answering with URL/File Input")
st.write("Enter a URL or file path, along with a question, to get the answer.")
input_type = st.selectbox("Input Type", ("URL", "PDF", "DOCX"))
if input_type == 'URL':
    input_path = st.text_input("Enter URL")
else:
    input_path = st.text_input("Enter file path")


question = st.text_input("Enter Your Question")

method = st.selectbox("Method", ("VectorstoreIndexCreator", "map_reduce", "refine", "map_rerank"))

submit_button = st.button("Get Answer")


if submit_button:
    print(input_path)
    if method != "VectorstoreIndexCreator":
        if input_type == "URL":
            docs = Util.load_web_content(input_path)
        else:
            docs = Util.load_file_content(input_path)

        answer = Util.ask_question(docs, question, method)
    else:
        loader = Util.get_loader(file_path=input_path, filetype=input_type)
        answer = Util.ask_question_vector(loader, question)
    st.subheader("Answer:")
    st.write(answer)



###  streamlit run lite.py
