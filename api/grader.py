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

def format_prompt(essay: str, rubric: dict, slo_choice: str) -> str:
    # rubric_str = "\n".join(
    #    f"{category}:\n" + "\n".join(f"  {score}: {desc}" for score, desc in scores.items())
    #    for category, scores in rubric.items()
    # )
    return f"""
You are an expert writing teacher. Grade the following student essay using the rubric below. For each of the four categories, assign a score from 1 to 3. Then briefly justify your score (2–3 sentences). The SLO (Student learning outcome) is {slo_choice}. Conclude with a total score out of 12 provide feedback
as a valid JSON object with this structure format: {{"scores": {{"Category1": 2, ...}}, "feedback": {{"Category1": "...", ...}}}}
Scoring Guide:
- 1 = Needs Improvement
- 2 = Satisfactory
- 3 = Excellent (meets all listed criteria)

Rubric Descriptions:

1. **Accuracy**  
Score of 3: The response demonstrates a deep understanding of the definition of {slo_choice}. It includes a detailed and accurate description of how the chosen artifact reflects the student's skills in that SLO.
Score of 2: Response mentions the  ({slo_choice}) and connects some details of the artifact to the spirit of {slo_choice}. Seems to have an understanding of the spirit of the definition of {slo_choice}.
Score of 1: Response loosely/vaguely ties SLO definition to artifact and lacks specific examples of the connection between the two. Demonstrates lack of full understanding of the meaning of {slo_choice}.

2. **Argument**  
Score of 3: The response presents logically sequenced, well-developed ideas with smooth transitions between sections or paragraphs. It provides multiple specific examples of how the artifact connects to the SLO definition.
Score of 2: Most ideas are well sequenced and fleshed out. Some transition between sections/paragraphs is provided and some specific connections between SLO and details of the artifact are discussed.
Score of 1: Response lacks proper structure and does not communicate logically sequenced ideas. Little to no transition between paragraphs/sections and only vague references to the connections between the SLO and specifics of the artifacts are provided.

3. **Conclusions & Extensions**  
Score of 3: The response is engaging and clearly explains how the SLO was assessed in the artifact. It thoughtfully discusses how their work or the assignment could be improved to better assess the SLO.
Score of 2: Response states how the SLO was assessed in the artifact. Mentions how their work or the assignment itself could be modified to improve its assessment of the SLO.
Score of 1: Response loosely connects SLO with specifics of the artifact or shows lack of complete understanding of the SLO’s definition. Does not sufficiently address ways in which their work or the design of the artifact could be modified to improve its assessment of the SLO.

4. **Mechanics**  
Score of 3: The response shows exemplary effort with no errors in spelling, grammar, punctuation, or formatting. It demonstrates extensive editing and thoughtful reflection.
Score of 2: Response contains minor errors in grammar, spelling, and/or punctuation. Shows some evidence of editing but contains minor logical inconsistencies, run on sentences, etc.
Score of 1: Response is provided but little to no editing appears evident. Contains multiple grammatical errors, run-on sentences, sentence fragments, spelling errors, etc.

Essay:
\"\"\"{essay}\"\"\"
"""


def grade_essay(request: GradingRequest) -> GradingResponse:
    prompt = format_prompt(request.essay, request.rubric, request.slo_choice)

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
