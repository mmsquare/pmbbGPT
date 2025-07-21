#!/usr/bin/env python3
"""
Check different possible fine-tuning API endpoints on Fireworks AI
"""

import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('FIREWORKS_API_KEY')
headers = {'Authorization': f'Bearer {api_key}'}

# Different possible fine-tuning endpoints to test
endpoints_to_test = [
    "https://api.fireworks.ai/fine_tuning/v1/files",
    "https://api.fireworks.ai/v1/fine_tuning/files", 
    "https://api.fireworks.ai/fine-tuning/v1/files",
    "https://api.fireworks.ai/v1/fine-tuning/files",
    "https://api.fireworks.ai/training/v1/files",
    "https://api.fireworks.ai/v1/training/files",
    "https://api.fireworks.ai/models/v1/files",
    "https://api.fireworks.ai/v1/models/files",
]

print("🔍 Testing Fine-tuning API Endpoints")
print("=" * 50)

for endpoint in endpoints_to_test:
    try:
        response = requests.get(endpoint, headers=headers)
        print(f"✅ {endpoint} - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ {endpoint} - Error: {e}")
    print()

print("📋 Checking if fine-tuning is mentioned in models endpoint...")
try:
    response = requests.get('https://api.fireworks.ai/inference/v1/models', headers=headers)
    if response.status_code == 200:
        models = response.json()['data']
        fine_tune_models = [m for m in models if m['kind'] in ['HF_PEFT_ADDON', 'CUSTOM_MODEL']]
        print(f"Found {len(fine_tune_models)} fine-tuned models:")
        for model in fine_tune_models:
            print(f"  - {model['id']} ({model['kind']}) - Owner: {model['owned_by']}")
    else:
        print(f"❌ Error accessing models: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}") 