# 🍷 Sommelier Inteligente - Guía Rápida

## 🚀 Inicio Rápido

### 1. Activar Entorno Virtual

```bash
wine_env\Scripts\activate
```

### 2. Verificar y Ejecutar

```bash
# Opción 1: Script automático (RECOMENDADO)
python deploy_sommelier.py

# Opción 2: Ejecución directa
python app_sommelier.py
```

### 3. Abrir en Navegador

```
http://127.0.0.1:5000
```

## 🎯 Uso del Sistema

### Búsqueda Básica

1. **Presupuesto**: Establece rango de precios (€)
2. **Rating mínimo**: Calidad deseada (3.8 - 5.0)
3. **Ocasión**: Selecciona el contexto de uso
4. **Preferencias**: Estilo de vino preferido

### Filtros Avanzados

- **API REST**: `/api/recomendar?precio_min=15&precio_max=35&rating_min=4.1`
- **JSON Response**: Datos estructurados para integraciones

## 📁 Archivos Importantes

| Archivo                      | Descripción                     |
| ---------------------------- | ------------------------------- |
| `app_sommelier.py`           | Aplicación Flask principal      |
| `config_sommelier.py`        | Configuración centralizada      |
| `deploy_sommelier.py`        | Script de despliegue automático |
| `templates/sommelier_*.html` | Interfaz web                    |
| `static/style/sommelier.css` | Estilos personalizados          |

## 🔧 Resolución de Problemas

### Error: "No se encontraron archivos CSV"

```bash
# Ejecutar scraping para generar datos
python datos.py
```

### Error: "Modelo no encontrado"

```bash
# Entrenar modelo desde notebook
jupyter notebook spanish_wine_dataset_classification.ipynb
```

### Error: "Puerto 5000 ocupado"

```python
# Cambiar puerto en config_sommelier.py
PORT = 8080
```

## 🌐 URLs del Sistema

- **Inicio**: `http://127.0.0.1:5001/`
- **Información**: `http://127.0.0.1:5001/about`
- **API Vinos**: `http://127.0.0.1:5001/api/vinos`
- **API Recomendaciones**: `http://127.0.0.1:5001/api/recomendar`

## 💡 Consejos de Uso

### Para Principiantes

- Presupuesto: €15-25
- Rating: 4.0+
- Ocasión: General

### Para Ocasiones Especiales

- Presupuesto: €30-50
- Rating: 4.15+
- Ocasión: Romántica/Especial

### Para Regalos

- Presupuesto: €25-40
- Rating: 4.1+
- Ocasión: Regalo

## 📊 Datos del Sistema

- **Fuente**: Vivino (scraping automatizado)
- **Algoritmo**: Random Forest
- **Precisión**: 100% en conjunto de prueba
- **Variables**: 10 características por vino
- **Actualización**: Manual (ejecutar scraping)

## 🔒 Seguridad

- Servidor solo accesible localmente por defecto
- No se almacenan datos de usuario
- Configuración en archivos locales
- Sin autenticación requerida

---

**¿Necesitas ayuda?** Revisa `README_SOMMELIER.md` para documentación completa.
