#!/usr/bin/env python3
"""
Fireworks AI Model Usage Script
Uses existing models with few-shot learning since fine-tuning API may not be available
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fireworks AI API endpoints
FIREWORKS_API_BASE = "https://api.fireworks.ai/inference/v1"

def setup_api_key():
    """Set up the Fireworks AI API key"""
    api_key = os.getenv('FIREWORKS_API_KEY')
    if not api_key or api_key == 'your-api-key-here':
        print("❌ FIREWORKS_API_KEY not set or still has placeholder value")
        return None
    
    print("✅ API key configured")
    return api_key

def load_training_data(data_path):
    """Load training data for few-shot examples"""
    print(f"📊 Loading training data from: {data_path}")
    
    examples = []
    with open(data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                examples.append(data)
    
    print(f"✅ Loaded {len(examples)} examples")
    return examples

def create_few_shot_prompt(examples, user_question, max_examples=3):
    """Create a few-shot prompt with training examples"""
    prompt = "You are a product management expert. Here are some examples of how to answer questions:\n\n"
    
    # Add examples (limit to avoid token limits)
    for i, example in enumerate(examples[:max_examples]):
        prompt += f"Question: {example['input']}\n"
        prompt += f"Answer: {example['output']}\n\n"
    
    prompt += f"Now answer this question:\nQuestion: {user_question}\nAnswer:"
    
    return prompt

def query_model(api_key, model_id, prompt, max_tokens=500):
    """Query the Fireworks AI model"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(
            f"{FIREWORKS_API_BASE}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return content
        else:
            print(f"❌ Error querying model: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error querying model: {e}")
        return None

def test_with_training_data(api_key, examples, model_id="accounts/fireworks/models/llama-v3p1-70b-instruct"):
    """Test the model with training data examples"""
    print(f"🧪 Testing model: {model_id}")
    print("=" * 50)
    
    for i, example in enumerate(examples):
        print(f"\n📝 Test {i+1}:")
        print(f"Question: {example['input']}")
        
        # Create few-shot prompt
        other_examples = [ex for j, ex in enumerate(examples) if j != i]
        prompt = create_few_shot_prompt(other_examples, example['input'])
        
        # Get model response
        response = query_model(api_key, model_id, prompt)
        
        if response:
            print(f"🤖 Model Response: {response}")
            print(f"✅ Expected: {example['output'][:100]}...")
        else:
            print("❌ Failed to get response")
        
        print("-" * 30)

def interactive_chat(api_key, examples, model_id="accounts/fireworks/models/llama-v3p1-70b-instruct"):
    """Interactive chat mode"""
    print(f"💬 Interactive chat mode with model: {model_id}")
    print("Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        user_input = input("\n🤔 Your question: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Create few-shot prompt
        prompt = create_few_shot_prompt(examples, user_input)
        
        # Get model response
        response = query_model(api_key, model_id, prompt)
        
        if response:
            print(f"🤖 Answer: {response}")
        else:
            print("❌ Sorry, I couldn't generate a response.")

def list_available_models(api_key):
    """List available models"""
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(
            f"{FIREWORKS_API_BASE}/models",
            headers=headers
        )
        
        if response.status_code == 200:
            models = response.json()['data']
            print("📋 Available models:")
            print("=" * 50)
            
            for model in models:
                if model['supports_chat']:
                    print(f"• {model['id']} ({model['kind']})")
            
            return models
        else:
            print(f"❌ Error listing models: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return None

def main():
    """Main function"""
    print("🤖 Fireworks AI Product Management Assistant")
    print("=" * 50)
    
    # Setup
    api_key = setup_api_key()
    if not api_key:
        return
    
    data_path = "data.JSONL"
    
    # Load training data
    examples = load_training_data(data_path)
    if not examples:
        print("❌ No training data found")
        return
    
    # List available models
    models = list_available_models(api_key)
    if not models:
        return
    
    # Choose a model (using LLaMA 3.1 70B - best LLaMA 3 model available)
    model_id = "accounts/fireworks/models/llama-v3p1-70b-instruct"
    
    print(f"\n🎯 Using model: {model_id}")
    
    # Test with training data
    test_with_training_data(api_key, examples, model_id)
    
    # Interactive chat
    print("\n" + "=" * 50)
    interactive_chat(api_key, examples, model_id)

if __name__ == "__main__":
    main() 