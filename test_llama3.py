#!/usr/bin/env python3
"""
Test different LLaMA 3 models available on Fireworks AI
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('FIREWORKS_API_KEY')
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

def test_model(model_id, question):
    """Test a specific model with a question"""
    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": question}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            "https://api.fireworks.ai/inference/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}"
            
    except Exception as e:
        return f"Error: {e}"

# Test question
question = "How should I prioritize features when everything feels urgent?"

print("🤖 LLaMA 3 Model Comparison Test")
print("=" * 50)
print(f"Question: {question}")
print()

# Test different LLaMA 3 models
models_to_test = [
    ("accounts/fireworks/models/llama-v3p1-8b-instruct", "LLaMA 3.1 8B"),
    ("accounts/fireworks/models/llama-v3p1-70b-instruct", "LLaMA 3.1 70B"),
    ("accounts/fireworks/models/llama-v3p3-70b-instruct", "LLaMA 3.3 70B"),
    ("accounts/fireworks/models/llama-v3p1-405b-instruct", "LLaMA 3.1 405B"),
]

for model_id, model_name in models_to_test:
    print(f"📝 {model_name} Response:")
    print("-" * 30)
    response = test_model(model_id, question)
    print(response)
    print("\n" + "=" * 50 + "\n")

print("✅ Test completed!")
print("\n💡 Recommendation: LLaMA 3.1 70B offers the best balance of performance and speed") 