#!/usr/bin/env python3
"""test_ai_analysis.py

Test the AI analysis endpoint with real questions from the backend.

This script:
1. Fetches questions from the backend API
2. Tests the AI analysis endpoint with Ollama and LMStudio models
3. Displays the results for comparison

Usage:
  ./test_ai_analysis.py

Requirements:
- Backend server must be running on port 8000
- Ollama and/or LMStudio should be available on their respective ports
"""

import sys
import json
import requests
from typing import List, Dict, Any


def get_questions(base_url: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Fetch questions from the backend API."""
    try:
        response = requests.get(f"{base_url}/questions", timeout=10)
        response.raise_for_status()
        questions = response.json()
        return questions[:limit]  # Return first 'limit' questions
    except Exception as e:
        print(f"ERROR: Failed to fetch questions: {e}")
        return []


def test_ai_analysis(
    base_url: str, questions: List[Dict[str, Any]], model: str
) -> Dict[str, Any]:
    """Test the AI analysis endpoint with a specific model."""
    try:
        payload = {"model": model, "questions": questions}

        print(f"Testing AI analysis with {model}...")
        response = requests.post(
            f"{base_url}/analyze/concepts",
            json=payload,
            timeout=60,  # AI analysis might take longer
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"ERROR: AI analysis failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": f"HTTP {response.status_code}", "details": response.text}

    except Exception as e:
        print(f"ERROR: AI analysis request failed: {e}")
        return {"error": str(e)}


def main():
    base_url = "http://localhost:8000"

    print("Testing AI Analysis Endpoint")
    print("=" * 50)

    # Step 1: Get questions
    print("1. Fetching questions from backend...")
    questions = get_questions(base_url, limit=3)

    if not questions:
        print("ERROR: No questions retrieved. Is the backend running?")
        sys.exit(1)

    print(f"Retrieved {len(questions)} questions:")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q.get('question', 'N/A')[:80]}...")
    print()

    # Step 2: Test with different models
    models_to_test = ["ollama", "lmstudio"]

    results = {}
    for model in models_to_test:
        print(f"2. Testing {model.upper()} analysis...")
        result = test_ai_analysis(base_url, questions, model)
        results[model] = result

        if "error" not in result:
            print(f"✓ {model.upper()} analysis completed successfully")
            # Show a summary of the results
            if "analyses" in result:
                print(f"  Found {len(result['analyses'])} analysis results")
                for analysis in result["analyses"][:2]:  # Show first 2
                    model_name = analysis.get("model", "unknown")
                    clusters = analysis.get("clusters", [])
                    print(f"    {model_name}: {len(clusters)} clusters")
            else:
                print(f"  Unexpected response format: {list(result.keys())}")
        else:
            print(f"✗ {model.upper()} analysis failed: {result['error']}")

        print()

    # Step 3: Summary
    print("3. Summary:")
    successful_models = [m for m, r in results.items() if "error" not in r]
    failed_models = [m for m, r in results.items() if "error" in r]

    if successful_models:
        print(f"✓ Successful models: {', '.join(successful_models)}")
    if failed_models:
        print(f"✗ Failed models: {', '.join(failed_models)}")

    if successful_models:
        print("\nAI analysis is working! The baseUrl fix is successful.")
        sys.exit(0)
    else:
        print("\nAI analysis failed for all models. Check backend and LLM services.")
        sys.exit(1)


if __name__ == "__main__":
    main()
