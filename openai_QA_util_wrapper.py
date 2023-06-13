from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import SeleniumURLLoader # UnstructuredURLLoader
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
os.environ["OPENAI_API_KEY"] = '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'
llm = OpenAI()

CHAIN_TYPE = 'map_reduce'  # stuff, map_reduce, refine, map_rerank
CHUNK_OVERLAP = 0
CHUNK_SIZE = 500

char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)


def load_pdf_content(file_path=None):
    if not file_path:
        file_path = input("Enter the file path: ")
    #extension = file_path.split('.')[-1]

    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    docs = char_text_splitter.split_documents(pages)
    return docs


def load_web_content(url=None):
    if not url:
        url = input("Enter the website URL: ")
    loader = SeleniumURLLoader(urls=[url])  # SeleniumURLLoader, UnstructuredURLLoader
    data = loader.load()
    docs = char_text_splitter.split_documents(data)
    return docs


def ask_question(docs, question=None):
    if not question:
        question = input("Enter your question: ")

    chain = load_qa_chain(llm=llm, chain_type=CHAIN_TYPE)

    response = chain.run(input_documents=docs, question=question)

    return response
    #print('ChatGPT Answer:', response)
    #print('\n\n\n')


if __name__ == "__main__":
    while True:
        # Ask the user to choose the data source
        data_source = input("Enter 'pdf' to load content from a file or 'url' to load content from a website: ")

        if data_source.lower() == 'quit':
            break

        # Load content based on the chosen data source
        if data_source.lower() == 'pdf':
            docs = load_pdf_content()
        elif data_source == 'url':
            docs = load_web_content()
        else:
            print("Invalid data source. Please try again.")
            continue
        # Ask the user for a question and generate an answer
        if docs:
            response = ask_question(docs)
            print('ChatGPT Answer:', response)
            print('\n\n\n')
