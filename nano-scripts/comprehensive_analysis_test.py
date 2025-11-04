#!/usr/bin/env python3
"""comprehensive_analysis_test.py

Complete end-to-end test of the question analysis pipeline.

This script:
1. Fetches questions from the backend
2. Fetches answers for each question
3. Calls the AI analysis endpoint
4. Shows detailed results and debugging info

Usage:
  ./comprehensive_analysis_test.py
"""

import sys
import requests
import json
from typing import List, Dict, Any


def get_questions(base_url: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Fetch questions from the backend API."""
    try:
        response = requests.get(f"{base_url}/questions", timeout=10)
        response.raise_for_status()
        questions = response.json()
        return questions[:limit]
    except Exception as e:
        print(f"ERROR: Failed to fetch questions: {e}")
        return []


def get_answer(base_url: str, question_id: str) -> str:
    """Fetch answer for a specific question."""
    try:
        response = requests.get(
            f"{base_url}/questions/{question_id}/answer", timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "") if data.get("has_answer") else ""
    except Exception as e:
        print(f"Warning: Failed to fetch answer for {question_id}: {e}")
        return ""


def test_full_analysis(base_url: str):
    """Test the complete analysis pipeline."""
    print("=== COMPREHENSIVE ANALYSIS TEST ===")
    print()

    # Step 1: Get questions
    print("1. Fetching questions...")
    questions = get_questions(base_url, limit=3)
    if not questions:
        print("ERROR: No questions retrieved")
        return

    print(f"Retrieved {len(questions)} questions:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q['question'][:60]}...")
        print(f"     Category: {q['category']}")
        print(f"     Has notes: {bool(q.get('notes'))}")
    print()

    # Step 2: Get answers
    print("2. Fetching answers...")
    questions_with_answers = []
    for q in questions:
        answer = get_answer(base_url, q["id"])
        question_with_answer = {
            "id": q["id"],
            "question": q["question"],
            "answer": answer,
            "category": q["category"],
        }
        questions_with_answers.append(question_with_answer)

        has_answer = bool(answer.strip())
        print(f"  {q['id']}: {'✓' if has_answer else '✗'} ({len(answer)} chars)")

    print()

    # Step 3: Prepare analysis payload
    print("3. Preparing analysis payload...")
    payload = {"questions": questions_with_answers}

    print(f"Payload contains {len(payload['questions'])} questions")
    questions_with_content = [q for q in payload["questions"] if q["answer"].strip()]
    print(f"Questions with answer content: {len(questions_with_content)}")

    if not questions_with_content:
        print("WARNING: No questions have answer content!")
        print("This will cause the analysis to return empty results.")
        return

    print()

    # Step 4: Call analysis
    print("4. Calling AI analysis endpoint...")
    try:
        response = requests.post(
            f"{base_url}/analyze/concepts",
            json=payload,
            timeout=120,  # Give it more time for AI processing
        )

        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")

        if response.status_code == 200:
            result = response.json()
            print("\nResponse structure:")
            print(f"  Keys: {list(result.keys())}")
            print(f"  Analyses count: {len(result.get('analyses', []))}")
            print(f"  Fallback used: {result.get('fallback_used', False)}")

            analyses = result.get("analyses", [])
            if analyses:
                print("\nAnalysis details:")
                for i, analysis in enumerate(analyses):
                    print(f"  Analysis {i+1}:")
                    print(f"    Model: {analysis.get('model_name', 'unknown')}")
                    print(f"    Concepts: {len(analysis.get('concepts', []))}")
                    print(
                        f"    Relationships: {len(analysis.get('relationships', []))}"
                    )
                    print(
                        f"    Clusters: {len(analysis.get('suggested_clusters', []))}"
                    )
                    print(f"    Has error: {bool(analysis.get('error'))}")

                    if analysis.get("error"):
                        print(f"    Error: {analysis['error']}")

                    if analysis.get("raw_response"):
                        raw = analysis["raw_response"]
                        print(f"    Raw response length: {len(raw)} chars")
                        print(f"    Raw response preview: {raw[:200]}...")

                    print()
            else:
                print("  No analyses in response!")

        else:
            print(f"HTTP Error: {response.text}")

    except Exception as e:
        print(f"ERROR: Analysis request failed: {e}")
        import traceback

        traceback.print_exc()


def main():
    base_url = "http://localhost:8000"

    test_full_analysis(base_url)

    print("\n=== TEST COMPLETE ===")


if __name__ == "__main__":
    main()
