import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="You'll speak in Spanish from now on. You're a specialist AI that helps in the FIA Chile.",
)

history = []

print("FIA IA: Hola, soy la IA de la FIA Chile. ¿En qué puedo ayudarte hoy?")

while True:

    user_input = input("You: ")

    chat_session = model.start_chat(
        history = history
    )

    response = chat_session.send_message("user_input")

    model_response = response.text

    print(model_response)
    print()

    history.append("role": "user", "parts": [user_input])
    history.append("role": "system", "parts": [model_response])

