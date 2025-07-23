const axios = require('axios');
const TRAINING_DATA = require('./training-data');

function createFewShotPrompt(userQuestion, maxExamples = 3) {
    let prompt = "You are a product management expert. Here are some examples of how to answer questions:\n\n";

    for (let i = 0; i < Math.min(maxExamples, TRAINING_DATA.length); i++) {
        const example = TRAINING_DATA[i];
        prompt += `Question: ${example.input}\n`;
        prompt += `Answer: ${example.output}\n\n`;
    }

    prompt += `Now answer this question:\nQuestion: ${userQuestion}\nAnswer:`;
    return prompt;
}

async function queryModel(question) {
    const apiKey = process.env.FIREWORKS_API_KEY;
    const modelId = "accounts/mmsquare/models/ft-mdecuh2p-7z2lw";
    
    if (!apiKey) {
        return "Error: FIREWORKS_API_KEY not found in environment variables";
    }
    
    const headers = {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
    };

    // Create few-shot prompt
    const prompt = createFewShotPrompt(question);

    const data = {
        "model": modelId,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    };

    try {
        const response = await axios.post(
            "https://api.fireworks.ai/inference/v1/chat/completions",
            data,
            { headers }
        );

        return response.data.choices[0].message.content;
    } catch (error) {
        if (error.response) {
            return `Error: ${error.response.status} - ${error.response.data}`;
        } else {
            return `Error: ${error.message}`;
        }
    }
}

exports.handler = async function(event, context) {
    // Handle CORS
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    };
    
    // Handle preflight requests
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }
    
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({error: 'Method not allowed'})
        };
    }
    
    try {
        // Parse request body
        const body = JSON.parse(event.body);
        const question = body.question || '';
        
        if (!question) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({error: 'No question provided'})
            };
        }
        
        // Get AI response
        const answer = await queryModel(question);
        
        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({answer})
        };
        
    } catch (error) {
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({error: error.message})
        };
    }
}; 