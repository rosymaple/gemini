from google import genai
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import sys

# need to add system prompt to generate content configuration for specific tasks
# adding a "personality" to the model output
client = genai.Client()
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