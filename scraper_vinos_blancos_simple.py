#!/usr/bin/env python3
"""
Script alternativo para scraping de vinos BLANCOS usando requests + BeautifulSoup
Más estable y sin dependencias de ChromeDriver
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import os
import json
import re
from urllib.parse import quote_plus, urljoin

class VivinoScraperBlancosSimple:
    def __init__(self):
        self.base_url = "https://www.vivino.com"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.vinos_encontrados = []
        self.session = requests.Session()
        
        # Headers para simular navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def buscar_vinos_blancos_por_termino(self, termino_busqueda, paginas=5):
        """
        Buscar vinos blancos por término de búsqueda
        """
        print(f"\n🔍 Buscando: {termino_busqueda}")
        
        for pagina in range(1, paginas + 1):
            try:
                # Construir URL de búsqueda para vinos blancos
                url = f"{self.base_url}/search/wines?q={quote_plus(termino_busqueda)}+blanco&page={pagina}"
                
                print(f"   📄 Procesando página {pagina}")
                print(f"   🔗 URL: {url}")
                
                # Realizar petición
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    # Parsear HTML
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extraer vinos de la página
                    vinos_pagina = self.extraer_vinos_de_soup(soup, termino_busqueda, pagina)
                    self.vinos_encontrados.extend(vinos_pagina)
                    
                    print(f"      ✅ {len(vinos_pagina)} vinos extraídos")
                    
                    # Si no hay vinos, probablemente no hay más páginas
                    if len(vinos_pagina) == 0:
                        print(f"      ⚠️ No se encontraron más vinos, terminando búsqueda")
                        break
                        
                else:
                    print(f"      ❌ Error HTTP {response.status_code}")
                
                # Pausa entre peticiones
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"      ❌ Error en página {pagina}: {e}")
                continue
    
    def extraer_vinos_de_soup(self, soup, categoria, pagina):
        """
        Extraer información de vinos del HTML parseado
        """
        vinos = []
        
        # Buscar diferentes selectores de tarjetas de vinos
        wine_cards = soup.find_all('div', class_=re.compile(r'wine.*card', re.I))
        
        if not wine_cards:
            # Intentar con otros selectores
            wine_cards = soup.find_all('a', href=re.compile(r'/w/\d+'))
        
        print(f"        🔍 Encontradas {len(wine_cards)} tarjetas de vinos")
        
        for i, card in enumerate(wine_cards, 1):
            try:
                vino_data = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'session_id': self.session_id,
                    'categoria_busqueda': categoria,
                    'posicion': i,
                    'posicion_global': len(self.vinos_encontrados) + i,
                    'tipo_vino': 'Blanco',  # Forzar tipo blanco
                    'pagina': pagina,
                    'posicion_pagina': i,
                    'disponibilidad': 'Disponible',
                    'archivo_origen': f'vivino_blancos_simple_{self.session_id}.csv'
                }
                
                # Extraer nombre del vino
                nombre_elem = card.find('span', class_=re.compile(r'wine.*name', re.I))
                if not nombre_elem:
                    nombre_elem = card.find(text=re.compile(r'[A-Za-z]'))
                    if isinstance(nombre_elem, str):
                        vino_data['nombre_completo'] = nombre_elem.strip()
                    else:
                        continue
                else:
                    vino_data['nombre_completo'] = nombre_elem.get_text(strip=True)
                
                # Extraer URL
                if card.name == 'a':
                    href = card.get('href')
                else:
                    link = card.find('a')
                    href = link.get('href') if link else None
                
                if href:
                    if not href.startswith('http'):
                        href = urljoin(self.base_url, href)
                    vino_data['url'] = href
                
                # Extraer precio
                precio_elem = card.find(text=re.compile(r'€\s*\d+'))
                if precio_elem:
                    precio_nums = re.findall(r'\d+[,.]?\d*', precio_elem)
                    if precio_nums:
                        try:
                            vino_data['precio_eur'] = float(precio_nums[0].replace(',', '.'))
                        except:
                            pass
                
                # Extraer rating
                rating_elem = card.find(text=re.compile(r'\d+[,.]\d+'))
                if rating_elem:
                    rating_nums = re.findall(r'\d+[,.]\d+', rating_elem)
                    if rating_nums:
                        try:
                            vino_data['rating'] = float(rating_nums[0].replace(',', '.'))
                        except:
                            pass
                
                # Procesar nombre completo para extraer más datos
                nombre_completo = vino_data.get('nombre_completo', '')
                if nombre_completo:
                    # Extraer bodega (primera parte antes de coma o espacio)
                    if ',' in nombre_completo:
                        vino_data['bodega'] = nombre_completo.split(',')[0].strip()
                    else:
                        palabras = nombre_completo.split()
                        if palabras:
                            vino_data['bodega'] = palabras[0]
                    
                    # Extraer año
                    year_match = re.search(r'\b(19|20)\d{2}\b', nombre_completo)
                    if year_match:
                        vino_data['año'] = int(year_match.group())
                    
                    # Extraer región si está presente
                    regiones_conocidas = ['Rueda', 'Rías Baixas', 'Ribeiro', 'Valdeorras', 
                                        'Penedès', 'Valencia', 'Cataluña', 'Galicia']
                    for region in regiones_conocidas:
                        if region.lower() in nombre_completo.lower():
                            vino_data['region'] = region
                            break
                
                vinos.append(vino_data)
                
            except Exception as e:
                print(f"          ⚠️ Error extrayendo vino {i}: {e}")
                continue
        
        return vinos
    
    def ejecutar_scraping_completo(self):
        """
        Ejecutar scraping completo de vinos blancos
        """
        print("🍇 INICIANDO SCRAPING DE VINOS BLANCOS (MÉTODO SIMPLE)")
        print("=" * 70)
        print(f"🎯 Objetivo: Obtener al menos 300 vinos blancos")
        print(f"📅 Sesión: {self.session_id}")
        
        # Términos de búsqueda específicos para vinos blancos españoles
        terminos_busqueda = [
            'Albariño España',
            'Verdejo Rueda',
            'Godello Valdeorras',
            'Tempranillo Blanco',
            'Viura Rioja',
            'Xarel.lo Penedès',
            'Macabeo España',
            'Parellada Cataluña',
            'vino blanco España',
            'white wine Spain',
            'Ribeiro blanco',
            'Monterrei blanco',
            'Chardonnay España',
            'Sauvignon Blanc España',
            'blanco español',
            'Rías Baixas',
            'Rueda blanco',
            'Penedès blanco',
            'Valencia blanco',
            'Galicia blanco'
        ]
        
        try:
            print(f"\n🔍 INICIANDO BÚSQUEDAS ESPECIALIZADAS")
            
            for i, termino in enumerate(terminos_busqueda, 1):
                print(f"\n📍 Búsqueda {i}/{len(terminos_busqueda)}: {termino}")
                
                self.buscar_vinos_blancos_por_termino(termino, paginas=4)
                
                print(f"   📊 Total acumulado: {len(self.vinos_encontrados)} vinos")
                
                # Pausar entre búsquedas
                time.sleep(random.uniform(3, 6))
                
                # Verificar si ya tenemos suficientes
                if len(self.vinos_encontrados) >= 300:
                    print(f"\n🎉 ¡Objetivo alcanzado! {len(self.vinos_encontrados)} vinos blancos")
                    break
            
            # Guardar resultados
            self.guardar_resultados()
            
        except KeyboardInterrupt:
            print(f"\n⚠️ Scraping interrumpido por el usuario")
            print(f"💾 Guardando {len(self.vinos_encontrados)} vinos encontrados...")
            self.guardar_resultados()
        
        except Exception as e:
            print(f"❌ Error durante el scraping: {e}")
            self.guardar_resultados()
    
    def guardar_resultados(self):
        """
        Guardar los resultados del scraping
        """
        if not self.vinos_encontrados:
            print("❌ No hay vinos para guardar")
            return
        
        # Crear DataFrame
        df = pd.DataFrame(self.vinos_encontrados)
        
        # Eliminar duplicados por URL si existe
        if 'url' in df.columns:
            df_sin_duplicados = df.drop_duplicates(subset=['url'], keep='first')
        else:
            df_sin_duplicados = df.drop_duplicates(subset=['nombre_completo'], keep='first')
        
        # Nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"datos_scraping/vivino_blancos_simple_{timestamp}.csv"
        
        # Crear directorio si no existe
        os.makedirs('datos_scraping', exist_ok=True)
        
        # Guardar CSV
        df_sin_duplicados.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"\n💾 RESULTADOS GUARDADOS:")
        print(f"   📁 Archivo: {nombre_archivo}")
        print(f"   📊 Total de vinos: {len(df_sin_duplicados)}")
        print(f"   🗑️ Duplicados eliminados: {len(df) - len(df_sin_duplicados)}")
        
        # Estadísticas
        if len(df_sin_duplicados) > 0:
            print(f"\n📈 ESTADÍSTICAS:")
            
            if 'precio_eur' in df_sin_duplicados.columns:
                precios_validos = df_sin_duplicados['precio_eur'].dropna()
                if len(precios_validos) > 0:
                    print(f"   💰 Precio promedio: €{precios_validos.mean():.2f}")
                    print(f"   💰 Rango de precios: €{precios_validos.min():.2f} - €{precios_validos.max():.2f}")
            
            if 'rating' in df_sin_duplicados.columns:
                ratings_validos = df_sin_duplicados['rating'].dropna()
                if len(ratings_validos) > 0:
                    print(f"   ⭐ Rating promedio: {ratings_validos.mean():.2f}")
            
            # Contar por categorías
            if 'categoria_busqueda' in df_sin_duplicados.columns:
                categorias = df_sin_duplicados['categoria_busqueda'].value_counts()
                print(f"   📋 Vinos por categoría de búsqueda:")
                for categoria, cantidad in categorias.head(5).items():
                    print(f"      • {categoria}: {cantidad} vinos")
            
            # Mostrar algunos ejemplos
            print(f"\n🍷 EJEMPLOS DE VINOS BLANCOS ENCONTRADOS:")
            ejemplos = df_sin_duplicados.head(5)
            for _, vino in ejemplos.iterrows():
                nombre = vino.get('nombre_completo', 'Sin nombre')
                precio = vino.get('precio_eur', 'Sin precio')
                bodega = vino.get('bodega', 'Sin bodega')
                print(f"   • {nombre[:50]}... - {bodega} - €{precio}")

if __name__ == "__main__":
    scraper = VivinoScraperBlancosSimple()
    scraper.ejecutar_scraping_completo()
