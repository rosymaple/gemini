from google import genai

client = genai.Client()

# one shot prompt asks the question with one clarification example

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""We are a business selling logging and monitoring products.
    What are good products to give away at our booth at Pycon?
    Last year we gave away tote bags and they were popular and met our budget."""
)

print(response.text)