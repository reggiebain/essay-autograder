import os
import requests
import json
import pdfplumber
import docx
import csv
from dotenv import load_dotenv
import pickle

load_dotenv()


API_URL = "http://localhost:8000/grade"
API_KEY = os.getenv("API_KEY")

RUBRIC = {
    "Accuracy": {"3": "Excellent (meets all criteria)", "2": "Satisfactory", "1": "Needs Improvement"},
    "Argument": {"3": "Excellent (meets all criteria)", "2": "Satisfactory", "1": "Needs Improvement"},
    "Conclusions and Extensions": {"3": "Excellent (meets all criteria)", "2": "Satisfactory", "1": "Needs Improvement"},
    "Mechanics": {"3": "Excellent (meets all criteria)", "2": "Satisfactory", "1": "Needs Improvement"},
}
"""
You are an expert writing teacher. Grade the following student essay using the rubric below. For each of the four categories, assign a score from 1 to 3. Then briefly justify your score (2–3 sentences). The SLO (Student learning outcome) is {slo_choice}. Conclude with a total score out of 12 provide feedback
as a valid JSON object with this structure format: {{"scores": {{"Category1": 2, ...}}, "feedback": {{"Category1": "...", ...}}}}
Scoring Guide:
- 1 = Needs Improvement
- 2 = Satisfactory
- 3 = Excellent (meets all listed criteria)

Rubric Descriptions:

1. **Accuracy**  
Score of 3: The response demonstrates a deep understanding of the definition of the specific SLO (Student Learning Outcome which is analytical thinking). It includes a detailed and accurate description of how the chosen artifact reflects the student's skills in that SLO.
Score of 2: Response mentions the SLO and connects some details of the artifact to the spirit of the SLO. Seems to have an understanding of the spirit of the SLO’s definition.
Score of 1: Response loosely/vaguely ties SLO definition to artifact and lacks specific examples of the connection between the two. Demonstrates lack of full understanding of the meaning of the SLO.

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

CATEGORY_LABELS = list(RUBRIC.keys())
SLO_CHOICE = 'Analytical Thinking'

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def grade_essay(text):
    response = requests.post(
        API_URL,
        headers={"X-API-Key": API_KEY},
        json={"essay": text, "rubric": RUBRIC, "slo_choice": SLO_CHOICE},
    )
    response.raise_for_status()
    return response.json()

def process_essays(base_folder="essays"):
    results = []
    for student_folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, student_folder)
        if os.path.isdir(folder_path):
            graded = False
            for filename in os.listdir(folder_path):
                if filename.endswith((".pdf", ".docx")):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        essay_text = extract_text(file_path)
                        result = grade_essay(essay_text)
                        results.append({
                            "student": student_folder,
                            "filename": filename,
                            "scores": json.dumps(result["scores"]),
                            "feedback": json.dumps(result["feedback"]),
                        })
                        graded = True
                    except Exception as e:
                        print(f"Failed to grade {file_path}: {e}")
            if not graded:
                # No documents found — return zero scores
                results.append({
                    "student": student_folder,
                    "filename": "",
                    "scores": json.dumps({cat: 0 for cat in CATEGORY_LABELS}),
                    "feedback": json.dumps({cat: "No submission" for cat in CATEGORY_LABELS}),
                })
    return results

def save_results(results, csv_file="grading_results.csv", pkl_file="grading_results.pkl"):
    if not results:
        print("No results to save.")
        return

    # Parse scores/feedback as dicts (same as before)
    parsed_results = []
    for row in results:
        scores = row["scores"]
        feedback = row["feedback"]

        if isinstance(scores, str):
            scores = json.loads(scores)
        if isinstance(feedback, str):
            feedback = json.loads(feedback)

        parsed_row = {
            "student": row["student"],
            "filename": row["filename"]
        }
        for key in scores:
            parsed_row[f"{key}_score"] = scores.get(key, 0)
            parsed_row[f"{key}_feedback"] = feedback.get(key, "")
        parsed_results.append(parsed_row)

    # Save to CSV
    fieldnames = list(parsed_results[0].keys())
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_results)

    # Save to Pickle
    with open(pkl_file, "wb") as f:
        pickle.dump(parsed_results, f)

    print(f"Saved {len(parsed_results)} results to {csv_file} and {pkl_file}")


if __name__ == "__main__":
    results = process_essays("essays")
    save_results(results)
    print("Grading complete. Results saved to grading_results.csv")
