# Configuración del Sommelier Inteligente
import os
import pickle
from pathlib import Path

class Config:
    """Configuración centralizada para el Sommelier Inteligente"""
    
    # Rutas del proyecto
    BASE_DIR = Path(__file__).parent
    STATIC_DIR = BASE_DIR / 'static'
    TEMPLATES_DIR = BASE_DIR / 'templates'
    DATA_DIR = BASE_DIR / 'datos_scraping'
    MODELS_DIR = BASE_DIR / 'modelos generados'
    
    # Configuración Flask
    SECRET_KEY = 'sommelier-wine-recommendation-2025'
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5001
    
    # Configuración de la base de datos PostgreSQL Neon
    DATABASE_URL = 'postgresql://FlaskEjercicioConnect_owner:npg_4SBm3VXpFwIE@ep-floral-frost-a2tieivc-pooler.eu-central-1.aws.neon.tech/FlaskEjercicioConnect?sslmode=require&channel_binding=require'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Archivos de datos
    CSV_PATTERN_1 = 'vivino_scraping_completo_*.csv'
    CSV_PATTERN_2 = 'resumen_scraping_completo_*.csv'
    CSV_FILES_1 = list(DATA_DIR.glob(CSV_PATTERN_1)) if DATA_DIR.exists() else []
    CSV_FILES_2 = list(DATA_DIR.glob(CSV_PATTERN_2)) if DATA_DIR.exists() else []
    CSV_FILES = CSV_FILES_1 + CSV_FILES_2  # Combinar ambos tipos de archivos
    LATEST_CSV = max(CSV_FILES, key=os.path.getctime) if CSV_FILES else None
    
    # Archivos del modelo actualizado (buscar en static primero, luego directorios alternativos)
    MODEL_FILE = STATIC_DIR / 'wine_model.pkl' if (STATIC_DIR / 'wine_model.pkl').exists() else (BASE_DIR / 'modelo_random_forest_vivino.pkl' if (BASE_DIR / 'modelo_random_forest_vivino.pkl').exists() else MODELS_DIR / 'modelo_random_forest_vivino.pkl')
    SCALER_FILE = STATIC_DIR / 'wine_scaler.pkl' if (STATIC_DIR / 'wine_scaler.pkl').exists() else (BASE_DIR / 'scaler_vivino.pkl' if (BASE_DIR / 'scaler_vivino.pkl').exists() else MODELS_DIR / 'scaler_vivino.pkl')
    MODEL_INFO_FILE = STATIC_DIR / 'model_info.pkl' if (STATIC_DIR / 'model_info.pkl').exists() else None
    ENCODER_FILE = BASE_DIR / 'label_encoder_vivino.pkl' if (BASE_DIR / 'label_encoder_vivino.pkl').exists() else MODELS_DIR / 'label_encoder_vivino.pkl'
    
    # Configuración de recomendaciones
    DEFAULT_RECOMMENDATIONS = 6
    MAX_RECOMMENDATIONS = 12
    MIN_RATING = 3.8
    MAX_RATING = 5.0
    MIN_PRICE = 8.0
    MAX_PRICE = 100.0
    
    # Categorías de ocasiones
    OCASIONES = {
        'general': 'Uso general',
        'romantica': 'Cena romántica',
        'fiesta': 'Fiesta o celebración',
        'regalo': 'Para regalar',
        'especial': 'Ocasión especial'
    }
    
    # Preferencias de gusto
    GUSTOS = {
        'equilibrado': 'Equilibrado',
        'premium': 'Premium',
        'economico': 'Económico',
        'popular': 'Popular'
    }
    
    # Pesos para el algoritmo de recomendación
    FEATURE_WEIGHTS = {
        'rating': 0.35,
        'num_reviews': 0.20,
        'posicion': 0.15,
        'precio': 0.10,
        'popularidad': 0.10,
        'valor': 0.10
    }
    
    @classmethod
    def verificar_archivos_requeridos(cls):
        """Verifica que todos los archivos necesarios existan"""
        archivos_faltantes = []
        
        # Verificar CSV de datos
        if not cls.LATEST_CSV or not cls.LATEST_CSV.exists():
            archivos_faltantes.append(f"CSV de datos ({cls.CSV_PATTERN})")
        
        # Verificar archivos del modelo
        archivos_modelo = [
            (cls.MODEL_FILE, "Modelo Random Forest"),
            (cls.SCALER_FILE, "Scaler"),
            (cls.ENCODER_FILE, "Label Encoder")
        ]
        
        for archivo, nombre in archivos_modelo:
            if not archivo.exists():
                archivos_faltantes.append(f"{nombre} ({archivo.name})")
        
        return archivos_faltantes
    
    @classmethod
    def cargar_modelo(cls):
        """Carga el modelo y sus componentes"""
        try:
            import joblib
            
            # Cargar modelo principal
            modelo = joblib.load(cls.MODEL_FILE)
            
            # Cargar scaler
            scaler = joblib.load(cls.SCALER_FILE)
            
            # Cargar información del modelo si está disponible
            model_info = None
            if cls.MODEL_INFO_FILE and cls.MODEL_INFO_FILE.exists():
                try:
                    model_info = joblib.load(cls.MODEL_INFO_FILE)
                except:
                    model_info = None
            
            # Cargar encoder si existe (compatibilidad con modelos antiguos)
            encoder = None
            if cls.ENCODER_FILE.exists():
                try:
                    with open(cls.ENCODER_FILE, 'rb') as f:
                        encoder = pickle.load(f)
                except:
                    encoder = None
            
            print(f"✅ Modelo cargado exitosamente desde {cls.MODEL_FILE}")
            if model_info:
                print(f"📊 Versión del modelo: {model_info.get('version', 'desconocida')}")
                print(f"📅 Timestamp: {model_info.get('timestamp', 'desconocido')}")
                print(f"🏷️ Clases disponibles: {model_info.get('clases_calidad', [])}")
            
            return modelo, scaler, encoder, model_info
        
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return None, None, None, None
    
    @classmethod
    def obtener_info_dataset(cls):
        """Obtiene información sobre el dataset actual"""
        if not cls.LATEST_CSV:
            return None
        
        import pandas as pd
        try:
            df = pd.read_csv(cls.LATEST_CSV)
            return {
                'archivo': cls.LATEST_CSV.name,
                'total_vinos': len(df),
                'precio_min': df['precio_euros'].min(),
                'precio_max': df['precio_euros'].max(),
                'rating_min': df['rating'].min(),
                'rating_max': df['rating'].max(),
                'columnas': list(df.columns)
            }
        except Exception:
            return None

# Configuración específica para desarrollo
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

# Configuración específica para producción
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    HOST = '0.0.0.0'

# Configuración específica para testing
class TestingConfig(Config):
    DEBUG = True
    TESTING = True

# Selección de configuración basada en variable de entorno
config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config(env='development'):
    """Obtiene la configuración según el entorno"""
    return config_mapping.get(env, DevelopmentConfig)
