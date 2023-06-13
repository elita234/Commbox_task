from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import SeleniumURLLoader
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI

llm = OpenAI(openai_api_key='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')


loader = PyPDFLoader("1.pdf")
pages = loader.load_and_split()

#print(pages)

urls = [
    #"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    #"https://goo.gl/maps/NDSHwePEyaHMFGwh8",
    'https://en.wikipedia.org/wiki/Wikipedia'
]
loader = SeleniumURLLoader(urls=urls)
data = loader.load()


chain = load_qa_chain(llm=llm, chain_type='refine') # stuff, map_reduce, refine, map_rerank

query = "Whats the number of benign samples?"
query = "When was wikipedia founded?"
response = chain.run(input_documents=data, question=query)
print(response)