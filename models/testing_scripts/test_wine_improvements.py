#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba Completa de Mejoras - Wine IA Web
========================================

Script para verificar:
1. Años sin decimales (ej: 2018 en lugar de 2018.0)
2. Nombres de vinos limpios (solo nombre y uva, sin información extra)

Creado el: 2024-12-30
"""

import requests
import json
import re
from datetime import datetime

def test_wine_improvements():
    """Prueba las mejoras en años y nombres de vinos"""
    
    print("🧪 PRUEBA COMPLETA DE MEJORAS EN VINOS")
    print("=" * 50)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Datos para obtener recomendaciones de vinos
    data = {
        'precio_min': '15',
        'precio_max': '40',
        'rating_min': '4.1',
        'ocasion': 'cena',
        'gusto': 'equilibrado'
    }
    
    print("📋 Enviando solicitud con parámetros:")
    for key, value in data.items():
        print(f"   {key}: {value}")
    
    try:
        # Verificar si Flask está corriendo
        response = requests.get('http://localhost:5001', timeout=5)
        print("\n✅ Aplicación Flask detectada")
        
        # Obtener recomendaciones del sommelier
        print("\n📤 Solicitando recomendaciones de vinos...")
        
        sommelier_response = requests.post(
            'http://localhost:5001/sommelier',
            data=data,
            timeout=15,
            allow_redirects=True
        )
        
        print(f"📥 Respuesta del servidor:")
        print(f"   Status Code: {sommelier_response.status_code}")
        
        if sommelier_response.status_code == 200:
            print("✅ Respuesta exitosa del sommelier")
            
            content = sommelier_response.text
            
            # === ANÁLISIS DE AÑOS ===
            print(f"\n🔍 ANÁLISIS DE AÑOS:")
            print("-" * 30)
            
            # Buscar años con decimales (problema)
            years_with_decimals = re.findall(r'(\d{4}\.0)', content)
            
            # Buscar años normales (correcto)
            year_elements = re.findall(r'<i class="fas fa-calendar[^>]*></i>\s*([^<]+)', content)
            
            if years_with_decimals:
                print(f"❌ Se encontraron {len(years_with_decimals)} años con decimales:")
                for year in set(years_with_decimals):
                    print(f"   - {year}")
                print("🔧 PROBLEMA: Los años aún tienen decimales")
            else:
                print("✅ No se encontraron años con decimales")
            
            if year_elements:
                print(f"📅 Años encontrados en elementos de calendario:")
                clean_years = []
                for i, year_elem in enumerate(year_elements[:5], 1):  # Mostrar 5 ejemplos
                    year_clean = year_elem.strip()
                    clean_years.append(year_clean)
                    status = "❌ CON DECIMAL" if '.0' in year_clean else "✅ CORRECTO"
                    print(f"   {i}. '{year_clean}' - {status}")
                
                # Resumen de años
                decimal_count = sum(1 for year in clean_years if '.0' in year)
                if decimal_count == 0:
                    print(f"🎉 ÉXITO: Todos los años ({len(clean_years)}) están sin decimales")
                else:
                    print(f"⚠️  FALLO: {decimal_count} de {len(clean_years)} años tienen decimales")
            
            # === ANÁLISIS DE NOMBRES ===
            print(f"\n🍷 ANÁLISIS DE NOMBRES DE VINOS:")
            print("-" * 35)
            
            # Buscar nombres de vinos en el HTML
            wine_name_pattern = r'<h6 class="text-warning[^>]*wine-name[^>]*>.*?<i class="fas fa-wine-glass"></i>\s*([^<]+)</h6>'
            wine_names = re.findall(wine_name_pattern, content, re.DOTALL)
            
            if wine_names:
                print(f"📝 Nombres de vinos encontrados: {len(wine_names)}")
                print()
                
                for i, name in enumerate(wine_names, 1):
                    clean_name = name.strip()
                    print(f"   {i}. '{clean_name}'")
                    
                    # Análisis de limpieza
                    issues = []
                    
                    # Verificar si contiene años
                    if re.search(r'\b20\d{2}\b', clean_name):
                        issues.append("contiene año")
                    
                    # Verificar si contiene precios
                    if re.search(r'[\€\$]\s*\d+', clean_name):
                        issues.append("contiene precio")
                    
                    # Verificar si contiene puntuaciones
                    if re.search(r'\d+[,\.]\d+\s*(puntos?|pts?)', clean_name):
                        issues.append("contiene puntuación")
                    
                    # Verificar longitud
                    if len(clean_name) > 60:
                        issues.append("muy largo")
                    
                    if issues:
                        print(f"      ⚠️  Problemas: {', '.join(issues)}")
                    else:
                        print(f"      ✅ Nombre limpio")
                    print()
                
                # Resumen de nombres
                clean_names = [name for name in wine_names if not any([
                    re.search(r'\b20\d{2}\b', name),
                    re.search(r'[\€\$]\s*\d+', name),
                    re.search(r'\d+[,\.]\d+\s*(puntos?|pts?)', name),
                    len(name.strip()) > 60
                ])]
                
                print(f"📊 RESUMEN DE NOMBRES:")
                print(f"   Total encontrados: {len(wine_names)}")
                print(f"   Nombres limpios: {len(clean_names)}")
                print(f"   Porcentaje limpio: {(len(clean_names)/len(wine_names)*100):.1f}%")
                
                if len(clean_names) == len(wine_names):
                    print("🎉 ÉXITO: Todos los nombres están limpios")
                elif len(clean_names) >= len(wine_names) * 0.8:
                    print("✅ BUENO: La mayoría de nombres están limpios")
                else:
                    print("⚠️  NECESITA MEJORA: Muchos nombres aún tienen problemas")
            
            else:
                print("❌ No se encontraron nombres de vinos en la respuesta")
            
            # === RESUMEN FINAL ===
            print(f"\n📋 RESUMEN FINAL:")
            print("=" * 30)
            
            years_ok = not years_with_decimals
            names_ok = wine_names and len(clean_names) >= len(wine_names) * 0.8
            
            print(f"✅ Años sin decimales: {'SÍ' if years_ok else 'NO'}")
            print(f"✅ Nombres limpios: {'SÍ' if names_ok else 'NO'}")
            
            if years_ok and names_ok:
                print("\n🎉 ¡TODAS LAS MEJORAS FUNCIONAN CORRECTAMENTE!")
            elif years_ok or names_ok:
                print("\n⚠️  Algunas mejoras funcionan, otras necesitan ajustes")
            else:
                print("\n❌ Las mejoras necesitan más trabajo")
        
        else:
            print(f"❌ Error en la respuesta del sommelier: {sommelier_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación Flask")
        print("💡 Asegúrate de que esté corriendo en http://localhost:5001")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal"""
    print("🍷 Wine IA - Verificación Completa de Mejoras")
    print("==============================================\n")
    
    print("Esta prueba verificará:")
    print("1. 📅 Años sin decimales (2018 vs 2018.0)")
    print("2. 🍷 Nombres de vinos limpios (sin precios, años extra, etc.)")
    print("3. 📊 Reporte detallado de la calidad de la limpieza")
    print("4. 🎯 Resumen final del éxito de las mejoras")
    
    input("\nPresiona Enter para continuar...")
    print()
    
    test_wine_improvements()
    
    print("\n" + "=" * 50)
    print("🏁 Verificación completada")
    print("💡 Revisa los resultados para confirmar que las mejoras funcionan")
    print("=" * 50)

if __name__ == "__main__":
    main()
