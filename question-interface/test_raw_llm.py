#!/usr/bin/env python3
"""
Test raw LLM response without JSON formatting to see what it generates.
"""

import httpx
import asyncio
import json

OLLAMA_BASE_URL = "http://localhost:11434"


async def test_raw_llm():
    """Test raw LLM response."""
    # Sample prompt similar to what the backend uses
    prompt = """Analyze these questions and answers to identify key concepts and relationships:

Q1: What are the key areas I should focus on for improving my productivity?
A1: Focus on time management, task prioritization, and eliminating distractions. Set clear goals and break them down into actionable steps...

Q2: How can I better organize my sales pipeline?
A2: Use CRM software, categorize leads by stage, set follow-up reminders, and track conversion rates...

Please provide:
1. Key concepts extracted from each Q&A
2. Semantic relationships between questions
3. Suggested concept clusters that group related questions

Format your response as JSON with this structure:
{
  "concepts": [
    {"question_id": "id", "concepts": ["concept1", "concept2"]}
  ],
  "relationships": [
    {"question1_id": "id1", "question2_id": "id2", "relationship": "similar/explains/contrasts", "strength": 0.8}
  ],
  "suggested_clusters": [
    {"name": "cluster_name", "description": "what it represents", "question_ids": ["id1", "id2"]}
  ]
}"""

    print("🔄 Testing raw LLM response...")
    print("📝 Prompt:")
    print(prompt[:200] + "...")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": "gpt-oss:20b",
                    "prompt": prompt,
                    "stream": False,
                },
            )

            if response.status_code == 200:
                result = response.json()
                llm_response = result.get("response", "")

                print("\n🤖 Raw LLM Response:")
                print("=" * 50)
                print(llm_response)
                print("=" * 50)

                # Try to parse as JSON
                try:
                    parsed = json.loads(llm_response)
                    print("✅ Response is valid JSON")
                    print(f"📦 Contains clusters: {'suggested_clusters' in parsed}")
                    if "suggested_clusters" in parsed:
                        print(
                            f"   Number of clusters: {len(parsed['suggested_clusters'])}"
                        )
                except json.JSONDecodeError as e:
                    print(f"❌ Response is not valid JSON: {e}")

                    # Try to extract JSON from the response
                    import re

                    json_match = re.search(r"\{.*\}", llm_response, re.DOTALL)
                    if json_match:
                        try:
                            parsed = json.loads(json_match.group())
                            print("✅ Found JSON in response")
                            print(
                                f"📦 Contains clusters: {'suggested_clusters' in parsed}"
                            )
                        except:
                            print("❌ JSON extraction failed")
                    else:
                        print("❌ No JSON found in response")

            else:
                print(f"❌ LLM API error: {response.status_code}")
                print(response.text)

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_raw_llm())
