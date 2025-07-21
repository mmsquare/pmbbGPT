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

print("🔍 Your Available Models:")
print("=" * 50)

# Check for fine-tuned models
fine_tuned_models = []
for model in models:
    if model['kind'] in ['HF_PEFT_ADDON', 'CUSTOM_MODEL'] or 'finetune' in model['id'].lower():
        fine_tuned_models.append(model)
        print(f"🎯 Fine-tuned Model: {model['id']}")
        print(f"   - Kind: {model['kind']}")
        print(f"   - Owner: {model['owned_by']}")
        print(f"   - Created: {model['created']}")
        print(f"   - Chat: {model['supports_chat']}")
        print()

# Check for models owned by your account
your_models = []
for model in models:
    if 'your-account' in model['owned_by'].lower() or 'ming_air' in model['owned_by'].lower():
        your_models.append(model)
        print(f"👤 Your Model: {model['id']}")
        print(f"   - Kind: {model['kind']}")
        print(f"   - Owner: {model['owned_by']}")
        print()

if not fine_tuned_models and not your_models:
    print("❌ No fine-tuned models found")
    print("\n💡 To create a fine-tuned model:")
    print("1. Check if Fireworks AI supports fine-tuning in your plan")
    print("2. Contact Fireworks AI support for fine-tuning access")
    print("3. Use the few-shot learning approach (which is working well!)")

print("\n📋 All available models for reference:")
print("-" * 30)
for model in models:
    if model['supports_chat']:
        print(f"• {model['id']} ({model['kind']})") 