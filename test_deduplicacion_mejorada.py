#!/usr/bin/env python3
"""
Script para probar la nueva función de deduplicación mejorada
"""

import sys
import os

# Configurar path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Simular la función directamente para probar
import pandas as pd
from config_sommelier import get_config

def test_deduplicacion_mejorada():
    """
    Prueba múltiples búsquedas para verificar que no se dupliquen vinos
    """
    print("🧪 PROBANDO DEDUPLICACIÓN MEJORADA")
    print("=" * 50)
    
    config = get_config('development')
    
    if not config.LATEST_CSV:
        print("❌ No se encontró archivo de datos")
        return
    
    # Importar la función desde app_sommelier
    try:
        from app_sommelier import buscar_vinos_similares
        print("✅ Función importada correctamente")
    except ImportError as e:
        print(f"❌ Error importando función: {e}")
        return
    
    # Realizar múltiples búsquedas con los mismos parámetros
    print("\n🔍 PRUEBA 1: Mismos parámetros múltiples veces")
    
    parametros = [20, 35, 4.1]  # precio_min, precio_max, rating_min
    
    for i in range(3):
        print(f"\n--- Búsqueda #{i+1} ---")
        vinos = buscar_vinos_similares(*parametros)
        
        nombres = [vino['nombre_limpio'] for vino in vinos]
        bodegas = [vino['bodega'] for vino in vinos]
        
        print(f"Vinos encontrados: {len(vinos)}")
        print(f"Nombres únicos: {len(set(nombres))} de {len(nombres)}")
        print(f"Bodegas únicas: {len(set(bodegas))} de {len(bodegas)}")
        
        # Mostrar los vinos
        for j, vino in enumerate(vinos, 1):
            print(f"  {j}. {vino['nombre_limpio']} - {vino['bodega']} ({vino['año']})")
        
        # Verificar duplicados
        if len(set(nombres)) < len(nombres):
            print("❌ DUPLICADOS DETECTADOS EN NOMBRES")
        else:
            print("✅ Sin duplicados en nombres")
        
        if len(set(bodegas)) < len(bodegas):
            print("⚠️ Algunas bodegas repetidas (puede ser normal)")
        else:
            print("✅ Sin duplicados en bodegas")
    
    # Probar con diferentes parámetros
    print("\n🔍 PRUEBA 2: Diferentes rangos de precio")
    
    rangos_prueba = [
        [15, 30, 4.0],
        [25, 50, 4.1],
        [10, 25, 4.2]
    ]
    
    for i, (precio_min, precio_max, rating_min) in enumerate(rangos_prueba):
        print(f"\n--- Rango #{i+1}: €{precio_min}-{precio_max}, rating ≥{rating_min} ---")
        vinos = buscar_vinos_similares(precio_min, precio_max, rating_min)
        
        if vinos:
            nombres = [vino['nombre_limpio'] for vino in vinos]
            print(f"Vinos: {len(vinos)}, Únicos: {len(set(nombres))}")
            
            if len(set(nombres)) == len(nombres):
                print("✅ Deduplicación correcta")
            else:
                print("❌ Duplicados encontrados")
        else:
            print("⚠️ No se encontraron vinos")
    
    print("\n🎉 PRUEBAS COMPLETADAS")

if __name__ == "__main__":
    test_deduplicacion_mejorada()
