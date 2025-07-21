#!/usr/bin/env python3
"""
Fireworks AI Custom Model Training Script
Uses REST API directly since fine-tuning is not available in the Python SDK
"""

import os
import json
import requests
import time
from pathlib import Path
from dotenv import load_dotenv

# Fireworks AI API endpoints
FIREWORKS_API_BASE = "https://api.fireworks.ai/inference/v1"
FINE_TUNING_API_BASE = "https://api.fireworks.ai/v1/fine_tuning"

def setup_api_key():
    """Set up the Fireworks AI API key"""
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv('FIREWORKS_API_KEY')
    if not api_key or api_key == 'your-api-key-here':
        print("❌ FIREWORKS_API_KEY not set or still has placeholder value")
        print("Please:")
        print("1. Copy env.example to .env")
        print("2. Edit .env and replace 'your-api-key-here' with your actual API key")
        print("3. Get your API key from: https://console.fireworks.ai/")
        return None
    
    print("✅ API key configured")
    return api_key

def validate_data(data_path):
    """Validate the training data format"""
    print(f"📊 Validating data from: {data_path}")
    
    if not Path(data_path).exists():
        print(f"❌ Data file not found: {data_path}")
        return False
    
    valid_count = 0
    invalid_count = 0
    
    with open(data_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                if 'input' in data and 'output' in data:
                    valid_count += 1
                else:
                    print(f"⚠️  Line {line_num}: Missing 'input' or 'output' field")
                    invalid_count += 1
            except json.JSONDecodeError:
                print(f"❌ Line {line_num}: Invalid JSON")
                invalid_count += 1
    
    print(f"✅ Valid examples: {valid_count}")
    if invalid_count > 0:
        print(f"⚠️  Invalid examples: {invalid_count}")
    
    return valid_count > 0

def upload_training_data(api_key, data_path):
    """Upload training data to Fireworks AI"""
    print("📤 Uploading training data...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Read and prepare the data
        with open(data_path, 'r') as f:
            data_content = f.read()
        
        # Upload the file
        upload_url = f"{FINE_TUNING_API_BASE}/files"
        files = {
            'file': ('data.jsonl', data_content, 'application/json')
        }
        
        response = requests.post(upload_url, headers=headers, files=files)
        
        if response.status_code == 200:
            file_data = response.json()
            file_id = file_data['id']
            print(f"✅ File uploaded successfully. File ID: {file_id}")
            return file_id
        else:
            print(f"❌ Error uploading file: {response.status_code} - {response.text}")
            return None
        
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return None

def create_fine_tune_job(api_key, file_id, model_name="llama-v3-8b-instruct"):
    """Create a fine-tuning job"""
    print(f"🚀 Creating fine-tuning job for model: {model_name}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "training_file": file_id,
        "model": model_name,
        "hyperparameters": {
            "n_epochs": 3,
            "batch_size": 1,
            "learning_rate_multiplier": 1.0
        }
    }
    
    try:
        response = requests.post(
            f"{FINE_TUNING_API_BASE}/jobs",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            job_data = response.json()
            job_id = job_data['id']
            print(f"✅ Fine-tuning job created. Job ID: {job_id}")
            return job_id
        else:
            print(f"❌ Error creating fine-tuning job: {response.status_code} - {response.text}")
            return None
        
    except Exception as e:
        print(f"❌ Error creating fine-tuning job: {e}")
        return None

def monitor_training(api_key, job_id):
    """Monitor the training progress"""
    print(f"📈 Monitoring training job: {job_id}")
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    while True:
        try:
            response = requests.get(
                f"{FINE_TUNING_API_BASE}/jobs/{job_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                job = response.json()
                status = job['status']
                
                print(f"Status: {status}")
                
                if status == "succeeded":
                    print("🎉 Training completed successfully!")
                    model_id = job.get('fine_tuned_model')
                    print(f"Model ID: {model_id}")
                    return model_id
                elif status == "failed":
                    print("❌ Training failed")
                    error = job.get('error')
                    if error:
                        print(f"Error: {error}")
                    return None
                elif status in ["pending", "running"]:
                    print("⏳ Training in progress...")
                    time.sleep(30)  # Wait 30 seconds before checking again
                else:
                    print(f"Unknown status: {status}")
                    return None
            else:
                print(f"❌ Error checking job status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error monitoring job: {e}")
            return None

def test_model(api_key, model_id):
    """Test the trained model"""
    print(f"🧪 Testing model: {model_id}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": "How should I prioritize features when everything feels urgent?"}
        ],
        "max_tokens": 200
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
            print("✅ Model test successful!")
            print(f"Response: {content}")
            return True
        else:
            print(f"❌ Model test failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        return False

def main():
    """Main training function"""
    print("🤖 Fireworks AI Custom Model Training")
    print("=" * 50)
    
    # Setup
    api_key = setup_api_key()
    if not api_key:
        return
    
    data_path = "data.JSONL"
    
    # Validate data
    if not validate_data(data_path):
        print("❌ Data validation failed")
        return
    
    # Upload data
    file_id = upload_training_data(api_key, data_path)
    if not file_id:
        return
    
    # Create fine-tuning job
    job_id = create_fine_tune_job(api_key, file_id)
    if not job_id:
        return
    
    # Monitor training
    model_id = monitor_training(api_key, job_id)
    
    if model_id:
        print("\n🎯 Training Summary:")
        print(f"✅ Model trained successfully!")
        print(f"📋 Model ID: {model_id}")
        print(f"📁 Training data: {data_path}")
        print(f"🔧 Job ID: {job_id}")
        
        # Test the model
        print("\n🧪 Testing the trained model...")
        test_model(api_key, model_id)
        
        print("\nYou can now use this model with:")
        print(f"fireworks.client.chat.completions.create(model='{model_id}', ...)")
    else:
        print("❌ Training failed or was cancelled")

if __name__ == "__main__":
    main() 