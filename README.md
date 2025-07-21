# Product Management AI Assistant

A chat-based AI assistant for product management questions, powered by Fireworks AI and LLaMA 3.1 70B model.

## Features

- 🤖 AI-powered product management advice
- 💬 Chat-like interface
- 📚 Few-shot learning with custom training data
- 🌐 Deployed on Netlify

## Local Development

1. Install dependencies:
```bash
pip install flask requests python-dotenv
```

2. Set up environment variables:
```bash
cp env.example .env
# Edit .env and add your FIREWORKS_API_KEY
```

3. Run locally:
```bash
python web_app.py
```

4. Visit: http://localhost:8080

## Netlify Deployment

### Prerequisites
- Netlify account
- FIREWORKS_API_KEY environment variable

### Deployment Steps

1. **Install Netlify CLI** (if not already installed):
```bash
npm install -g netlify-cli
```

2. **Login to Netlify**:
```bash
netlify login
```

3. **Initialize and deploy**:
```bash
netlify init
netlify deploy --prod
```

4. **Set environment variables** in Netlify dashboard:
   - Go to Site settings > Environment variables
   - Add `FIREWORKS_API_KEY` with your API key

### Project Structure for Netlify

```
pmbbGPT/
├── public/              # Static files
│   └── index.html      # Frontend
├── functions/           # Serverless functions
│   ├── ask.py          # AI API handler
│   ├── requirements.txt # Python dependencies
│   └── data.JSONL      # Training data
├── netlify.toml        # Netlify configuration
└── requirements.txt    # Root dependencies
```

## API Usage

The AI assistant uses few-shot learning with 5 product management examples:

1. Feature prioritization
2. Product strategy definition
3. Founder alignment with user needs
4. Growth vs retention tradeoffs
5. Market differentiation

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Netlify Functions (Python)
- **AI**: Fireworks AI LLaMA 3.1 70B
- **Deployment**: Netlify 