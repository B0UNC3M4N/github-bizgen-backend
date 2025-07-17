# app/scraper.py

import requests
from bs4 import BeautifulSoup
from config import GITHUB_TOKEN

def get_trending_repos(language=None, since="daily", max_repos=30):
    url = "https://github.com/trending"
    if language:
        url += f"/{language}"
    params = {"since": since}

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    repos = []
    articles = soup.select("article.Box-row")

    for article in articles[:max_repos]:
        # Get repo title and link
        repo_link_tag = article.select_one("h2 a")
        if not repo_link_tag:
            continue

        href = repo_link_tag.get("href")  # e.g., /vercel/next.js
        title = href.strip("/").replace("/", " / ")
        repo_url = "https://github.com" + href
        owner, name = href.strip("/").split("/")

        # Description
        description_tag = article.select_one("p")
        description = description_tag.text.strip() if description_tag else "No description"

        # Stars
        stars_tag = article.select_one("a.Link--muted[href$='/stargazers']")
        stars = stars_tag.text.strip() if stars_tag else "0"

        # Fetch README
        readme = get_readme(owner, name)

        repos.append({
            "title": title,
            "url": repo_url,
            "owner": owner,
            "name": name,
            "description": description,
            "stars": stars,
            "readme": readme
        })

    return repos

def get_readme(owner, repo):
    headers = {
        "Accept": "application/vnd.github.v3.raw",
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"❌ README not found for {owner}/{repo}")
        return "No README available."
