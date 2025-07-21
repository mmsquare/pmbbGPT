# Product Management AI Assistant

A chat-based AI assistant for product management questions, powered by Fireworks AI and LLaMA 3.1 70B model.

## Features

- 🤖 AI-powered product management advice
- 💬 Chat-like interface
- 📚 Few-shot learning with custom training data
- 🌐 Deployed on Netlify
- 🔑 Server-side API key storage (no user setup required)

## Live Demo

**🌐 Live Site**: https://fascinating-moonbeam-d04d88.netlify.app

## How to Use

1. **Visit the site** and start asking questions immediately
2. **Get AI-powered advice** based on expert examples
3. **No API key required** - everything is handled server-side

## Local Development

For local development, you can use Netlify CLI:

1. Install Netlify CLI:
```bash
npm install -g netlify-cli
```

2. Set up environment variables:
```bash
netlify env:set FIREWORKS_API_KEY "your-api-key-here"
```

3. Run locally:
```bash
netlify dev
```

4. Visit: http://localhost:8888

## Netlify Deployment

### Prerequisites
- Netlify account
- FIREWORKS_API_KEY environment variable (set in Netlify dashboard)

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

### Project Structure

```
pmbbGPT/
├── public/
│   └── index.html          # Frontend (chat interface)
├── functions/
│   ├── ask.js              # Serverless function (AI API)
│   ├── training-data.js    # Training data (JS module)
│   ├── training-data.json  # Training data (JSON format)
│   └── package.json        # Function dependencies
├── update-training-data.js # Utility to manage training data
├── netlify.toml            # Netlify configuration
└── README.md               # Documentation
```

## Security & Privacy

- **Server-side API calls**: Your Fireworks AI API key is stored securely on Netlify
- **No client-side exposure**: API key never leaves the server
- **User-friendly**: No setup required for end users

## Training Data Management

The AI assistant uses few-shot learning with product management examples stored in separate files:

### 📁 Training Data Files
- **`functions/training-data.json`** - Easy-to-edit JSON format
- **`functions/training-data.js`** - JavaScript module (auto-generated)

### 🔧 Managing Training Data

**Update training data:**
```bash
node update-training-data.js
```

**Add new example:**
```bash
node update-training-data.js add "Your question here?" "Your answer here."
```

### 📋 Current Examples
1. Feature prioritization
2. Product strategy definition  
3. Founder alignment with user needs
4. Growth vs retention tradeoffs
5. Market differentiation

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Netlify Functions (Node.js)
- **AI**: Fireworks AI LLaMA 3.1 70B
- **Deployment**: Netlify
- **Local Development**: Netlify CLI

## GitHub Repository

**📁 Source Code**: https://github.com/mmsquare/pmbbGPT 