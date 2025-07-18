import os
from flask import request, jsonify
from langchain_community.retrievers import TavilySearchAPIRetriever

# Obtener la API key de Tavily
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "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")

def get_tavily_retriever():
    return TavilySearchAPIRetriever(api_key=TAVILY_API_KEY)

def tavily_search_endpoint():
    try:
        data = request.get_json()
        query = data.get('query')
        if not query:
            return jsonify({'error': 'Falta el parámetro query'}), 400
        retriever = get_tavily_retriever()
        docs = retriever.get_relevant_documents(query)
        results = [doc.page_content for doc in docs]
        return jsonify({'results': results})
    except Exception as e:
        # Mostrar el error real para depuración
        return jsonify({'error': f'Error de conexión o API: {str(e)}'}), 500

def chatbot_endpoint(chat):
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'response': 'Mensaje vacío'}), 400
    try:
        from langchain_core.messages import HumanMessage
        retriever = get_tavily_retriever()
        docs = retriever.get_relevant_documents(user_message)
        web_context = "\n".join([doc.page_content for doc in docs])
        prompt = f"""
        Usuario: {user_message}
        \nInformación web relevante:
        {web_context}
        \nResponde de forma útil, breve y profesional usando la información web si es relevante.
        """
        response = chat.invoke([HumanMessage(content=prompt)])
        return jsonify({'response': str(getattr(response, 'content', response))})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500
