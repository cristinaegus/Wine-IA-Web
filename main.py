
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from langchain_core.messages import HumanMessage
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def load_model():
    """Carga el modelo actualizado de Groq"""
    from langchain_groq import ChatGroq
    import os
    
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY no configurada")
    
    # Usar modelo actualizado y soportado
    return ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",  # Modelo actualizado
        temperature=0.7
    )

model = load_model()

app = FastAPI()

def get_index_html():
    return FileResponse("indexchatbot.html")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    return get_index_html()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    response = model.invoke([HumanMessage(content=user_message)])
    return {"reply": response.content}

# Servir archivos estáticos (por ejemplo, CSS) en /static
from pathlib import Path
static_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=static_dir), name="static")
static_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Para ejecutar: uvicorn main:app --reload
