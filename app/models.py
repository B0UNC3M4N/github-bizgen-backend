# app/models.py

from pydantic import BaseModel
from typing import List, Optional

class Repo(BaseModel):
    title: str
    url: str
    description: str
    stars: Optional[str]

class RatedIdea(BaseModel):
    summary: str
    idea: str
    monetization: str
    reason: Optional[str] = None
    rating: dict
