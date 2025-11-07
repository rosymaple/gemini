from google import genai
import rich
from rich.markdown import Markdown

client = genai.Client()
chat = client.chats.create(model='gemini-2.5-flash')

while True:
    prompt = input('Enter your message: ')
    response = chat.send_message(prompt + ' Answer in a short sentence. ')
    # print(response.text)
    rich.print(Markdown(response.text))
    print(response.usage_metadata.total_token_count)


# response = client.models.generate_content(
#     model='gemini-2.5-flash',
#     contents="""We are a business selling logging and monitoring products.
#     What are good products to give away at our booth at Pycon?"""
# )



