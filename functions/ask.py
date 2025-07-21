import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    api_key = os.getenv('FIREWORKS_API_KEY')
    model_id = "accounts/fireworks/models/llama-v3p1-70b-instruct"
    
    if not api_key:
        return "Error: FIREWORKS_API_KEY not found in environment variables"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Load training data for few-shot learning
    examples = load_training_data()
    prompt = create_few_shot_prompt(examples, question)

    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
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
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {e}"

def handler(event, context):
    """Netlify function handler"""
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }
    
    # Handle preflight requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        body = json.loads(event['body'])
        question = body.get('question', '')
        
        if not question:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No question provided'})
            }
        
        # Get AI response
        answer = query_model(question)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'answer': answer})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        } 