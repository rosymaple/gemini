from google import genai
import rich
from rich.markdown import Markdown


client = genai.Client()     # generate client to talk to gemini api

response = client.models.generate_content(
    # specify model and prompt
    model='gemini-2.5-flash',
    contents="""We are a business selling logging and monitoring products.
    What are good products to give away at our booth at Pycon?"""
)

# print(response.text) print text response from gemini 

rich.print(Markdown(response.text))     

# rich markdown formatting

print(response.usage_metadata)

# print token usage metadata