"""
Script para probar si el modelo Groq funciona correctamente
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_groq_connection():
    """Prueba la conexión con Groq"""
    from langchain_groq import ChatGroq
    from langchain_core.messages import HumanMessage
    
    # Obtener API key
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
    
    if not GROQ_API_KEY:
        print("❌ ERROR: No se encontró GROQ_API_KEY en las variables de entorno")
        return False
    
    print(f"✓ API Key encontrada (longitud: {len(GROQ_API_KEY)})")
    
    try:
        # Inicializar el modelo
        print("\n🔄 Inicializando ChatGroq con modelo llama-3.3-70b-versatile...")
        chat = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        print("✓ Modelo inicializado correctamente")
        
        # Hacer una prueba simple
        print("\n🔄 Enviando mensaje de prueba...")
        test_message = "Hola, ¿puedes confirmar que estás funcionando?"
        response = chat.invoke([HumanMessage(content=test_message)])
        
        print("✓ Respuesta recibida:")
        print(f"  Contenido: {response.content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR al probar Groq: {type(e).__name__}: {str(e)}")
        return False

def check_chatbot_issues():
    """Verifica problemas en chatbot.py"""
    print("\n" + "="*60)
    print("ANÁLISIS DE PROBLEMAS EN chatbot.py")
    print("="*60)
    
    issues = []
    
    # Leer el archivo
    with open("chatbot.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Verificar API key con espacios
    if '"gsk_' in content and ' ").strip()' in content:
        issues.append("⚠️  La API key en el código tiene un espacio al final")
    
    # Verificar si hay ruta Flask registrada
    if '@app.route' not in content:
        issues.append("⚠️  No hay rutas Flask (@app.route) registradas")
    
    # Verificar si el servidor se inicia
    if 'app.run' not in content:
        issues.append("⚠️  No hay código para iniciar el servidor Flask (app.run)")
    
    if issues:
        print("\nProblemas encontrados:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✓ No se encontraron problemas evidentes")
    
    return len(issues) == 0

if __name__ == "__main__":
    print("="*60)
    print("TEST DEL MODELO GROQ EN CHATBOT")
    print("="*60)
    
    # Verificar problemas en el archivo
    check_chatbot_issues()
    
    # Probar conexión con Groq
    print("\n" + "="*60)
    print("PRUEBA DE CONEXIÓN CON GROQ")
    print("="*60 + "\n")
    
    success = test_groq_connection()
    
    print("\n" + "="*60)
    if success:
        print("✅ RESULTADO: El modelo Groq funciona correctamente")
    else:
        print("❌ RESULTADO: Hay problemas con el modelo Groq")
    print("="*60)
