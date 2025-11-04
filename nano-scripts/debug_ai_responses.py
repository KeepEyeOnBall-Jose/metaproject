#!/usr/bin/env python3
"""debug_ai_responses.py

Debug AI model responses to understand why analysis results are empty.

This script tests the AI analysis endpoint and shows the raw responses
to help diagnose why clustering might not be working.

Usage:
  ./debug_ai_responses.py
"""

import sys
import requests
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


def debug_ai_response(base_url: str, questions: List[Dict[str, Any]], model: str):
    """Debug the AI analysis response for a specific model."""
    try:
        payload = {"model": model, "questions": questions}

        print(f"\n=== Testing {model.upper()} ===")
        print(f"Payload: {len(questions)} questions")

        response = requests.post(
            f"{base_url}/analyze/concepts", json=payload, timeout=60
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200:
            result = response.json()
            print(f"Response Type: {type(result)}")
            print(f"Full Response: {result}")

            if isinstance(result, dict):
                print(f"Response Keys: {list(result.keys())}")

                if "analyses" in result:
                    analyses = result["analyses"]
                    print(f"Number of analyses: {len(analyses)}")

                    for i, analysis in enumerate(analyses):
                        print(f"\nAnalysis {i+1}:")
                        print(f"  Full analysis: {analysis}")

                        if "model" in analysis:
                            print(f"  Model: {analysis['model']}")

                        if "clusters" in analysis:
                            clusters = analysis["clusters"]
                            print(f"  Clusters: {len(clusters)} items")
                            if clusters:
                                print(f"    First cluster: {clusters[0]}")
                            else:
                                print("    No clusters found!")

                        if "raw_response" in analysis:
                            raw = analysis["raw_response"]
                            print(f"  Raw response length: {len(str(raw))} chars")
                            print(f"  Raw response preview: {str(raw)[:500]}...")

                elif "error" in result:
                    print(f"Error in response: {result['error']}")
                else:
                    print(f"Unexpected response structure: {result}")
            else:
                print(f"Response is not a dict: {result}")
        else:
            print(f"HTTP Error: {response.text}")

    except Exception as e:
        print(f"ERROR: Request failed: {e}")
        import traceback

        traceback.print_exc()


def main():
    base_url = "http://localhost:8000"

    print("Debugging AI Analysis Responses")
    print("=" * 50)

    # Get questions
    questions = get_questions(base_url, limit=3)
    if not questions:
        print("No questions available")
        sys.exit(1)

    # Test both models
    for model in ["ollama", "lmstudio"]:
        debug_ai_response(base_url, questions, model)

    print("\n" + "=" * 50)
    print(
        "Debug complete. Check the raw responses above to understand why clustering might be empty."
    )


if __name__ == "__main__":
    main()
