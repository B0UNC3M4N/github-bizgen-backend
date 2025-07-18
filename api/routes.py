# api/routes.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from pathlib import Path
import json
import httpx

router = APIRouter()

@router.get("/ideas")
def get_ideas():
    file_path = Path("output/business_ideas.json")
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"message": "No data found"})

    with open(file_path, "r") as f:
        data = json.load(f)

    return {"ideas": data}  # ✅ Frontend expects {"ideas": [...]}

@router.get("/preview-image")
async def proxy_github_image(owner: str, repo: str):
    url = f"https://opengraph.githubassets.com/1/{owner}/{repo}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return StreamingResponse(content=response.iter_bytes(), media_type="image/png")