# app/idea_generator.py

from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_initial_idea(repo):
    prompt = f"""
You're a startup founder. You just discovered this open-source GitHub project:

Title: {repo['title']}
Description: {repo['description']}
URL: {repo['url']}
Readme snippet: {repo.get('readme', '')[:500]}

Based on this project, describe one clear, creative, and realistic business idea that you or another founder could build. Be concise but compelling. Avoid any disclaimers, AI-sounding phrases, or unnecessary explanation.

Respond with only the business idea in natural, human-like language.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message.content.strip()
