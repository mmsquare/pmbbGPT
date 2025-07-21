#!/usr/bin/env node

/**
 * Utility script to update training data
 * Usage: node update-training-data.js
 */

const fs = require('fs');
const path = require('path');

// Paths to training data files
const JSON_PATH = './functions/training-data.json';
const JS_PATH = './functions/training-data.js';

function updateTrainingData() {
    try {
        // Read the JSON file
        const jsonData = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
        
        // Generate the JavaScript content
        const jsContent = `// Product Management Training Data for Few-Shot Learning
const TRAINING_DATA = ${JSON.stringify(jsonData, null, 4)};

module.exports = TRAINING_DATA;`;
        
        // Write to the JavaScript file
        fs.writeFileSync(JS_PATH, jsContent);
        
        console.log('✅ Training data updated successfully!');
        console.log(`📊 ${jsonData.length} examples loaded`);
        
        // Show the examples
        console.log('\n📋 Current training examples:');
        jsonData.forEach((example, index) => {
            console.log(`${index + 1}. ${example.input.substring(0, 60)}...`);
        });
        
    } catch (error) {
        console.error('❌ Error updating training data:', error.message);
        process.exit(1);
    }
}

function addExample(input, output) {
    try {
        // Read existing data
        const jsonData = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
        
        // Add new example
        jsonData.push({ input, output });
        
        // Write back to JSON file
        fs.writeFileSync(JSON_PATH, JSON.stringify(jsonData, null, 4));
        
        // Update JavaScript file
        updateTrainingData();
        
        console.log('✅ New example added successfully!');
        
    } catch (error) {
        console.error('❌ Error adding example:', error.message);
        process.exit(1);
    }
}

// Command line interface
const args = process.argv.slice(2);

if (args.length === 0) {
    updateTrainingData();
} else if (args[0] === 'add' && args.length >= 3) {
    const input = args[1];
    const output = args[2];
    addExample(input, output);
} else {
    console.log('Usage:');
    console.log('  node update-training-data.js                    # Update from JSON to JS');
    console.log('  node update-training-data.js add "Q" "A"        # Add new example');
} 