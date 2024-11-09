from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/procesar_mensaje', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    # Aquí procesas `user_input` con tu IA y generas `bot_reply`
    bot_reply = f"Respuesta generada para: {user_input}"  # Ejemplo básico de respuesta
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
