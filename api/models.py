# api/models.py
from pydantic import BaseModel
from typing import Dict


class GradingRequest(BaseModel):
    essay: str
    rubric: Dict[str, Dict[str, str]]


class GradingResponse(BaseModel):
    scores: Dict[str, int]
    feedback: Dict[str, str]
