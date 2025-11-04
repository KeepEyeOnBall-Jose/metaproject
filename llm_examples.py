"""
Simple LLM Query Examples for Metaproject
Add this to your existing Python files to integrate LLM queries
"""

from llm_client import query_ollama, query_lmstudio, LocalLLMClient, get_available_services

# Example 1: Quick one-off queries

# Simple query to Ollama
response = query_ollama("Summarize this concept in 2 sentences: quantum entanglement")
if response:
    print(f"Ollama: {response}")

# Simple query to LM Studio
response = query_lmstudio("Explain recursion in programming simply")
if response:
    print(f"LM Studio: {response}")

# Example 2: Using the client class for more control

# Initialize clients
ollama_client = LocalLLMClient("ollama")
lm_client = LocalLLMClient("lmstudio")

# Check what's available
services = get_available_services()
print(f"Available: Ollama={services['ollama']}, LM Studio={services['lmstudio']}")

# Query with specific parameters
if services['ollama']:
    response = ollama_client.query(
        prompt="What are the main benefits of microservices architecture?",
        model="gpt-oss:20b",  # or whatever model you have
        temperature=0.3,      # more focused responses
        max_tokens=200
    )
    print(f"Microservices benefits: {response}")

if services['lmstudio']:
    response = lm_client.query(
        prompt="Write a haiku about debugging code",
        temperature=0.8,      # more creative
        max_tokens=100
    )
    print(f"Debugging haiku: {response}")

# Example 3: Integration with your question interface
def enhance_question_with_llm(question_text: str) -> str:
    """Use LLM to enhance or analyze questions"""
    if not services['lmstudio']:
        return question_text

    prompt = f"""Analyze this question and suggest improvements:
Question: {question_text}

Provide:
1. Is this question clear?
2. One suggestion to make it better
3. Enhanced version

Keep response under 100 words."""

    response = lm_client.query(prompt, max_tokens=150)
    return response if response else question_text

# Example usage in your question interface
# question = "how do computers work?"
# enhanced = enhance_question_with_llm(question)
# print(enhanced)