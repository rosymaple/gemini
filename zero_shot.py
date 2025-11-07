from google import genai

client = genai.Client()

# zero shot prompt asks the question with no clarifying examples

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""We are a business selling logging and monitoring products.
    What are good products to give away at our booth at Pycon?"""
)

print(response.text)