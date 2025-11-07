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
        # open and read system instruction from file
        system_instruction_text = f.read()
except:
    # try except error handling
    print('Missing system instructions, quitting.')
    sys.exit(1) # error code 1 = failure to run program


while True:
    question = input('> ')
    # asks for input from user at > symbol
    response = chat.send_message(
        question,
        # generate response using system instruction
        config=GenerateContentConfig(
            system_instruction=system_instruction_text
        )
    )

    rich.print(Markdown(response.text))

    break

# end of while loop
# break to end program