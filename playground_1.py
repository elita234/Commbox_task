import openai
import requests
import bs4
from PyPDF2 import PdfReader
from langchain import OpenAI

# Configure your OpenAI API key
openai.api_key = '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'


def load_file_content():
    file_path = input("Enter the file path: ")
    extension = file_path.split('.')[-1]
    content = ''
    if extension == 'pdf':
        reader = PdfReader(file_path)
        for page in reader.pages:
            content += page.extract_text()+ '\n\n\n'

    if extension == 'txt':
        with open(file_path, 'r') as file:
            content = file.read()


    return content


def load_web_content():
    url = input("Enter the website URL: ")
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    conteny = soup.body.get_text(' ', strip=True)
    return conteny


def ask_question(content):
    question = input("Enter your question: ")

    # Generate answer using ChatGPT
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", # gpt-4 || gpt-3.5-turbo
      messages=[
            {"role": "system", "content": "You are a helpful assistant, here to answer a question about the following content: " + content},
            {"role": "user", "content": question}
        ]
    )

    # Extract the answer from the model response
    answer = response['choices'][0]['message']['content']

    print('ChatGPT Answer:', answer)

while True:
    # Ask the user to choose the data source
    data_source = input("Enter 'file' to load content from a file or 'web' to load content from a website: ")

    if data_source.lower() == 'quit':
        break

    # Load content based on the chosen data source
    if data_source.lower() == 'file':
        content = load_file_content()
    elif data_source == 'web':
        content = load_web_content()
    else:
        print("Invalid data source. Please try again.")
        continue
    print(content)
    # Ask the user for a question and generate an answer
    if content:
        ask_question(content)
