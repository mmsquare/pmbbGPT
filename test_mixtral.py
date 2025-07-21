#!/usr/bin/env python3
"""
Quick test to compare Mixtral 8x22B with Llama model
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

print("🤖 Model Comparison Test")
print("=" * 50)
print(f"Question: {question}")
print()

# Test Llama model
print("📝 Llama v3.1 8B Response:")
llama_response = test_model("accounts/fireworks/models/llama-v3p1-8b-instruct", question)
print(llama_response)
print()

# Test Mixtral model
print("📝 Mixtral 8x22B Response:")
mixtral_response = test_model("accounts/fireworks/models/mixtral-8x22b-instruct", question)
print(mixtral_response)
print()

print("✅ Test completed!") 