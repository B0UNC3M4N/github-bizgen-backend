# app/rater.py

from openai import OpenAI
from config import OPENAI_API_KEY

# Create OpenAI client instance
client = OpenAI(api_key=OPENAI_API_KEY)

def rate_idea(repo, idea):
    prompt = f"""
    Evaluate this idea based on the repo below.

    Title: {repo['title']}
    Description: {repo['description']}
    URL: {repo['url']}

    Idea:
    {idea}

    Rate on:
    - Originality (0-10)
    - Feasibility (0-10)
    - Market Potential (0-10)
    - Monetization Clarity (0-10)

    Return as JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()