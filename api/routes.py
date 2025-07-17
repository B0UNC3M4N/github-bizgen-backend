# api/routes.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path
import json

router = APIRouter()

@router.get("/ideas")
def get_ideas():
    file_path = Path("output/business_ideas.json")
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"message": "No data found"})

    with open(file_path, "r") as f:
        data = json.load(f)

    return {"ideas": data}  # ✅ Frontend expects {"ideas": [...]}
