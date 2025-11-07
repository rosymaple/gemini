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

client = genai.Client()

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True # true = generating embeddings, false = searching for embeddings in database

    def __call__(self, input: Documents):
        if self.document_mode:
            embedding_task = 'retrieval_document'
        else:
            embedding_task = 'retrieval_query'

        response = client.models.embed_content(

            model='models/text-embedding-004',
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task
            )
        )

        return [e.values for e in response.embeddings] # list comprehension

embed_function = GeminiEmbeddingFunction()
embed_function.document_mode = True # generate embedding mode

chroma_client = chromadb.PersistentClient()
db = chroma_client.get_or_create_collection(name='zoomies_clothes', embedding_function=embed_function)

with open('id_description.csv', 'r') as file:
    clothing_data = pandas.read_csv(file) # read csv using pandas dataframe
    # read id and description columns and turn columnns into lists
    ids = list(clothing_data.ID)
    descriptions = list(clothing_data.Description)

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


while True:
    question = input('> ')
    response = chat.send_message(
        question,
        config=GenerateContentConfig(
            system_instruction=system_instruction_text
        )
    )

    rich.print(Markdown(response.text))

    break

# end of while loop
# break to end program