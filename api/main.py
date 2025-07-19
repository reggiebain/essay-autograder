# api/main.py
from fastapi import FastAPI, HTTPException, Header
from api.models import GradingRequest, GradingResponse
from api.grader import grade_essay
import os

API_KEY = os.getenv("API_KEY")

app = FastAPI()


@app.post("/grade", response_model=GradingResponse)
async def grade(request: GradingRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return grade_essay(request)
