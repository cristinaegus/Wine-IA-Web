#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de Corrección de Años - Wine IA Web
==========================================

Script para verificar que los años de los vinos ya no aparezcan con decimales.

Creado el: 2024-12-30
"""

import requests
import json
from datetime import datetime

def test_year_formatting():
    """Prueba que los años se muestren sin decimales"""
    
    print("🧪 PRUEBA DE CORRECCIÓN DE AÑOS EN VINOS")
    print("=" * 45)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Datos para obtener recomendaciones de vinos
    data = {
        'precio_min': '10',
        'precio_max': '50',
        'rating_min': '4.0',
        'ocasion': 'general',
        'gusto': 'equilibrado'
    }
    
    print("📋 Enviando solicitud de recomendaciones con parámetros:")
    for key, value in data.items():
        print(f"   {key}: {value}")
    
    try:
        # Verificar si Flask está corriendo
        response = requests.get('http://localhost:5001', timeout=5)
        print("\n✅ Aplicación Flask detectada")
        
        # Obtener recomendaciones
        print("\n📤 Solicitando recomendaciones de vinos...")
        
        sommelier_response = requests.post(
            'http://localhost:5001/sommelier',
            data=data,
            timeout=10,
            allow_redirects=True
        )
        
        print(f"📥 Respuesta del servidor:")
        print(f"   Status Code: {sommelier_response.status_code}")
        
        if sommelier_response.status_code == 200:
            print("✅ Respuesta exitosa del sommelier")
            
            # Buscar años en la respuesta HTML
            content = sommelier_response.text
            
            # Buscar patrones de años con decimales (ej: 2018.0, 2019.0)
            import re
            
            # Buscar años con decimales en el contenido
            years_with_decimals = re.findall(r'(\d{4}\.0)', content)
            years_without_decimals = re.findall(r'(\d{4})(?!\.)', content)
            
            print(f"\n🔍 Análisis de años en la respuesta:")
            
            if years_with_decimals:
                print(f"❌ Se encontraron {len(years_with_decimals)} años con decimales:")
                for year in set(years_with_decimals):
                    print(f"   - {year}")
                print("🔧 El problema AÚN EXISTE - revisar la corrección")
            else:
                print("✅ No se encontraron años con decimales")
            
            # Mostrar algunos años encontrados (sin decimales)
            unique_years = set(years_without_decimals)
            if unique_years:
                print(f"✅ Años encontrados (formato correcto): {len(unique_years)}")
                sample_years = list(unique_years)[:5]  # Mostrar solo 5 ejemplos
                for year in sample_years:
                    print(f"   - {year}")
            
            # Buscar elementos con la clase de año en el HTML
            year_elements = re.findall(r'<i class="fas fa-calendar[^>]*></i>\s*([^<]+)', content)
            if year_elements:
                print(f"\n📅 Elementos de año encontrados en el HTML:")
                for i, year_elem in enumerate(year_elements[:3], 1):  # Mostrar solo 3 ejemplos
                    year_clean = year_elem.strip()
                    print(f"   {i}. '{year_clean}'")
                    
                    # Verificar si contiene decimales
                    if '.0' in year_clean:
                        print(f"      ❌ Contiene decimal: {year_clean}")
                    else:
                        print(f"      ✅ Formato correcto: {year_clean}")
        else:
            print(f"❌ Error en la respuesta: {sommelier_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación Flask")
        print("💡 Asegúrate de que esté corriendo en http://localhost:5001")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal"""
    print("🍷 Wine IA - Verificación de Corrección de Años")
    print("===============================================\n")
    
    print("Esta prueba va a:")
    print("1. 🧪 Solicitar recomendaciones de vinos al sommelier")
    print("2. 🔍 Analizar la respuesta HTML en busca de años con decimales")
    print("3. ✅ Confirmar que la corrección funcionó")
    print("4. 📝 Mostrar un reporte detallado")
    
    input("\nPresiona Enter para continuar...")
    print()
    
    test_year_formatting()
    
    print("\n" + "=" * 45)
    print("🏁 Verificación completada")
    print("💡 Si ves años con decimales (ej: 2018.0), la corrección necesita ajustes")
    print("✅ Si todos los años aparecen sin decimales (ej: 2018), ¡la corrección funcionó!")
    print("=" * 45)

if __name__ == "__main__":
    main()
