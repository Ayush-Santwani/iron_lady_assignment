import os
import json
from flask import Flask, request, jsonify, render_template
from difflib import get_close_matches

app = Flask(__name__, template_folder='templates')

BASE_DIR = os.path.dirname(__file__)
FAQ_PATH = os.path.join(BASE_DIR, 'faq.json')

# Load FAQs
with open(FAQ_PATH, 'r', encoding='utf-8') as f:
    FAQ = json.load(f)

def find_faq_answer(question: str):
    keys = list(FAQ.keys())
    # exact match (case-insensitive)
    for k in keys:
        if question.strip().lower() == k.strip().lower():
            return FAQ[k], "direct"
    # fuzzy match
    matches = get_close_matches(question, keys, n=1, cutoff=0.6)
    if matches:
        return FAQ[matches[0]], "fuzzy"
    return None, None

@app.route('/')
def index():
    # render chatbot UI
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json() or {}
    question = data.get('question', '')
    if not question:
        return jsonify({"error": "No question provided"})

    answer, match_type = find_faq_answer(question)
    if answer:
        return jsonify({"answer": answer, "match_type": match_type})

    return jsonify({"answer": "Sorry, I couldn't find anything relevant."})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
