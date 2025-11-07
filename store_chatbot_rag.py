from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import sys
import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas


# chromadb for creating database of product descriptions and embeddings
# embeddings search for RAG chatbot
# pandas can read csv files

client = genai.Client()

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True # true = generating embeddings, false = searching for embeddings in database

    def __call__(self, input: Documents):
        # call embedding function within Documents 

        # specifiy type of embedding task
        if self.document_mode:
            embedding_task = 'retrieval_document'
        else:
            embedding_task = 'retrieval_query'

        # models.embed_content reads input and searches for embeddings

        response = client.models.embed_content(

            model='models/text-embedding-004',
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task
            )
        )

        return [e.values for e in response.embeddings] # list comprehension

# GeminiEmbeddingFunction creates embeddings for documents
# true = generate embedding, false = query embedding
embed_function = GeminiEmbeddingFunction()
embed_function.document_mode = True # generate embedding mode

# .PersistentClient creates persistent database locally
# .get_or_create_collection creates collection in database
chroma_client = chromadb.PersistentClient()
db = chroma_client.get_or_create_collection(name='zoomies_clothes', embedding_function=embed_function)

with open('id_description.csv', 'r') as file:
    clothing_data = pandas.read_csv(file) # read csv using pandas dataframe
    # read id and description columns and turn columnns into lists
    ids = list(clothing_data.ID) # list of clothing_data IDs
    descriptions = list(clothing_data.Description)  # list of clothing_data Descriptions

# upsert adds data
db.upsert(
    ids=ids,
    documents=descriptions,
)

embed_function.document_mode = False # querying the database and finding relevant documents

query = 'What are the best pants for running in the winter?'
result = db.query(query_texts=[query], n_results=5)   # how many results to return?
[all_items] = result['documents']
print(all_items)

# need to add system prompt to generate content configuration for specific tasks
# adding a "personality" to the model output

chat = client.chats.create(model='gemini-2.5-flash')

try:
    with open('chat_system_instruction.txt', 'r') as f:
        system_instruction_text = f.read()
except:
    print('Missing system instructions, quitting.')
    sys.exit(1)

try:
    with open('chat_system_instruction.txt', 'r') as f:
        system_instruction_text = f.read()
except:
    print('Missing system instructions, quitting.')
    sys.exit(1)


# while loop for prompting user input and generating RAG chatbot

while True:
    
    question = input('> ')

    # perform a RAG (retrieval augmented generation) search to find most relevant documents
    result = db.query(query_texts=[question], n_results=5) # how many results to return?
    [all_items] = result['documents']
    print(all_items)

    # Create a prompt that includes the most relevant documents from RAG search

    prompt_with_rag = f"""The user has the following question: 
    
    USER_QUESTION: {question}

    Here is information from the product database that may help answer the question:
    
    """

    for item in all_items:
        item_one_line = item.replace('\n', ' ') # replace newlines with spaces
        prompt_with_rag += f'PRODUCT: {item_one_line}\n' # reads best in one line format


    print(prompt_with_rag)

    response = chat.send_message(
        prompt_with_rag,
        config=GenerateContentConfig(
            system_instruction=system_instruction_text
        )
    )

    rich.print(Markdown(response.text))

    break

# end of while loop
# break to end program

