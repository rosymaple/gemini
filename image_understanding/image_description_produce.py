from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel

client = genai.Client()

class Produce(BaseModel):
    name: str
    color: str
    fruit_or_veg: str # "fruit" or "vegetable"

with open('image_understanding/fruits-and-vegetables.png', 'rb') as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
        'What produce is in this picture?'
    ],
    config=GenerateContentConfig(
        system_instruction="""Identify as many produce items as you can, 
        but please be accurate because my job depends on it. 
        Include the color and 
        "Fruit" for fruits and "Vegetable" for vegetables.""",
        response_mime_type='application/json',
        response_schema=list[Produce]
    )
)

print(response.parsed)

for produce_item in response.parsed:
    print(produce_item.name)



