from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import csv
import os
import httpx
import json

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


# Answers directory path
ANSWERS_DIR = os.path.join(
    os.path.dirname(__file__), "../../metaproject-life/data/answers"
)


@app.get("/questions/{question_id}/answer")
def get_answer(question_id: str):
    """Get the markdown answer for a specific question."""
    # Find the question to verify it exists
    questions = load_questions()
    question = None
    for q in questions:
        if q.id == question_id:
            question = q
            break

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if the question has an answer reference
    if not question.notes or not question.notes.startswith("answer:"):
        return {"has_answer": False, "answer": None}

    # Extract the answer filename from notes
    answer_filename = question.notes.replace("answer:", "").strip()
    answer_path = os.path.join(
        os.path.dirname(__file__), "../../metaproject-life/data", answer_filename
    )

    # Read the markdown file
    try:
        with open(answer_path, "r", encoding="utf-8") as f:
            answer_content = f.read()
        return {"has_answer": True, "answer": answer_content}
    except FileNotFoundError:
        return {"has_answer": False, "answer": None}


# LLM Analysis Models
class ConceptAnalysisRequest(BaseModel):
    questions: List[Dict[str, Any]]  # List of {id, question, answer, category}


class ModelAnalysis(BaseModel):
    model_name: str
    concepts: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    suggested_clusters: List[Dict[str, Any]]
    raw_response: Optional[str] = None
    error: Optional[str] = None


class ConceptAnalysisResponse(BaseModel):
    analyses: List[ModelAnalysis]  # Multiple model analyses
    fallback_used: bool = False


OLLAMA_BASE_URL = "http://localhost:11434"
LMSTUDIO_BASE_URL = "http://localhost:1234"  # Default LMStudio port


@app.post("/analyze/concepts", response_model=ConceptAnalysisResponse)
async def analyze_concepts(request: ConceptAnalysisRequest):
    """Analyze questions and answers to discover concepts and relationships using multiple LLMs."""
    try:
        # Prepare data for LLM analysis
        qa_pairs = []
        for q in request.questions:
            if q.get("answer"):
                qa_pairs.append(
                    {
                        "id": q["id"],
                        "question": q["question"][:200],  # Truncate for LLM
                        "answer": q["answer"][:500],  # Truncate for LLM
                        "category": q["category"],
                    }
                )

        if not qa_pairs:
            return ConceptAnalysisResponse(analyses=[], fallback_used=True)

        # Define available models
        models = [
            {
                "name": "Ollama (gpt-oss:20b)",
                "url": OLLAMA_BASE_URL,
                "model": "gpt-oss:20b",
            },
            {"name": "LMStudio", "url": LMSTUDIO_BASE_URL, "model": "local-model"},
        ]

        analyses = []

        # Create enhanced prompt for better analysis
        prompt = f"""Analyze these questions and answers to identify key concepts, themes, and relationships.
Focus on finding meaningful connections between questions, even if they seem unrelated at first glance.

{chr(10).join([f"Q{i+1}: {qa['question']}\\nA{i+1}: {qa['answer'][:300]}..." for i, qa in enumerate(qa_pairs[:10])])}

Please provide a detailed analysis:
1. Key concepts and themes extracted from each Q&A pair
2. Semantic relationships between questions (similar, explains, contrasts, builds-upon, etc.)
3. Suggested concept clusters that group related questions by theme or topic

Format your response as JSON:
{{
  "concepts": [
    {{"question_id": "id", "concepts": ["concept1", "concept2", "theme1"]}}
  ],
  "relationships": [
    {{"question1_id": "id1", "question2_id": "id2", "relationship": "similar/explains/contrasts", "strength": 0.8, "reasoning": "brief explanation"}}
  ],
  "suggested_clusters": [
    {{"name": "cluster_name", "description": "detailed description of what this cluster represents", "question_ids": ["id1", "id2"], "themes": ["theme1", "theme2"]}}
  ]
}}"""

        # Try each model
        for model_config in models:
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"{model_config['url']}/api/generate",
                        json={
                            "model": model_config["model"],
                            "prompt": prompt,
                            "stream": False,
                        },
                    )

                    if response.status_code == 200:
                        result = response.json()
                        llm_response = result.get("response", "{}")

                        # Try to parse JSON response
                        try:
                            analysis_data = json.loads(llm_response)
                            analyses.append(
                                ModelAnalysis(
                                    model_name=model_config["name"],
                                    concepts=analysis_data.get("concepts", []),
                                    relationships=analysis_data.get(
                                        "relationships", []
                                    ),
                                    suggested_clusters=analysis_data.get(
                                        "suggested_clusters", []
                                    ),
                                    raw_response=llm_response,
                                )
                            )
                        except json.JSONDecodeError:
                            # Try to extract JSON from markdown
                            import re

                            json_match = re.search(
                                r"```(?:json)?\s*\n(.*?)\n```", llm_response, re.DOTALL
                            )
                            if json_match:
                                try:
                                    analysis_data = json.loads(
                                        json_match.group(1).strip()
                                    )
                                    analyses.append(
                                        ModelAnalysis(
                                            model_name=model_config["name"],
                                            concepts=analysis_data.get("concepts", []),
                                            relationships=analysis_data.get(
                                                "relationships", []
                                            ),
                                            suggested_clusters=analysis_data.get(
                                                "suggested_clusters", []
                                            ),
                                            raw_response=llm_response,
                                        )
                                    )
                                except json.JSONDecodeError:
                                    analyses.append(
                                        ModelAnalysis(
                                            model_name=model_config["name"],
                                            concepts=[],
                                            relationships=[],
                                            suggested_clusters=[],
                                            raw_response=llm_response,
                                            error="JSON parsing failed",
                                        )
                                    )
                            else:
                                analyses.append(
                                    ModelAnalysis(
                                        model_name=model_config["name"],
                                        concepts=[],
                                        relationships=[],
                                        suggested_clusters=[],
                                        raw_response=llm_response,
                                        error="No JSON found in response",
                                    )
                                )
                    else:
                        analyses.append(
                            ModelAnalysis(
                                model_name=model_config["name"],
                                concepts=[],
                                relationships=[],
                                suggested_clusters=[],
                                error=f"HTTP {response.status_code}: {response.text}",
                            )
                        )

            except Exception as e:
                analyses.append(
                    ModelAnalysis(
                        model_name=model_config["name"],
                        concepts=[],
                        relationships=[],
                        suggested_clusters=[],
                        error=str(e),
                    )
                )

        # If no analyses succeeded, provide fallback
        if not analyses or all(
            not analysis.concepts and not analysis.suggested_clusters
            for analysis in analyses
        ):
            # Create basic category-based clusters as fallback
            categories = {}
            for qa in qa_pairs:
                cat = qa["category"]
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(qa["id"])

            fallback_clusters = [
                {
                    "name": cat,
                    "description": f"Questions categorized as '{cat}' - basic grouping by category",
                    "question_ids": ids,
                    "themes": [cat],
                }
                for cat, ids in categories.items()
            ]

            analyses.append(
                ModelAnalysis(
                    model_name="Fallback Analysis",
                    concepts=[
                        {"question_id": qa["id"], "concepts": [qa["category"]]}
                        for qa in qa_pairs
                    ],
                    relationships=[],
                    suggested_clusters=fallback_clusters,
                )
            )

        return ConceptAnalysisResponse(
            analyses=analyses,
            fallback_used=len(analyses) == 1
            and analyses[0].model_name == "Fallback Analysis",
        )

    except Exception as e:
        # Ultimate fallback
        qa_pairs = []
        for q in request.questions:
            if q.get("answer"):
                qa_pairs.append({"id": q["id"], "category": q["category"]})

        categories = {}
        for qa in qa_pairs:
            cat = qa["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(qa["id"])

        fallback_clusters = [
            {
                "name": cat,
                "description": f"Questions in {cat} category",
                "question_ids": ids,
                "themes": [cat],
            }
            for cat, ids in categories.items()
        ]

        return ConceptAnalysisResponse(
            analyses=[
                ModelAnalysis(
                    model_name="Error Fallback",
                    concepts=[
                        {"question_id": qa["id"], "concepts": [qa["category"]]}
                        for qa in qa_pairs
                    ],
                    relationships=[],
                    suggested_clusters=fallback_clusters,
                    error=str(e),
                )
            ],
            fallback_used=True,
        )
