from google import genai
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import os

# need to add system prompt to generate content configuration for specific tasks
# adding a "personality" to the model output
client = genai.Client()
chat = client.chats.create(model='gemini-2.5-flash')

while True:
    question = input('Enter your question for the tutor: ')
    response = chat.send_message(
        question,
        config=GenerateContentConfig(
            system_instruction="""You are a helpful programming tutor.
            This is a Java programming class. 
            You can explain concepts and programs but don't give users the answer.
            If the user asks for code, ask them questions and explain concepts
            to help them write it themselves. Be positive and encouraging at all times."""
        )
    )

    rich.print(Markdown(response.text))

    break

# end of while loop
# break to end program







