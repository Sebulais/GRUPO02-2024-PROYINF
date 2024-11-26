from flask import request, jsonify, render_template
from app import app
import google.generativeai as genai

# Configurar la API de Gemini
genai.configure(api_key=app.config['GEMINI_API_KEY'])

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/api/chat/", methods=["POST"])
def chat():
    try:
        # Obtener mensaje del usuario
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400

        # Interactuar con el modelo de Gemini
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt=user_message)

        # Respuesta del modelo
        bot_reply = response.text if response.text else "Lo siento, no tengo respuesta."
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
