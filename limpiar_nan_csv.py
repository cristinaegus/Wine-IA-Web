#!/usr/bin/env python3
"""
Script para eliminar registros con valores NaN del CSV de vinos
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def limpiar_nan_csv():
    """
    Elimina todos los registros que contienen valores NaN del CSV
    """
    print("🧹 LIMPIANDO REGISTROS CON VALORES NaN")
    print("=" * 50)
    
    # Buscar el archivo CSV más reciente en datos_scraping
    directorio_datos = 'datos_scraping'
    if not os.path.exists(directorio_datos):
        print(f"❌ No se encontró el directorio {directorio_datos}")
        return
    
    archivos_csv = []
    for archivo in os.listdir(directorio_datos):
        if archivo.endswith('.csv'):
            archivos_csv.append(os.path.join(directorio_datos, archivo))
    
    if not archivos_csv:
        print("❌ No se encontraron archivos CSV en datos_scraping")
        return
    
    # Usar el archivo más reciente (limpio si existe)
    archivo_principal = None
    for archivo in archivos_csv:
        if 'limpio' in archivo and 'resumen_scraping_completo' in archivo:
            archivo_principal = archivo
            break
    
    if not archivo_principal:
        # Buscar cualquier archivo de resumen completo
        for archivo in archivos_csv:
            if 'resumen_scraping_completo' in archivo:
                archivo_principal = archivo
                break
    
    if not archivo_principal:
        # Usar el primer archivo disponible
        archivo_principal = archivos_csv[0]
    
    print(f"📂 Procesando archivo: {archivo_principal}")
    
    # Cargar datos
    try:
        df = pd.read_csv(archivo_principal)
        print(f"✅ Archivo cargado: {len(df)} registros totales")
    except Exception as e:
        print(f"❌ Error cargando archivo: {e}")
        return
    
    # Definir columnas críticas que NO deben tener NaN
    columnas_criticas = [
        'nombre_limpio',      # Nombre del vino es esencial
        'precio_eur',         # Precio es esencial para recomendaciones
        'rating_limpio',      # Rating es esencial para calidad
        'url'                 # URL es esencial para identificar el vino
    ]
    
    # Verificar qué columnas críticas existen en el DataFrame
    columnas_criticas_existentes = [col for col in columnas_criticas if col in df.columns]
    
    if not columnas_criticas_existentes:
        print("❌ No se encontraron columnas críticas en el DataFrame")
        print(f"Columnas disponibles: {list(df.columns)}")
        return
    
    print(f"🎯 Columnas críticas a verificar: {columnas_criticas_existentes}")
    
    # Mostrar información sobre valores NaN en columnas críticas
    print(f"\n🔍 ANÁLISIS DE VALORES NaN EN COLUMNAS CRÍTICAS:")
    for columna in columnas_criticas_existentes:
        cantidad_nan = df[columna].isnull().sum()
        print(f"   {columna}: {cantidad_nan} valores NaN ({cantidad_nan/len(df)*100:.1f}%)")
    
    # Contar registros con NaN en columnas críticas
    registros_con_nan_criticos = df[columnas_criticas_existentes].isnull().any(axis=1).sum()
    print(f"\n📊 Registros con NaN en columnas críticas: {registros_con_nan_criticos}")
    print(f"📊 Registros válidos en columnas críticas: {len(df) - registros_con_nan_criticos}")
    
    # Eliminar solo registros con NaN en columnas críticas
    df_limpio = df.dropna(subset=columnas_criticas_existentes)
    
    print(f"\n🧹 RESULTADO DE LA LIMPIEZA SELECTIVA:")
    print(f"   📉 Registros eliminados: {len(df) - len(df_limpio)}")
    print(f"   ✅ Registros conservados: {len(df_limpio)}")
    print(f"   📊 Porcentaje conservado: {len(df_limpio)/len(df)*100:.1f}%")
    
    if len(df_limpio) == 0:
        print("❌ ADVERTENCIA: No quedan registros después de la limpieza")
        return
    
    # Verificar que no queden NaN en columnas críticas
    nan_restantes_criticos = df_limpio[columnas_criticas_existentes].isnull().sum().sum()
    if nan_restantes_criticos == 0:
        print("✅ Verificación: No quedan valores NaN en columnas críticas")
    else:
        print(f"⚠️ Advertencia: Aún quedan {nan_restantes_criticos} valores NaN en columnas críticas")
    
    # Mostrar información adicional sobre otras columnas con NaN
    print(f"\n📋 INFORMACIÓN ADICIONAL:")
    nan_por_columna_restante = df_limpio.isnull().sum()
    columnas_con_nan = [(col, cantidad) for col, cantidad in nan_por_columna_restante.items() if cantidad > 0]
    
    if columnas_con_nan:
        print(f"Columnas que aún tienen NaN (no críticas):")
        for columna, cantidad in columnas_con_nan:
            print(f"   {columna}: {cantidad} valores NaN ({cantidad/len(df_limpio)*100:.1f}%)")
    else:
        print("✅ No quedan valores NaN en ninguna columna")
    
    # Guardar archivo limpio en el mismo directorio
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Determinar nombre del archivo de salida
    nombre_base = os.path.basename(archivo_principal)
    directorio_salida = os.path.dirname(archivo_principal)
    
    if 'limpio' in nombre_base:
        nombre_salida = os.path.join(directorio_salida, nombre_base.replace('.csv', f'_sin_nan_criticos.csv'))
    else:
        nombre_salida = os.path.join(directorio_salida, nombre_base.replace('.csv', f'_limpio_sin_nan_criticos.csv'))
    
    try:
        df_limpio.to_csv(nombre_salida, index=False, encoding='utf-8')
        print(f"💾 Archivo guardado: {nombre_salida}")
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")
        return
    
    # Mostrar muestra de datos limpios
    print(f"\n📋 MUESTRA DE DATOS LIMPIOS:")
    print(f"Primeros 3 registros:")
    
    columnas_importantes = ['nombre_limpio', 'bodega', 'año', 'precio_eur', 'rating_limpio']
    columnas_mostrar = [col for col in columnas_importantes if col in df_limpio.columns]
    
    for i, (_, row) in enumerate(df_limpio.head(3).iterrows()):
        print(f"   {i+1}. ", end="")
        valores = []
        for col in columnas_mostrar:
            valor = row[col]
            if pd.notna(valor):
                valores.append(f"{col}={valor}")
        print(" | ".join(valores))
    
    # Estadísticas finales
    print(f"\n📈 ESTADÍSTICAS FINALES:")
    if 'precio_eur' in df_limpio.columns:
        precio_promedio = df_limpio['precio_eur'].mean()
        print(f"   💰 Precio promedio: €{precio_promedio:.2f}")
    
    if 'rating_limpio' in df_limpio.columns:
        rating_promedio = df_limpio['rating_limpio'].mean()
        print(f"   ⭐ Rating promedio: {rating_promedio:.2f}")
    
    if 'bodega' in df_limpio.columns:
        bodegas_unicas = df_limpio['bodega'].nunique()
        print(f"   🏭 Bodegas únicas: {bodegas_unicas}")
    
    print(f"\n🎉 LIMPIEZA COMPLETADA EXITOSAMENTE")
    print(f"📁 Archivo original: {archivo_principal}")
    print(f"📁 Archivo limpio: {nombre_salida}")

if __name__ == "__main__":
    limpiar_nan_csv()
