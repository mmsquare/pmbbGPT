#!/usr/bin/env node
/**
 * update-jsonl.js <pretty.json> <output.jsonl>
 * Converts a human-readable JSON array of chat objects (each with `messages`)
 * into a strict JSONL file where each line is one JSON object.
 * If <output.jsonl> is omitted, writes alongside the input with .jsonl suffix.
 */
const fs = require('fs');
const path = require('path');

const [,, inPath, outPathArg] = process.argv;
if (!inPath) {
  console.error('Usage: node update-jsonl.js <pretty.json> [output.jsonl]');
  process.exit(1);
}
const outPath = outPathArg || path.join(path.dirname(inPath), path.basename(inPath, path.extname(inPath)) + '.jsonl');

try {
  const arr = JSON.parse(fs.readFileSync(inPath, 'utf8'));
  if (!Array.isArray(arr)) throw new Error('Input must be a JSON array');
  const lines = arr.map(obj => JSON.stringify(obj));
  fs.writeFileSync(outPath, lines.join('\n') + '\n');
  console.log(`✅ Wrote ${lines.length} lines to ${outPath}`);
} catch (e) {
  console.error('❌ Error:', e.message);
  process.exit(1);
} 