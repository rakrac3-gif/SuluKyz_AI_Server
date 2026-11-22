
import os
import json
import urllib.request
import urllib.error
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({"status": "SuluKyz server running"})

@app.post("/chat")
def chat():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY is missing"}), 503

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Message is empty"}), 400

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        "models/gemini-2.5-flash:generateContent"
    )

    payload = {
        "systemInstruction": {
            "parts": [{"text": (
                "You are Сулу Кыз, a friendly voice assistant. "
                "Reply naturally in the user's language: "
                "Kyrgyz, Russian or English. "
                "Keep answers concise and helpful."
            )}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": message}]}
        ],
        "generationConfig": {"maxOutputTokens": 1024}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.load(response)

        parts = result["candidates"][0]["content"]["parts"]
        reply = "".join(p.get("text", "") for p in parts).strip()

        if not reply:
            return jsonify({"error": "Empty Gemini response"}), 502

        return jsonify({"reply": reply})

    except urllib.error.HTTPError as e:
        print("Gemini HTTP error:", e.code, e.read().decode("utf-8", "replace"))
        return jsonify({"error": "Gemini request failed", "code": e.code}), 502
    except Exception as e:
        print("Gemini error:", str(e))
        return jsonify({"error": "Gemini connection failed"}), 502
