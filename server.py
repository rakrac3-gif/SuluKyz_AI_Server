import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

@app.post("/chat")
def chat():
    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({"error": "API key not configured"}), 500

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are Сулу Кыз, a friendly female voice assistant. "
                "Reply naturally in the user's language: Kyrgyz, "
                "Russian or English. Keep answers concise."
            ),
            input=message
        )
        return jsonify({"reply": response.output_text})
    except Exception:
        return jsonify({"error": "AI request failed"}), 502

@app.get("/")
def home():
    return jsonify({"status": "SuluKyz server running"})
  
