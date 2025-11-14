import os
from flask import Flask, request, jsonify
import requests
# Cargar variables de entorno desde .env automáticamente
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Inicializar modelo Groq con un modelo actualizado y soportado
from langchain_groq import ChatGroq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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").strip()

# Modelos actualizados disponibles en Groq:
# - llama-3.3-70b-versatile (recomendado, más potente)
# - llama-3.1-8b-instant (más rápido)
# - mixtral-8x7b-32768 (alternativa)

try:
    chat = ChatGroq(
        api_key=GROQ_API_KEY, 
        model_name="llama-3.3-70b-versatile",  # Modelo actualizado
        temperature=0.7
    )
    print("✓ Modelo Groq inicializado correctamente: llama-3.3-70b-versatile")
except Exception as e:
    print(f"❌ Error inicializando ChatGroq: {e}")
    chat = None




## Elimina la lógica de búsqueda Grq, solo deja el chatbot
@app.route('/chat', methods=['POST'])
def chatbot_endpoint():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Mensaje vacío'}), 400
    if chat is None:
        return jsonify({'response': 'Error: El modelo Groq no se ha inicializado correctamente.'}), 500
    try:
        from langchain_core.messages import HumanMessage
        prompt = f"Usuario: {user_message}\nResponde de forma útil, breve y profesional."
        response = chat.invoke([HumanMessage(content=prompt)])
        return jsonify({'response': str(getattr(response, 'content', response))})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

## Elimina la simulación de endpoint Grq, ya no existe

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 CHATBOT GROQ - Servidor iniciado")
    print("="*60)
    print(f"✓ Modelo: llama-3.3-70b-versatile")
    print(f"✓ Endpoint: POST http://localhost:5000/chat")
    print(f"✓ Formato: {{'message': 'tu pregunta aquí'}}")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)
