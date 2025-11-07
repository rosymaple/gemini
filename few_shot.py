from google import genai

client = genai.Client()

# few shot prompts ask the question with multiple clarifying examples

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""We are a business selling logging and monitoring products.
    What are good products to give away at our booth at Pycon?
    Last year we gave away tote bags and they were popular and met our budget.
    The year before we gave away pens and they were cheap but not popular.
    The year before we gave away water bottles and they were popular but too expensive."""
)

print(response.text)