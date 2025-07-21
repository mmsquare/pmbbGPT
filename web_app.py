#!/usr/bin/env python3
"""
Simple Flask web interface for the Product Management AI Assistant
"""

from flask import Flask, render_template, request, jsonify
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Fireworks AI configuration
FIREWORKS_API_BASE = "https://api.fireworks.ai/inference/v1"
API_KEY = os.getenv('FIREWORKS_API_KEY')
MODEL_ID = "accounts/fireworks/models/llama-v3p1-70b-instruct"

def load_training_data():
    """Load training data for few-shot examples"""
    examples = []
    try:
        with open('data.JSONL', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    examples.append(data)
    except FileNotFoundError:
        print("Warning: data.JSONL not found")
    return examples

def create_few_shot_prompt(examples, user_question, max_examples=3):
    """Create a few-shot prompt with training examples"""
    prompt = "You are a product management expert. Here are some examples of how to answer questions:\n\n"
    
    for i, example in enumerate(examples[:max_examples]):
        prompt += f"Question: {example['input']}\n"
        prompt += f"Answer: {example['output']}\n\n"
    
    prompt += f"Now answer this question:\nQuestion: {user_question}\nAnswer:"
    return prompt

def query_model(question):
    """Query the Fireworks AI model"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Load training data for few-shot learning
    examples = load_training_data()
    prompt = create_few_shot_prompt(examples, question)
    
    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
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
            return result['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error: {e}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'})
    
    answer = query_model(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 