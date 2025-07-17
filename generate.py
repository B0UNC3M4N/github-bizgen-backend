# generate.py

import json
from uuid import uuid4
from pathlib import Path
from urllib.parse import urlparse

from app.scraper import get_trending_repos
from app.idea_generator import generate_initial_idea
from app.rater import rate_idea
from app.utils import save_json, timestamp


def load_existing_ideas():
    path = Path("output/business_ideas.json")
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []


def extract_owner_and_repo(url: str):
    try:
        parts = urlparse(url).path.strip("/").split("/")
        return parts[0], parts[1]
    except Exception:
        return "", ""


def generate_all():
    repos = get_trending_repos(max_repos=15)
    existing_ideas = load_existing_ideas()
    existing_repo_urls = {idea["repositoryUrl"] for idea in existing_ideas}
    results = existing_ideas.copy()

    for repo in repos:
        if repo["url"] in existing_repo_urls:
            print(f"⏩ Skipping (already exists): {repo['title']}")
            continue

        print(f"📦 Processing: {repo['title']}")

        try:
            idea = generate_initial_idea(repo)
            rating_raw = rate_idea(repo, idea)

            try:
                rating = json.loads(rating_raw) if isinstance(rating_raw, str) else rating_raw
            except json.JSONDecodeError:
                print(f"⚠️ Failed to parse rating JSON for {repo['title']}")
                rating = {
                    "Originality": 0,
                    "Feasibility": 0,
                    "Market Potential": 0,
                    "Monetization Clarity": 0
                }

            owner, name = extract_owner_and_repo(repo["url"])

            mapped = {
                "id": str(uuid4()),
                "repositoryTitle": repo["title"],
                "repositoryUrl": repo["url"],
                "repositoryOwner": owner,
                "repositoryName": name,
                "businessIdea": idea,
                "ratings": {
                    "originality": rating["Originality"],
                    "feasibility": rating["Feasibility"],
                    "marketPotential": rating["Market Potential"],
                    "monetizationClarity": rating["Monetization Clarity"]
                },
                "dateGenerated": timestamp().split("T")[0]
            }

            results.append(mapped)

        except Exception as e:
            print(f"❌ Failed for {repo['title']}: {e}")

    save_json(results)
    print("✅ All done. Output saved to output/business_ideas.json")


if __name__ == "__main__":
    generate_all()
