#!/usr/bin/env python3
"""
Debug CORS issue by testing backend directly.
"""
import requests

# Test 1: Request without Origin header
print("Test 1: Request without Origin header")
response = requests.get("http://localhost:8000/questions")
print(f"Status: {response.status_code}")
print(f"CORS headers: {dict(response.headers)}")
print()

# Test 2: Request with Origin header
print("Test 2: Request with Origin header")
response = requests.get(
    "http://localhost:8000/questions", headers={"Origin": "http://0.0.0.0:5173"}
)
print(f"Status: {response.status_code}")
print(f"CORS headers: {dict(response.headers)}")
print()

# Test 3: OPTIONS preflight request
print("Test 3: OPTIONS preflight request")
response = requests.options(
    "http://localhost:8000/questions",
    headers={"Origin": "http://0.0.0.0:5173", "Access-Control-Request-Method": "GET"},
)
print(f"Status: {response.status_code}")
print(f"CORS headers: {dict(response.headers)}")
