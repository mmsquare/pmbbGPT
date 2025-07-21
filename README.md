# Product Management AI Assistant

A chat-based AI assistant for product management questions, powered by Fireworks AI and LLaMA 3.1 70B model.

## Features

- 🤖 AI-powered product management advice
- 💬 Chat-like interface
- 📚 Few-shot learning with custom training data
- 🌐 Deployed on Netlify
- 🔒 Client-side API calls (your API key stays private)

## Live Demo

**🌐 Live Site**: https://fascinating-moonbeam-d04d88.netlify.app

## How to Use

1. **Visit the site** and enter your Fireworks AI API key
2. **Ask questions** about product management
3. **Get AI-powered advice** based on expert examples

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
- FIREWORKS_API_KEY (entered by users in the browser)

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

### Project Structure

```
pmbbGPT/
├── public/
│   └── index.html      # Frontend (chat interface + API calls)
├── templates/
│   └── index.html      # Flask template (for local development)
├── netlify.toml        # Netlify configuration
├── web_app.py          # Flask app (for local development)
└── README.md           # Documentation
```

## Security & Privacy

- **API Key Security**: Your Fireworks AI API key is stored locally in your browser and never sent to our servers
- **Client-side Processing**: All API calls are made directly from your browser to Fireworks AI
- **No Server Storage**: We don't store any of your conversations or API keys

## API Usage

The AI assistant uses few-shot learning with 5 product management examples:

1. Feature prioritization
2. Product strategy definition
3. Founder alignment with user needs
4. Growth vs retention tradeoffs
5. Market differentiation

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **AI**: Fireworks AI LLaMA 3.1 70B
- **Deployment**: Netlify (Static Site)
- **Local Development**: Flask

## GitHub Repository

**📁 Source Code**: https://github.com/mmsquare/pmbbGPT 