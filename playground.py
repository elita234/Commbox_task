from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import SeleniumURLLoader # UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter



import os
os.environ["OPENAI_API_KEY"] = "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"

loader = PyPDFLoader("1.pdf")
pages = loader.load_and_split()

#print(pages)

urls = [
    #"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    #"https://goo.gl/maps/NDSHwePEyaHMFGwh8",
    'https://en.wikipedia.org/wiki/Herzliya'
]
loader = SeleniumURLLoader(urls=urls) # SeleniumURLLoader, UnstructuredURLLoader
data = loader.load()

char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs = char_text_splitter.split_documents(data)

#print(len(docs))


chain = load_qa_chain(llm=OpenAI(), chain_type='map_reduce') # stuff, map_reduce, refine, map_rerank

query = "When was wikipedia founded?"
response = chain.run(input_documents=docs, question=query)
print(response)




'''# split the documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)
# select which embeddings we want to use
embeddings = OpenAIEmbeddings()
# create the vectorestore to use as the index
db = Chroma.from_documents(texts, embeddings)
# expose this index in a retriever interface
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":2})
# create a chain to answer questions
qa = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
query = "How many AI publications in 2021?"
result = qa({"query": query})

print(result)'''