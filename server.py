
import os
from flask import Flask, request, jsonify
from openai import OpenAI, OpenAIError

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({"status": "SuluKyz server running"})

@app.post("/chat")
def chat():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        return jsonify({
            "error": "OPENAI_API_KEY is missing"
        }), 503

    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Message is empty"}), 400

    try:
        client = OpenAI(api_key=api_key, timeout=30.0)

        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are Сулу Кыз, a friendly AI voice assistant. "
                "Reply in the user's language: Kyrgyz, Russian "
                "or English. Keep answers natural and concise."
            ),
            input=message
        )

        reply = response.output_text.strip()

        if not reply:
            return jsonify({
                "error": "AI returned an empty response"
            }), 502

        return jsonify({"reply": reply})

    except OpenAIError as e:
        app.logger.error(
            "OpenAI request failed: %s", str(e)
        )
        return jsonify({
            "error": "AI request failed",
            "details": str(e)[:300]
        }), 502

    except Exception:
        app.logger.exception("Unexpected server error")
        return jsonify({
            "error": "Internal server error"
        }), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
