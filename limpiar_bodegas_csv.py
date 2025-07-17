#!/usr/bin/env python3
"""
Script para limpiar nombres de bodegas en el CSV del scraping
Separa palabras pegadas usando el patrón de mayúscula después de minúscula
"""

import pandas as pd
import re
import os
from datetime import datetime

def limpiar_nombre_bodega(nombre_bodega):
    """
    Limpia y separa nombres de bodegas pegados
    """
    if pd.isna(nombre_bodega) or not nombre_bodega:
        return nombre_bodega
    
    try:
        # Convertir a string y limpiar espacios
        nombre = str(nombre_bodega).strip()
        
        # Patrón para separar palabras pegadas: minúscula seguida de mayúscula
        # Ejemplos: "MorcaGarnacha" -> "Morca Garnacha"
        #          "Bodegas AtecaAtteca" -> "Bodegas Ateca Atteca"
        nombre_separado = re.sub(r'([a-z])([A-Z])', r'\1 \2', nombre)
        
        # Limpiar información extra común
        # Eliminar años pegados al final
        nombre_separado = re.sub(r'\s*20\d{2}[a-zA-Z]*$', '', nombre_separado)
        
        # Eliminar palabras como "Campo", "Tierra", etc. que son parte de nombres de vinos
        palabras_a_eliminar = [
            'Campo', 'Tierra', 'Red', 'Garnacha', 'Tempranillo', 'Mencía',
            'Verdejo', 'Sauvignon', 'Blanc', 'Rosé', 'Reserva', 'Crianza',
            'Gran', 'Old', 'Vines', 'Selection', 'Premium'
        ]
        
        # Dividir en palabras
        palabras = nombre_separado.split()
        palabras_filtradas = []
        
        for i, palabra in enumerate(palabras):
            # Mantener las primeras 2-3 palabras principales
            if i < 3:
                # Solo eliminar si la palabra está en la lista Y no es una de las primeras 2
                if i >= 2 and palabra in palabras_a_eliminar:
                    continue
                palabras_filtradas.append(palabra)
            else:
                # Para palabras posteriores, ser más selectivo
                if palabra not in palabras_a_eliminar and len(palabra) > 2:
                    palabras_filtradas.append(palabra)
        
        # Reconstruir el nombre
        nombre_limpio = ' '.join(palabras_filtradas)
        
        # Limpiar caracteres especiales al final
        nombre_limpio = re.sub(r'[^\w\s-].*$', '', nombre_limpio).strip()
        
        # Si el resultado está vacío, usar una versión más conservadora
        if not nombre_limpio or len(nombre_limpio) < 3:
            # Solo separar mayúsculas/minúsculas y limpiar espacios
            nombre_limpio = re.sub(r'([a-z])([A-Z])', r'\1 \2', str(nombre_bodega))
            nombre_limpio = re.sub(r'\s+', ' ', nombre_limpio).strip()
        
        return nombre_limpio
        
    except Exception as e:
        print(f"Error procesando '{nombre_bodega}': {e}")
        return str(nombre_bodega)

def procesar_csv_scraping(archivo_csv):
    """
    Procesa el archivo CSV y limpia los nombres de bodegas
    """
    print(f"📂 Procesando archivo: {archivo_csv}")
    
    # Leer el CSV
    try:
        df = pd.read_csv(archivo_csv)
        print(f"✅ Archivo leído exitosamente: {len(df)} filas")
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return None
    
    # Mostrar algunas bodegas antes de la limpieza
    print("\n🔍 Muestra de bodegas ANTES de la limpieza:")
    bodegas_sample = df['bodega'].dropna().head(10).tolist()
    for i, bodega in enumerate(bodegas_sample, 1):
        print(f"  {i:2d}. {bodega}")
    
    # Aplicar limpieza
    print("\n🧹 Aplicando limpieza de nombres de bodegas...")
    df['bodega_limpia'] = df['bodega'].apply(limpiar_nombre_bodega)
    
    # Mostrar algunas bodegas después de la limpieza
    print("\n✨ Muestra de bodegas DESPUÉS de la limpieza:")
    for i, (original, limpia) in enumerate(zip(bodegas_sample, df['bodega_limpia'].head(10)), 1):
        print(f"  {i:2d}. {original:<30} → {limpia}")
    
    # Reemplazar la columna original
    df['bodega'] = df['bodega_limpia']
    df = df.drop('bodega_limpia', axis=1)
    
    # Generar nombre del archivo limpio
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(archivo_csv)[0]
    archivo_limpio = f"{base_name}_limpio_{timestamp}.csv"
    
    # Guardar archivo limpio
    try:
        df.to_csv(archivo_limpio, index=False)
        print(f"\n💾 Archivo limpio guardado como: {archivo_limpio}")
        print(f"📊 Total de registros procesados: {len(df)}")
        
        # Estadísticas de limpieza
        bodegas_unicas_original = len(set(bodegas_sample))
        bodegas_unicas_limpia = df['bodega'].nunique()
        print(f"🏭 Bodegas únicas después de limpieza: {bodegas_unicas_limpia}")
        
        return archivo_limpio
        
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")
        return None

if __name__ == "__main__":
    archivo_csv = "resumen_scraping_completo_20250716_130237.csv"
    
    if os.path.exists(archivo_csv):
        archivo_procesado = procesar_csv_scraping(archivo_csv)
        if archivo_procesado:
            print(f"\n🎉 ¡Proceso completado exitosamente!")
            print(f"📁 Archivo original: {archivo_csv}")
            print(f"📁 Archivo limpio: {archivo_procesado}")
        else:
            print(f"\n❌ Error en el procesamiento")
    else:
        print(f"❌ Archivo no encontrado: {archivo_csv}")
