#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de Deduplicación de Vinos - Wine IA Web
===============================================

Script para verificar que se muestren 6 vinos diferentes sin duplicados.

Creado el: 2024-12-30
"""

import requests
import json
import re
from datetime import datetime

def test_wine_deduplication():
    """Prueba que los vinos recomendados sean únicos"""
    
    print("🧪 PRUEBA DE DEDUPLICACIÓN DE VINOS")
    print("=" * 45)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Datos para obtener recomendaciones (rango amplio para tener más opciones)
    data = {
        'precio_min': '10',
        'precio_max': '60',
        'rating_min': '4.0',
        'ocasion': 'general',
        'gusto': 'equilibrado'
    }
    
    print("📋 Enviando solicitud con parámetros amplios:")
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
            
            # === ANÁLISIS DE DUPLICADOS ===
            print(f"\n🔍 ANÁLISIS DE DUPLICADOS:")
            print("-" * 35)
            
            # Extraer información de vinos del HTML
            wine_pattern = r'<h6 class="text-warning[^>]*wine-name[^>]*>.*?<i class="fas fa-wine-glass"></i>\s*([^<]+)</h6>.*?<i class="fas fa-industry"></i>\s*([^<]+)</small>.*?<i class="fas fa-calendar[^>]*></i>\s*([^<]+)</small>'
            
            matches = re.findall(wine_pattern, content, re.DOTALL)
            
            if matches:
                print(f"🍷 Vinos encontrados: {len(matches)}")
                print()
                
                vinos_info = []
                
                for i, (nombre, bodega, año) in enumerate(matches, 1):
                    nombre_clean = nombre.strip()
                    bodega_clean = bodega.strip()
                    año_clean = año.strip()
                    
                    vino_info = {
                        'nombre': nombre_clean,
                        'bodega': bodega_clean,
                        'año': año_clean,
                        'clave': f"{nombre_clean.lower()}_{bodega_clean.lower()}_{año_clean}"
                    }
                    
                    vinos_info.append(vino_info)
                    
                    print(f"   {i}. 🍷 {nombre_clean}")
                    print(f"      🏭 Bodega: {bodega_clean}")
                    print(f"      📅 Año: {año_clean}")
                    print(f"      🔑 Clave: {vino_info['clave'][:50]}...")
                    print()
                
                # Análisis de duplicados
                print(f"📊 ANÁLISIS DE UNICIDAD:")
                print("-" * 25)
                
                # Por nombre
                nombres = [v['nombre'] for v in vinos_info]
                nombres_unicos = set(nombres)
                print(f"📝 Nombres únicos: {len(nombres_unicos)} de {len(nombres)}")
                
                if len(nombres_unicos) < len(nombres):
                    print("⚠️  Nombres duplicados encontrados:")
                    for nombre in nombres:
                        if nombres.count(nombre) > 1:
                            print(f"   - '{nombre}' aparece {nombres.count(nombre)} veces")
                
                # Por bodega + año
                bodegas_años = [f"{v['bodega']}_{v['año']}" for v in vinos_info]
                bodegas_años_unicos = set(bodegas_años)
                print(f"🏭 Bodega+Año únicos: {len(bodegas_años_unicos)} de {len(bodegas_años)}")
                
                if len(bodegas_años_unicos) < len(bodegas_años):
                    print("⚠️  Combinaciones bodega+año duplicadas:")
                    for combo in bodegas_años:
                        if bodegas_años.count(combo) > 1:
                            print(f"   - '{combo}' aparece {bodegas_años.count(combo)} veces")
                
                # Por clave completa
                claves = [v['clave'] for v in vinos_info]
                claves_unicas = set(claves)
                print(f"🔑 Claves únicas: {len(claves_unicas)} de {len(claves)}")
                
                if len(claves_unicas) < len(claves):
                    print("❌ Vinos completamente duplicados encontrados:")
                    for clave in claves:
                        if claves.count(clave) > 1:
                            print(f"   - Clave '{clave[:30]}...' aparece {claves.count(clave)} veces")
                
                # === VEREDICTO FINAL ===
                print(f"\n🎯 VEREDICTO FINAL:")
                print("=" * 20)
                
                total_esperado = 6
                total_encontrado = len(vinos_info)
                
                print(f"📊 Vinos esperados: {total_esperado}")
                print(f"📊 Vinos encontrados: {total_encontrado}")
                print(f"📊 Vinos únicos (nombres): {len(nombres_unicos)}")
                print(f"📊 Vinos únicos (completos): {len(claves_unicas)}")
                
                if total_encontrado == total_esperado and len(claves_unicas) == total_encontrado:
                    print("\n🎉 ¡PERFECTO! Se muestran 6 vinos completamente únicos")
                elif len(claves_unicas) == total_encontrado:
                    print(f"\n✅ BUENO: Todos los vinos mostrados son únicos")
                elif len(nombres_unicos) >= total_encontrado * 0.8:
                    print(f"\n⚠️  ACEPTABLE: La mayoría de vinos son únicos")
                else:
                    print(f"\n❌ PROBLEMA: Hay demasiados vinos duplicados")
                
                # Mostrar estadísticas de mejora
                duplicados_nombres = len(nombres) - len(nombres_unicos)
                duplicados_completos = len(claves) - len(claves_unicas)
                
                if duplicados_completos == 0:
                    print("🏆 Deduplicación perfecta implementada")
                elif duplicados_nombres == 0:
                    print("✅ Nombres únicos, variaciones menores en otros campos")
                else:
                    print(f"🔧 Se necesita mejorar la deduplicación: {duplicados_completos} duplicados")
            
            else:
                print("❌ No se pudieron extraer datos de vinos de la respuesta")
        
        else:
            print(f"❌ Error en la respuesta del sommelier: {sommelier_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación Flask")
        print("💡 Asegúrate de que esté corriendo en http://localhost:5001")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def main():
    """Función principal"""
    print("🍷 Wine IA - Verificación de Deduplicación")
    print("==========================================\n")
    
    print("Esta prueba verificará:")
    print("1. 🔢 Que se muestren exactamente 6 vinos")
    print("2. 🎯 Que todos los vinos sean únicos")
    print("3. 📊 Estadísticas de duplicación")
    print("4. 🏆 Calidad de la deduplicación implementada")
    
    input("\nPresiona Enter para continuar...")
    print()
    
    test_wine_deduplication()
    
    print("\n" + "=" * 45)
    print("🏁 Verificación de deduplicación completada")
    print("💡 Si ves duplicados, la función de deduplicación necesita ajustes")
    print("=" * 45)

if __name__ == "__main__":
    main()
