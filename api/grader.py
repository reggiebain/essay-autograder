# api/grader.py
import os
import openai
from openai import OpenAI
from api.models import GradingRequest, GradingResponse
import json

#openai.api_key = os.getenv("OPENAI_API_KEY")
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Load environment variable manually in case dotenv is needed
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def format_prompt(essay: str, rubric: dict) -> str:
    # rubric_str = "\n".join(
    #    f"{category}:\n" + "\n".join(f"  {score}: {desc}" for score, desc in scores.items())
    #    for category, scores in rubric.items()
    # )
    return f"""
You are an expert writing teacher. Grade the following student essay using the rubric below.
For each of the four categories, assign a score from 1 to 3 and justify your score in 2–3 sentences. 
Conclude with a total score out of 12. Format your response as valid JSON:

{{"scores": {{"Category1": 2, ...}}, "feedback": {{"Category1": "...", ...}}}}

Scoring Guide:
- 1 = Needs Improvement
- 2 = Satisfactory
- 3 = Excellent

Rubric:
\"\"\"{rubric}\"\"\"

Essay:
\"\"\"{essay}\"\"\"
"""



def grade_essay(request: GradingRequest) -> GradingResponse:
    prompt = format_prompt(request.essay, request.rubric)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    content = response.choices[0].message.content.strip()
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = eval(content)  # fallback (not recommended)

    return GradingResponse(**parsed)
