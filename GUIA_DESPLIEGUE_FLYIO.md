# Guía rápida para entorno virtual y despliegue en Fly.io

## 1. Crear y activar entorno virtual (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 2. Instalar dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Ejecutar la aplicación localmente

```powershell
python app_sommelier.py
```

O si usas Gunicorn:

```powershell
python -m gunicorn -b 127.0.0.1:5001 app_sommelier:app
```

## 4. Despliegue en Fly.io

### 4.1. Instalar Fly.io CLI

```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

Cierra y abre la terminal, luego verifica:

```powershell
flyctl version
```

### 4.2. Iniciar sesión en Fly.io

```powershell
flyctl auth login
```

### 4.3. Guardar secretos (API keys, claves Flask, etc.)

```powershell
flyctl secrets set SECRET_KEY=tu_clave_segura
flyctl secrets set GROQ_API_KEY=tu_api_key_real
```

### 4.4. Desplegar la aplicación

```powershell
flyctl deploy
```

## 5. Comprobar archivos de modelo en Fly.io

```powershell
flyctl ssh console
ls -l /app/modelos\ generados/
```

## 6. Acceder a la web desplegada

- La URL se muestra al final del deploy (ejemplo: https://wine-ia-web.fly.dev)

---

**Notas:**
- Asegúrate de que los archivos `.pkl` de los modelos estén en el proyecto y no ignorados por `.dockerignore`.
- Repite `flyctl secrets set ...` cada vez que cambies una clave o API key.
- Usa `flyctl deploy` tras cada cambio relevante en el código o dependencias.
