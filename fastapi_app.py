from fastapi import FastAPI
from pydantic import BaseModel
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

# Inicializar modelo Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
try:
    chat = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3-8b-8192")
except Exception as e:
    print(f"Error inicializando ChatGroq: {e}")
    chat = None

@app.post("/api/fastapi-chatbot")
def fastapi_chatbot(req: ChatRequest):
    if chat is None:
        return {"response": "Error: El modelo Groq no se ha inicializado correctamente."}
    try:
        from langchain_core.messages import HumanMessage
        prompt = f"Usuario: {req.message}\nResponde de forma útil, breve y profesional."
        response = chat.invoke([HumanMessage(content=prompt)])
        return {"response": str(getattr(response, 'content', response))}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
