#!/usr/bin/env python3
"""
Script para hacer una limpieza más exhaustiva del CSV eliminando registros con NaN en columnas importantes
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def limpiar_csv_exhaustivo():
    """
    Elimina registros con NaN en columnas importantes para obtener un dataset más limpio
    """
    print("🧹 LIMPIEZA EXHAUSTIVA DE VALORES NaN")
    print("=" * 50)
    
    # Buscar el archivo CSV más reciente limpio
    directorio_datos = 'datos_scraping'
    archivo_objetivo = None
    
    for archivo in os.listdir(directorio_datos):
        if archivo.endswith('_sin_nan_criticos.csv'):
            archivo_objetivo = os.path.join(directorio_datos, archivo)
            break
    
    if not archivo_objetivo:
        print("❌ No se encontró archivo con limpieza crítica previa")
        return
    
    print(f"📂 Procesando archivo: {archivo_objetivo}")
    
    # Cargar datos
    try:
        df = pd.read_csv(archivo_objetivo)
        print(f"✅ Archivo cargado: {len(df)} registros totales")
    except Exception as e:
        print(f"❌ Error cargando archivo: {e}")
        return
    
    # Definir columnas importantes para tener un dataset de alta calidad
    columnas_importantes = [
        'precio_eur',          # Esencial para recomendaciones
        'url',                 # Esencial para identificación
        'bodega',              # Importante para diversidad
        'año',                 # Importante para recomendaciones
        'region',              # Importante para características
        'num_reviews'          # Importante para confiabilidad
    ]
    
    # Verificar qué columnas importantes existen
    columnas_importantes_existentes = [col for col in columnas_importantes if col in df.columns]
    
    print(f"🎯 Columnas importantes a limpiar: {columnas_importantes_existentes}")
    
    # Mostrar estado actual
    print(f"\n🔍 ANÁLISIS DE VALORES NaN EN COLUMNAS IMPORTANTES:")
    for columna in columnas_importantes_existentes:
        cantidad_nan = df[columna].isnull().sum()
        print(f"   {columna}: {cantidad_nan} valores NaN ({cantidad_nan/len(df)*100:.1f}%)")
    
    # Realizar limpieza progresiva
    df_limpio = df.copy()
    registros_originales = len(df_limpio)
    
    print(f"\n🧹 LIMPIEZA PROGRESIVA:")
    
    # 1. Eliminar registros sin bodega
    if 'bodega' in df_limpio.columns:
        antes = len(df_limpio)
        df_limpio = df_limpio.dropna(subset=['bodega'])
        eliminados = antes - len(df_limpio)
        print(f"   1. Sin bodega: -{eliminados} registros → {len(df_limpio)} restantes")
    
    # 2. Eliminar registros sin año
    if 'año' in df_limpio.columns:
        antes = len(df_limpio)
        df_limpio = df_limpio.dropna(subset=['año'])
        eliminados = antes - len(df_limpio)
        print(f"   2. Sin año: -{eliminados} registros → {len(df_limpio)} restantes")
    
    # 3. Eliminar registros sin región
    if 'region' in df_limpio.columns:
        antes = len(df_limpio)
        df_limpio = df_limpio.dropna(subset=['region'])
        eliminados = antes - len(df_limpio)
        print(f"   3. Sin región: -{eliminados} registros → {len(df_limpio)} restantes")
    
    # 4. Eliminar registros sin número de reviews
    if 'num_reviews' in df_limpio.columns:
        antes = len(df_limpio)
        df_limpio = df_limpio.dropna(subset=['num_reviews'])
        eliminados = antes - len(df_limpio)
        print(f"   4. Sin reviews: -{eliminados} registros → {len(df_limpio)} restantes")
    
    print(f"\n📊 RESUMEN DE LIMPIEZA EXHAUSTIVA:")
    print(f"   📉 Registros eliminados: {registros_originales - len(df_limpio)}")
    print(f"   ✅ Registros conservados: {len(df_limpio)}")
    print(f"   📊 Porcentaje conservado: {len(df_limpio)/registros_originales*100:.1f}%")
    
    if len(df_limpio) == 0:
        print("❌ ADVERTENCIA: No quedan registros después de la limpieza exhaustiva")
        return
    
    # Verificar calidad del dataset final
    print(f"\n✅ VERIFICACIÓN DE CALIDAD:")
    for columna in columnas_importantes_existentes:
        nan_count = df_limpio[columna].isnull().sum()
        if nan_count == 0:
            print(f"   ✅ {columna}: Sin valores NaN")
        else:
            print(f"   ⚠️ {columna}: {nan_count} valores NaN restantes")
    
    # Guardar archivo ultra limpio
    nombre_base = os.path.basename(archivo_objetivo)
    directorio_salida = os.path.dirname(archivo_objetivo)
    nombre_salida = os.path.join(directorio_salida, nombre_base.replace('_sin_nan_criticos.csv', '_ultra_limpio.csv'))
    
    try:
        df_limpio.to_csv(nombre_salida, index=False, encoding='utf-8')
        print(f"💾 Archivo ultra limpio guardado: {nombre_salida}")
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")
        return
    
    # Estadísticas finales detalladas
    print(f"\n📈 ESTADÍSTICAS DEL DATASET ULTRA LIMPIO:")
    
    if 'precio_eur' in df_limpio.columns:
        precio_min = df_limpio['precio_eur'].min()
        precio_max = df_limpio['precio_eur'].max()
        precio_promedio = df_limpio['precio_eur'].mean()
        print(f"   💰 Precios: €{precio_min:.2f} - €{precio_max:.2f} (promedio: €{precio_promedio:.2f})")
    
    if 'año' in df_limpio.columns:
        año_min = int(df_limpio['año'].min())
        año_max = int(df_limpio['año'].max())
        print(f"   📅 Años: {año_min} - {año_max}")
    
    if 'bodega' in df_limpio.columns:
        bodegas_unicas = df_limpio['bodega'].nunique()
        print(f"   🏭 Bodegas únicas: {bodegas_unicas}")
    
    if 'region' in df_limpio.columns:
        regiones_unicas = df_limpio['region'].nunique()
        print(f"   🌍 Regiones únicas: {regiones_unicas}")
        
        # Mostrar top 5 regiones
        top_regiones = df_limpio['region'].value_counts().head(5)
        print(f"   🔝 Top 5 regiones:")
        for region, count in top_regiones.items():
            print(f"      • {region}: {count} vinos")
    
    if 'num_reviews' in df_limpio.columns:
        reviews_promedio = df_limpio['num_reviews'].mean()
        print(f"   ⭐ Reviews promedio por vino: {reviews_promedio:.1f}")
    
    print(f"\n🎉 LIMPIEZA EXHAUSTIVA COMPLETADA")
    print(f"📁 Archivo original: {archivo_objetivo}")
    print(f"📁 Archivo ultra limpio: {nombre_salida}")
    print(f"📊 Dataset final: {len(df_limpio)} vinos de alta calidad")

if __name__ == "__main__":
    limpiar_csv_exhaustivo()
