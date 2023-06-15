from langchain.document_loaders import SeleniumURLLoader # UnstructuredURLLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings


import os

#  https://platform.openai.com/account/api-keys
os.environ["OPENAI_API_KEY"] = 'key'
llm = OpenAI()

#CHAIN_TYPE = 'map_reduce'  # stuff, map_reduce, refine, map_rerank
CHUNK_OVERLAP = 0
CHUNK_SIZE = 1000

char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

#region treating files with chain_types

def load_file_content(file_path=None):
    '''Load docs from pdf or docx'''
    if not file_path:
        file_path = input("Enter the file path: ")
    extension = file_path.split('.')[-1]
    if extension.lower() == 'pdf':
        loader = PyPDFLoader(file_path)
        data = loader.load_and_split()
    elif extension.lower() == 'docx':
        loader = Docx2txtLoader(file_path)
        data = loader.load()
    else:
        print('File type not recognized')
        return None
    docs = char_text_splitter.split_documents(data)
    return docs


def load_web_content(url=None):
    '''Load data from a website'''
    if not url:
        url = input("Enter the website URL: ")
    loader = SeleniumURLLoader(urls=[url])  # SeleniumURLLoader, UnstructuredURLLoader
    data = loader.load()
    docs = char_text_splitter.split_documents(data)
    return docs


def ask_question(docs, question=None, chain_type='map_reduce'):  # stuff, map_reduce, refine, map_rerank
    '''Ask a question split into a qa chain loader'''
    if not question:
        question = input("Enter your question: ")

    chain = load_qa_chain(llm=llm, chain_type=chain_type)

    answer = chain.run(input_documents=docs, question=question)

    return answer
# endregion


#region treating files with VectorstoreIndexCreator
def get_loader(file_path=None, filetype='pdf'):
    '''Return a loader for a pdf, docx or website url'''
    if filetype.lower() == 'url':
        if not file_path:
            file_path = input("Enter the website URL: ")
        loader = SeleniumURLLoader(urls=[file_path])  # SeleniumURLLoader, UnstructuredURLLoader
    elif filetype.lower() == 'pdf':
        if not file_path:
            file_path = input("Enter the pdf file path: ")
        loader = PyPDFLoader(file_path)
    elif filetype.lower() == 'docx':
        if not file_path:
            file_path = input("Enter the docx file path: ")
        loader = Docx2txtLoader(file_path)
    else:
        print('File type not recognized')
        return None
    return loader


def ask_question_vector(loader, question=None):
    '''Ask a question using VectorstoreIndexCreator'''
    if not question:
        question = input("Enter your question: ")

    index = VectorstoreIndexCreator(
        text_splitter=CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP),
        embedding=OpenAIEmbeddings(),
        vectorstore_cls=Chroma
    ).from_loaders([loader])

    answer = index.query(llm=llm, question=question, chain_type='stuff')

    return answer

#endregion


if __name__ == "__main__":
    while True:
        # Ask the user to choose the data source
        data_source = input("Enter 'pdf' or 'docx' to load content from a file or 'url' to load content from a website: ")

        if data_source.lower() == 'quit':
            break
        method = input("Should we use VectorstoreIndexCreator? ")
        if method.lower() != 'y' and method.lower() != 'yes':
            # Load content based on the chosen data source
            if data_source.lower() in ['pdf', 'docx']:
                docs = load_file_content()
            elif data_source.lower() == 'url':
                docs = load_web_content()
            else:
                print("Invalid data source. Please try again.")
                continue
            # Ask the user for a question and generate an answer
            if docs:
                response = ask_question(docs)
                print('ChatGPT Answer:', response)
                print('\n\n\n')
        else:
            loader = get_loader(file_path=None, filetype=data_source)
            response = ask_question_vector(loader)
            print('ChatGPT Answer:', response)
            print('\n\n\n')


