#!/usr/bin/env python3
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('FIREWORKS_API_KEY')
headers = {'Authorization': f'Bearer {api_key}'}

response = requests.get('https://api.fireworks.ai/inference/v1/models', headers=headers)
models = response.json()['data']

print("🔍 Available Mistral models:")
print("=" * 50)

mistral_models = []
for model in models:
    if 'mistral' in model['id'].lower():
        mistral_models.append(model)
        print(f"• {model['id']}")
        print(f"  - Kind: {model['kind']}")
        print(f"  - Chat: {model['supports_chat']}")
        print(f"  - Context: {model.get('context_length', 'N/A')}")
        print()

if not mistral_models:
    print("❌ No Mistral models found")
    print("\n📋 All available models:")
    for model in models:
        if model['supports_chat']:
            print(f"• {model['id']}") 