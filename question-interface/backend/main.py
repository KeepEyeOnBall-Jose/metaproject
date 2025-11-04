from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import csv
import os

app = FastAPI(title="Question Tracker API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)


# Data model for questions
class Question(BaseModel):
    id: str
    question: str
    category: str
    created_at: str
    status: str
    notes: Optional[str] = None


# Load questions from CSV
QUESTIONS_FILE = os.path.join(
    os.path.dirname(__file__), "../../metaproject-life/data/questions.csv"
)


def load_questions() -> List[Question]:
    questions = []
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ensure all keys are strings
                row = {str(k): v for k, v in row.items()}
                questions.append(Question(**row))
    except FileNotFoundError:
        # Return empty list if file not found
        pass
    return questions


@app.get("/questions", response_model=List[Question])
def get_questions():
    return load_questions()


@app.get("/questions/{question_id}", response_model=Question)
def get_question(question_id: str):
    questions = load_questions()
    for q in questions:
        if q.id == question_id:
            return q
    raise HTTPException(status_code=404, detail="Question not found")


@app.get("/categories")
def get_categories():
    questions = load_questions()
    categories = {}
    for q in questions:
        categories[q.category] = categories.get(q.category, 0) + 1
    return categories  # {category: count}
