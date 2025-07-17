#!/usr/bin/env python3
"""
Script para probar las recomendaciones con los datos limpios
"""

import pandas as pd
import sys
import os

# Configurar path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_sommelier import get_config

def probar_datos_limpios():
    """
    Prueba las recomendaciones con los datos limpios
    """
    print("🍷 Probando datos limpios del scraping...")
    
    config = get_config('development')
    
    if config.LATEST_CSV:
        print(f"📊 Archivo de datos: {config.LATEST_CSV}")
        
        # Cargar datos
        df = pd.read_csv(config.LATEST_CSV)
        print(f"✅ Total de vinos: {len(df)}")
        
        # Mostrar muestra de bodegas limpias
        print("\n🏭 Muestra de bodegas después de la limpieza:")
        bodegas_unicas = df['bodega'].dropna().unique()[:15]
        for i, bodega in enumerate(bodegas_unicas, 1):
            print(f"  {i:2d}. {bodega}")
        
        print(f"\n📈 Total de bodegas únicas: {len(df['bodega'].dropna().unique())}")
        
        # Buscar ejemplos específicos que estaban pegados
        ejemplos_mejorados = [
            'Morca Garnacha', 'Alto Moncayo', 'Atalaya Alaya', 
            'Bodegas Ateca Atteca', 'Comando GRozas', 'Edetària Finca'
        ]
        
        print("\n✨ Ejemplos de limpieza exitosa:")
        for ejemplo in ejemplos_mejorados:
            count = df[df['bodega'].str.contains(ejemplo, na=False, case=False)].shape[0]
            if count > 0:
                print(f"  ✅ '{ejemplo}': {count} vinos encontrados")
        
        # Verificar que no haya nombres pegados obviamente
        print("\n🔍 Verificando que no queden nombres pegados:")
        nombres_pegados = df[df['bodega'].str.contains(r'[a-z][A-Z]', na=False, regex=True)]['bodega'].unique()[:5]
        if len(nombres_pegados) > 0:
            print("  ⚠️ Algunos nombres aún pegados:")
            for nombre in nombres_pegados:
                print(f"    - {nombre}")
        else:
            print("  ✅ No se encontraron nombres obviamente pegados")
        
        return True
    else:
        print("❌ No se encontró archivo de datos")
        return False

if __name__ == "__main__":
    probar_datos_limpios()
