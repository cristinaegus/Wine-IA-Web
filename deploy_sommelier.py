#!/usr/bin/env python3
"""
Script de Despliegue del Sommelier Inteligente
Verifica dependencias, archivos y configuración antes de ejecutar
"""

import sys
import os
import subprocess
from pathlib import Path
from config_sommelier import get_config

def verificar_python():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    dependencias = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'pickle', 'pathlib'
    ]
    
    faltantes = []
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            faltantes.append(dep)
            print(f"❌ {dep} - NO INSTALADO")
    
    if faltantes:
        print(f"\n📦 Instala las dependencias faltantes:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    
    return True

def verificar_estructura_proyecto():
    """Verifica la estructura del proyecto"""
    config = get_config('development')
    
    # Verificar directorios
    directorios = [
        config.TEMPLATES_DIR,
        config.STATIC_DIR / 'style',
        config.DATA_DIR,
        config.MODELS_DIR
    ]
    
    for directorio in directorios:
        if directorio.exists():
            print(f"✅ {directorio}")
        else:
            print(f"❌ {directorio} - NO EXISTE")
            return False
    
    # Verificar archivos críticos
    archivos_criticos = [
        'app_sommelier.py',
        'config_sommelier.py',
        'templates/sommelier_index.html',
        'templates/sommelier_about.html',
        'static/style/sommelier.css'
    ]
    
    for archivo in archivos_criticos:
        ruta = Path(archivo)
        if ruta.exists():
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - NO EXISTE")
            return False
    
    return True

def verificar_datos_y_modelo():
    """Verifica archivos de datos y modelo"""
    config = get_config('development')
    
    # Verificar archivos faltantes usando la configuración
    archivos_faltantes = config.verificar_archivos_requeridos()
    
    if archivos_faltantes:
        print("\n❌ ARCHIVOS FALTANTES:")
        for archivo in archivos_faltantes:
            print(f"   - {archivo}")
        
        print("\n📋 INSTRUCCIONES:")
        print("1. Ejecuta el notebook 'spanish_wine_dataset_classification.ipynb'")
        print("2. Asegúrate de que genere los archivos del modelo en 'modelos generados/'")
        print("3. Ejecuta el scraping para generar datos CSV actualizados")
        
        return False
    
    # Mostrar información del dataset
    info_dataset = config.obtener_info_dataset()
    if info_dataset:
        print(f"\n📊 INFORMACIÓN DEL DATASET:")
        print(f"   Archivo: {info_dataset['archivo']}")
        print(f"   Total vinos: {info_dataset['total_vinos']}")
        print(f"   Rango precios: €{info_dataset['precio_min']:.2f} - €{info_dataset['precio_max']:.2f}")
        print(f"   Rango ratings: {info_dataset['rating_min']:.2f} - {info_dataset['rating_max']:.2f}")
    
    return True

def mostrar_resumen_configuracion():
    """Muestra resumen de la configuración"""
    config = get_config('development')
    
    print(f"\n⚙️ CONFIGURACIÓN:")
    print(f"   Host: {config.HOST}")
    print(f"   Puerto: {config.PORT}")
    print(f"   Debug: {config.DEBUG}")
    print(f"   Recomendaciones por defecto: {config.DEFAULT_RECOMMENDATIONS}")

def ejecutar_aplicacion():
    """Ejecuta la aplicación Flask"""
    print("\n🚀 INICIANDO SOMMELIER INTELIGENTE...")
    print("   Presiona Ctrl+C para detener el servidor")
    
    try:
        # Ejecutar la aplicación
        subprocess.run([sys.executable, 'app_sommelier.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error ejecutando la aplicación: {e}")
        return False
    
    return True

def main():
    """Función principal del script de despliegue"""
    print("🍷 SOMMELIER INTELIGENTE - SCRIPT DE DESPLIEGUE")
    print("=" * 50)
    
    # Verificaciones paso a paso
    verificaciones = [
        ("Versión de Python", verificar_python),
        ("Dependencias instaladas", verificar_dependencias),
        ("Estructura del proyecto", verificar_estructura_proyecto),
        ("Datos y modelo", verificar_datos_y_modelo)
    ]
    
    for nombre, funcion in verificaciones:
        print(f"\n🔍 Verificando: {nombre}")
        if not funcion():
            print(f"\n❌ FALLO EN: {nombre}")
            print("   Resuelve los problemas antes de continuar")
            return False
    
    # Mostrar configuración
    mostrar_resumen_configuracion()
    
    # Confirmación para ejecutar
    print("\n✅ TODAS LAS VERIFICACIONES COMPLETADAS")
    respuesta = input("\n¿Ejecutar la aplicación? (s/N): ").strip().lower()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        return ejecutar_aplicacion()
    else:
        print("👋 Despliegue cancelado por el usuario")
        return True

if __name__ == "__main__":
    exit(0 if main() else 1)
