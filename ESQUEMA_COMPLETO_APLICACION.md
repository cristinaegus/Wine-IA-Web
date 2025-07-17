# 🍷 ESQUEMA COMPLETO - WINE IA WEB APPLICATION

```
Wine-IA-Web/                                    🍷 APLICACIÓN PRINCIPAL
├─ 📄 README.md                                 Documentación principal del proyecto
├─ 📄 requirements.txt                          Dependencias Python
├─ 📄 .gitignore                               Control de versiones
├─ 📄 .hintrc                                  Configuración del editor
│
├─ 🚀 APLICACIÓN PRINCIPAL
│   ├─ 📄 app_sommelier.py                     🎯 APP FLASK PRINCIPAL - Servidor web
│   ├─ 📄 config_sommelier.py                  ⚙️ Configuración centralizada
│   ├─ 📄 models.py                           🗃️ Modelos de base de datos (SQLAlchemy)
│   ├─ 📄 run_sommelier.py                    🏃 Script de ejecución
│   └─ 📄 datos.py                            📊 Procesamiento de datos
│
├─ 🌐 FRONTEND (Templates & Static)
│   ├─ 📁 templates/                          🎨 PLANTILLAS HTML
│   │   ├─ 📄 home.html                       🏠 Página principal (landing)
│   │   ├─ 📄 sommelier_index.html            🍷 Interfaz del Sommelier IA
│   │   ├─ 📄 sommelier_about.html            ℹ️ Información técnica
│   │   ├─ 📄 login.html                      🔐 Página de login
│   │   └─ 📄 register.html                   📝 Página de registro
│   │
│   └─ 📁 static/                             🎨 RECURSOS ESTÁTICOS
│       ├─ 📁 style/                          🎨 Hojas de estilo CSS
│       │   ├─ 📄 sommelier.css               🍷 Estilos del Sommelier
│       │   ├─ 📄 wine_about.css              ℹ️ Estilos página "Acerca de"
│       │   └─ 📄 wine_index.css              🏠 Estilos página principal
│       │
│       ├─ 📁 images/                         🖼️ Imágenes de la aplicación
│       │   ├─ 🖼️ gardenWineDrinkers.jpg      👥 Imagen social/jardín
│       │   └─ 🖼️ womanDrinkingWine.jpg       👩 Imagen degustación
│       │
│       └─ 🤖 MODELOS EN PRODUCCIÓN          🎯 Modelos activos
│           ├─ 📄 wine_model.pkl              🧠 Modelo Random Forest
│           ├─ 📄 wine_scaler.pkl             📏 Escalador de características
│           ├─ 📄 model_info.pkl              📊 Metadatos del modelo
│           └─ 📄 *_completo_*.pkl            📦 Versiones con timestamp
│
├─ 🤖 MACHINE LEARNING (Organizado)
│   └─ 📁 models/                             🧠 INTELIGENCIA ARTIFICIAL
│       ├─ 📄 README.md                       📖 Documentación técnica completa
│       │
│       ├─ 📁 training_scripts/               🏋️‍♂️ ENTRENAMIENTO
│       │   ├─ 📄 entrenar_modelo_completo.py 🎯 Script principal (464 vinos)
│       │   ├─ 📄 entrenar_modelo_vivino.py   🍷 Entrenamiento específico Vivino
│       │   └─ 📄 train_wine_model.py         📚 Script base de entrenamiento
│       │
│       ├─ 📁 trained_models/                 🎓 MODELOS ENTRENADOS
│       │   ├─ 📄 wine_model.pkl              🧠 Modelo principal (copia)
│       │   ├─ 📄 wine_scaler.pkl             📏 Escalador (copia)
│       │   ├─ 📄 model_info.pkl              📊 Metadatos (copia)
│       │   └─ 📄 *_completo_*.pkl            📦 Historial de versiones
│       │
│       └─ 📁 testing_scripts/                🧪 PRUEBAS Y VALIDACIÓN
│           └─ 📄 probar_modelo.py            ✅ Validación del modelo
│
├─ 🕷️ WEB SCRAPING (Scripts de extracción)
│   ├─ 📄 vivino_scraper_multipagina.py       🌐 Scraper multipágina
│   ├─ 📄 vivino_scraper_mejorado.py          ⚡ Scraper optimizado
│   ├─ 📄 vivino_scraper_diversificado.py     🎯 Scraper diversificado
│   ├─ 📄 vivino_scraper_avanzado.py          🚀 Scraper avanzado
│   ├─ 📄 analizar_scraping_completo.py       📊 Análisis de datos extraídos
│   ├─ 📄 descargar_chromedriver.py           🔧 Utilidad para ChromeDriver
│   └─ 📄 chromedriver.exe                    🌐 Driver para Selenium
│
├─ 📊 DATOS (Datasets y CSVs)
│   └─ 📁 datos_scraping/                     📈 DATASETS DE VINOS
│       ├─ 📄 Bases Proyecto.md               📋 Documentación de datos
│       ├─ 📄 resumen_scraping_completo_20250717_085859.csv  🎯 DATASET ACTUAL (464 vinos)
│       ├─ 📄 resumen_scraping_completo_20250716_130237.csv  📦 Versión anterior
│       ├─ 📄 vivino_scraping_completo_*.csv  🍷 Datasets de Vivino
│       ├─ 📄 vivino_multipagina_*.csv        🌐 Datos multipágina
│       ├─ 📄 vivino_diversificado_*.csv      🎯 Datos diversificados
│       └─ 📄 vivino_historico_*.csv          📚 Datos históricos
│
├─ 🔧 DEPLOYMENT & CONFIGURACIÓN
│   ├─ 📄 deploy_sommelier.py                🚀 Script de despliegue
│   ├─ 📄 modelo_random_forest_vivino.pkl    🧠 Modelo legacy (raíz)
│   ├─ 📄 scaler_vivino.pkl                  📏 Escalador legacy (raíz)
│   └─ 📄 label_encoder_vivino.pkl           🏷️ Codificador legacy (raíz)
│
├─ 📚 DOCUMENTACIÓN
│   ├─ 📄 GUIA_CONFIGURACION.md              📋 Guía de configuración general
│   ├─ 📄 GUIA_CONFIGURACION_WEB.md          🌐 Guía específica web
│   ├─ 📄 GUIA_RAPIDA_SOMMELIER.md           ⚡ Guía rápida Sommelier
│   ├─ 📄 README_SOMMELIER.md                🍷 Documentación del Sommelier
│   ├─ 📄 PUERTOS_APLICACIONES.md            🔌 Configuración de puertos
│   ├─ 📄 RESUMEN_SCRAPING_VIVINO.md         🕷️ Resumen del scraping
│   ├─ 📄 Resumen_Wine_Classification_Ensemble.md  🤖 Resumen ML
│   └─ 📄 PreparacionNotebook.md             📓 Preparación de notebooks
│
├─ 📓 JUPYTER NOTEBOOKS (Análisis y desarrollo)
│   ├─ 📄 spanish_wine_dataset_classification.ipynb  🇪🇸 Análisis dataset español
│   └─ 📄 Wine_multiclass_classification__97_5_accuracy.ipynb  🎯 Modelo 97.5% accuracy
│
├─ 🐍 ENTORNO VIRTUAL
│   └─ 📁 wine_env/                           🐍 ENTORNO PYTHON AISLADO
│       ├─ 📁 Scripts/                        🔧 Scripts de activación
│       ├─ 📁 Lib/                           📚 Librerías instaladas
│       └─ 📄 pyvenv.cfg                     ⚙️ Configuración del entorno
│
├─ 🗂️ CONTROL DE VERSIONES
│   ├─ 📁 .git/                              📝 Repositorio Git
│   └─ 📁 __pycache__/                       🔄 Cache de Python
│
└─ 🎯 PUNTOS DE ENTRADA PRINCIPALES
    ├─ 🌐 http://127.0.0.1:5001/             ➜ home.html (Landing page)
    ├─ 🍷 http://127.0.0.1:5001/sommelier    ➜ Sommelier IA
    ├─ ℹ️ http://127.0.0.1:5001/about        ➜ Información técnica
    ├─ 🔐 http://127.0.0.1:5001/login        ➜ Iniciar sesión
    └─ 📝 http://127.0.0.1:5001/register     ➜ Registro de usuarios

```

## 🔍 DETALLES TÉCNICOS

### 🏗️ Arquitectura de la aplicación

```
📱 Frontend (HTML/CSS/JS)
    ↕️
🌐 Flask Web Server (app_sommelier.py)
    ↕️
🗃️ PostgreSQL Database (Neon)
    ↕️
🤖 ML Pipeline (Random Forest + Scaler)
    ↕️
📊 Vivino Dataset (464 vinos españoles)
```

### 🎯 Flujo de usuario

```
1. 🏠 Landing (/) → home.html
2. 📝 Registro → PostgreSQL
3. 🔐 Login → Sesión autenticada
4. 🍷 Sommelier (/sommelier) → ML Predictions
5. ℹ️ Información (/about) → Detalles técnicos
```

### 🤖 Pipeline de Machine Learning

```
📊 Datos (CSV) → 🧹 Limpieza → 🔧 Features → 🏋️‍♂️ Entrenamiento → 💾 Modelo (.pkl) → 🚀 Producción
```

### 🔗 Dependencias principales

- **Flask 3.1.1** - Framework web
- **scikit-learn 1.7.0** - Machine Learning
- **pandas 2.3.1** - Manipulación de datos
- **PostgreSQL** - Base de datos (Neon)
- **Bootstrap 5** - Frontend framework
- **Selenium** - Web scraping

### 📊 Estado actual

- **✅ Aplicación**: Funcional en puerto 5001
- **✅ Modelo**: 100% accuracy, 464 vinos, 15 features
- **✅ Base de datos**: PostgreSQL conectada
- **✅ Frontend**: Responsive con imágenes
- **✅ Organización**: Estructura modular y documentada

---

_Última actualización: 17 de julio de 2025_
_Wine IA - Sistema Inteligente de Recomendación de Vinos_
