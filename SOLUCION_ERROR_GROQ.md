# 🔧 SOLUCIÓN: Error de Conexión con Modelo Groq en Fly.io

## 📋 Problema Identificado

El modelo `llama3-8b-8192` ha sido **descontinuado** por Groq.

**Error:** 
```
Error code: 400 - {'error': {'message': 'The model `llama3-8b-8192` has been decommissioned and is no longer supported.'}}
```

## ✅ Solución Aplicada

### Archivos Actualizados:

1. **`chatbot.py`** ✅
   - Modelo actualizado a: `llama-3.3-70b-versatile`
   - API key limpiada (sin espacios)
   - Ruta Flask registrada: `/chat`
   - Servidor configurado correctamente

2. **`main.py`** ✅
   - Función `load_model()` actualizada
   - Ahora usa `langchain_groq.ChatGroq` directamente
   - Modelo: `llama-3.3-70b-versatile`

3. **`test_groq_chatbot.py`** ✅
   - Script de prueba actualizado con nuevo modelo

## 🚀 Pasos para Desplegar en Fly.io

### Opción A: Usando el script automatizado (Recomendado)

```powershell
.\actualizar_flyio.ps1
```

Este script:
- ✓ Verifica instalación de Fly.io CLI
- ✓ Comprueba autenticación
- ✓ Actualiza GROQ_API_KEY desde .env
- ✓ Despliega la aplicación

### Opción B: Manualmente

```powershell
# 1. Asegurarse de tener la API key configurada
flyctl secrets set GROQ_API_KEY=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

# 2. Verificar secretos configurados
flyctl secrets list

# 3. Desplegar
flyctl deploy

# 4. Verificar logs
flyctl logs
```

## 🧪 Probar Localmente Antes de Desplegar

```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Probar el modelo Groq
python test_groq_chatbot.py

# 3. Ejecutar la aplicación localmente
python app_sommelier.py

# 4. Probar el endpoint (en otra terminal)
curl -X POST http://localhost:5001/api/chatbot -H "Content-Type: application/json" -d '{\"message\": \"Hola\"}'
```

## 📊 Modelos Groq Disponibles (Noviembre 2025)

| Modelo | Descripción | Uso Recomendado |
|--------|-------------|-----------------|
| **llama-3.3-70b-versatile** ⭐ | Más potente y versátil | **Producción (ACTUAL)** |
| llama-3.1-8b-instant | Más rápido, menos recursos | Desarrollo/testing |
| mixtral-8x7b-32768 | Contexto grande (32k tokens) | Conversaciones largas |

## ❓ Solución de Problemas

### Si sigue dando error de conexión:

1. **Verificar API Key:**
   ```powershell
   flyctl secrets list
   ```
   Debe aparecer `GROQ_API_KEY` en la lista.

2. **Verificar logs de despliegue:**
   ```powershell
   flyctl logs
   ```

3. **Probar API Key localmente:**
   ```powershell
   python test_groq_chatbot.py
   ```

4. **Verificar que el modelo se inicializa:**
   En los logs debe aparecer:
   ```
   ✓ Modelo Groq inicializado correctamente: llama-3.3-70b-versatile
   ```

### Si la API Key no funciona:

1. Verificar en la consola de Groq: https://console.groq.com/keys
2. Generar una nueva API key si es necesario
3. Actualizar en Fly.io:
   ```powershell
   flyctl secrets set GROQ_API_KEY=nueva_api_key
   ```

## 📝 Checklist de Verificación

- [x] ✅ Modelo actualizado en `chatbot.py`
- [x] ✅ Modelo actualizado en `main.py`
- [ ] ⏳ API Key configurada en Fly.io
- [ ] ⏳ Aplicación desplegada
- [ ] ⏳ Logs verificados sin errores
- [ ] ⏳ Endpoint de chatbot probado

## 🔗 Enlaces Útiles

- [Documentación de Groq](https://console.groq.com/docs/deprecations)
- [Modelos disponibles en Groq](https://console.groq.com/docs/models)
- [Fly.io Secrets](https://fly.io/docs/reference/secrets/)

---

**Fecha de actualización:** 14 de noviembre de 2025
