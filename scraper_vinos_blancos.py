#!/usr/bin/env python3
"""
Script especializado para scraping de vinos BLANCOS en Vivino
Objetivo: Obtener al menos 300 vinos blancos para balancear el dataset
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class VivinoScraperBlancos:
    def __init__(self):
        self.base_url = "https://www.vivino.com"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.vinos_encontrados = []
        self.setup_driver()
        
    def setup_driver(self):
        """Configurar el driver de Chrome para scraping"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en segundo plano
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            from selenium.webdriver.chrome.service import Service
            service = Service('chromedriver.exe')
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✅ Driver Chrome configurado correctamente")
        except Exception as e:
            print(f"❌ Error configurando driver: {e}")
            print("🔧 Asegúrate de que chromedriver.exe esté en el directorio")
            raise
    
    def buscar_vinos_blancos_por_region(self, region, paginas=5):
        """
        Buscar vinos blancos específicamente por región
        """
        print(f"\n🔍 Buscando vinos blancos en: {region}")
        
        # URLs específicas para vinos blancos por región
        urls_busqueda = [
            f"https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMvNzLFVy83MLrZVy8lMS7FSqyhKzSvJTI9Pzi9KycxLt1IrKUpNzCspzUGIAQCgdBaR&wine_type_ids%5B%5D=2&region_ids%5B%5D={self.get_region_id(region)}",
            f"https://www.vivino.com/search/wines?q={region}+blanco&wine_type_ids%5B%5D=2",
            f"https://www.vivino.com/search/wines?q={region}+white&wine_type_ids%5B%5D=2"
        ]
        
        for url_base in urls_busqueda:
            for pagina in range(1, paginas + 1):
                try:
                    url = f"{url_base}&page={pagina}"
                    print(f"   📄 Procesando página {pagina} de {region}")
                    
                    self.driver.get(url)
                    time.sleep(random.uniform(3, 6))
                    
                    # Esperar a que cargue el contenido
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "wine-card"))
                    )
                    
                    # Extraer información de los vinos
                    vinos_pagina = self.extraer_vinos_de_pagina(region, pagina)
                    self.vinos_encontrados.extend(vinos_pagina)
                    
                    print(f"      ✅ {len(vinos_pagina)} vinos extraídos")
                    
                    # Pausa entre páginas
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"      ❌ Error en página {pagina}: {e}")
                    continue
    
    def get_region_id(self, region):
        """Obtener ID de región para Vivino"""
        region_ids = {
            'Rueda': '55',
            'Rías Baixas': '51',
            'Valdeorras': '61',
            'Monterrei': '52',
            'Ribeiro': '54',
            'Valencia': '60',
            'Cataluña': '40',
            'Penedès': '53',
            'Alella': '35',
            'Empordà': '44'
        }
        return region_ids.get(region, '1')  # Default España
    
    def buscar_vinos_blancos_por_varietal(self, varietal, paginas=5):
        """
        Buscar vinos blancos por variedad de uva
        """
        print(f"\n🍇 Buscando vinos de variedad: {varietal}")
        
        urls_busqueda = [
            f"https://www.vivino.com/search/wines?q={varietal}&wine_type_ids%5B%5D=2",
            f"https://www.vivino.com/search/wines?q={varietal}+España&wine_type_ids%5B%5D=2",
            f"https://www.vivino.com/search/wines?q={varietal}+spanish&wine_type_ids%5B%5D=2"
        ]
        
        for url_base in urls_busqueda:
            for pagina in range(1, paginas + 1):
                try:
                    url = f"{url_base}&page={pagina}"
                    print(f"   📄 Procesando página {pagina} de {varietal}")
                    
                    self.driver.get(url)
                    time.sleep(random.uniform(3, 6))
                    
                    # Esperar a que cargue el contenido
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "wine-card"))
                    )
                    
                    # Extraer información de los vinos
                    vinos_pagina = self.extraer_vinos_de_pagina(f"{varietal}_varietal", pagina)
                    self.vinos_encontrados.extend(vinos_pagina)
                    
                    print(f"      ✅ {len(vinos_pagina)} vinos extraídos")
                    
                    # Pausa entre páginas
                    time.sleep(random.uniform(2, 4))
                    
                except Exception as e:
                    print(f"      ❌ Error en página {pagina}: {e}")
                    continue
    
    def extraer_vinos_de_pagina(self, categoria, pagina):
        """
        Extraer información de vinos de una página
        """
        vinos = []
        
        try:
            # Buscar tarjetas de vinos
            wine_cards = self.driver.find_elements(By.CSS_SELECTOR, ".wine-card, .wine_card")
            
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
                        'posicion_pagina': i
                    }
                    
                    # Extraer nombre del vino
                    try:
                        nombre_element = card.find_element(By.CSS_SELECTOR, ".wine-card__name, .wine_card__name, a[data-testid='wine-card-name']")
                        vino_data['nombre_completo'] = nombre_element.text.strip()
                    except:
                        vino_data['nombre_completo'] = "Nombre no encontrado"
                    
                    # Extraer URL
                    try:
                        link_element = card.find_element(By.CSS_SELECTOR, "a")
                        href = link_element.get_attribute('href')
                        if href and not href.startswith('http'):
                            href = self.base_url + href
                        vino_data['url'] = href
                    except:
                        vino_data['url'] = ""
                    
                    # Extraer precio
                    try:
                        precio_element = card.find_element(By.CSS_SELECTOR, ".wine-price, .wine_price, [data-testid='price']")
                        precio_text = precio_element.text.strip()
                        # Extraer número del precio
                        import re
                        precio_nums = re.findall(r'[\d,]+\.?\d*', precio_text)
                        if precio_nums:
                            vino_data['precio_eur'] = float(precio_nums[0].replace(',', '.'))
                    except:
                        vino_data['precio_eur'] = None
                    
                    # Extraer rating
                    try:
                        rating_element = card.find_element(By.CSS_SELECTOR, ".wine-card__rating, .wine_card__rating, [data-testid='rating']")
                        rating_text = rating_element.text.strip()
                        # Extraer número del rating
                        import re
                        rating_nums = re.findall(r'\d+\.?\d*', rating_text)
                        if rating_nums:
                            vino_data['rating'] = float(rating_nums[0])
                    except:
                        vino_data['rating'] = None
                    
                    # Extraer bodega y región del nombre completo
                    nombre_completo = vino_data['nombre_completo']
                    if nombre_completo and nombre_completo != "Nombre no encontrado":
                        # Intentar extraer bodega y otros datos
                        partes = nombre_completo.split(',')
                        if len(partes) >= 2:
                            vino_data['bodega'] = partes[0].strip()
                            vino_data['region'] = partes[1].strip() if len(partes) > 1 else ""
                        else:
                            vino_data['bodega'] = nombre_completo.split()[0] if nombre_completo else ""
                            vino_data['region'] = ""
                    
                    # Extraer año si está en el nombre
                    import re
                    year_match = re.search(r'\b(19|20)\d{2}\b', nombre_completo)
                    if year_match:
                        vino_data['año'] = int(year_match.group())
                    
                    # Marcar disponibilidad
                    vino_data['disponibilidad'] = 'Disponible'
                    vino_data['archivo_origen'] = f'vivino_blancos_{self.session_id}.csv'
                    
                    vinos.append(vino_data)
                    
                except Exception as e:
                    print(f"        ⚠️ Error extrayendo vino {i}: {e}")
                    continue
            
        except Exception as e:
            print(f"      ❌ Error extrayendo vinos de la página: {e}")
        
        return vinos
    
    def ejecutar_scraping_completo(self):
        """
        Ejecutar scraping completo de vinos blancos
        """
        print("🍇 INICIANDO SCRAPING DE VINOS BLANCOS")
        print("=" * 60)
        print(f"🎯 Objetivo: Obtener al menos 300 vinos blancos")
        print(f"📅 Sesión: {self.session_id}")
        
        # Regiones españolas famosas por vinos blancos
        regiones_blancas = [
            'Rueda',
            'Rías Baixas', 
            'Valdeorras',
            'Ribeiro',
            'Monterrei',
            'Penedès',
            'Valencia',
            'Alella',
            'Empordà'
        ]
        
        # Varietales blancos españoles
        varietales_blancos = [
            'Albariño',
            'Verdejo',
            'Godello',
            'Tempranillo Blanco',
            'Viura',
            'Xarel·lo',
            'Macabeo',
            'Parellada',
            'Chardonnay España',
            'Sauvignon Blanc España'
        ]
        
        try:
            # Scraping por regiones
            print(f"\n🌍 FASE 1: Scraping por regiones especializadas en blancos")
            for region in regiones_blancas:
                self.buscar_vinos_blancos_por_region(region, paginas=4)
                print(f"   📊 Total acumulado: {len(self.vinos_encontrados)} vinos")
                
                # Pausar entre regiones
                time.sleep(random.uniform(5, 8))
                
                # Verificar si ya tenemos suficientes
                if len(self.vinos_encontrados) >= 300:
                    print(f"🎉 ¡Objetivo alcanzado! {len(self.vinos_encontrados)} vinos blancos")
                    break
            
            # Si necesitamos más, buscar por varietales
            if len(self.vinos_encontrados) < 300:
                print(f"\n🍇 FASE 2: Scraping por varietales blancos")
                for varietal in varietales_blancos:
                    self.buscar_vinos_blancos_por_varietal(varietal, paginas=3)
                    print(f"   📊 Total acumulado: {len(self.vinos_encontrados)} vinos")
                    
                    # Pausar entre varietales
                    time.sleep(random.uniform(5, 8))
                    
                    # Verificar si ya tenemos suficientes
                    if len(self.vinos_encontrados) >= 300:
                        print(f"🎉 ¡Objetivo alcanzado! {len(self.vinos_encontrados)} vinos blancos")
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
        
        finally:
            self.driver.quit()
    
    def guardar_resultados(self):
        """
        Guardar los resultados del scraping
        """
        if not self.vinos_encontrados:
            print("❌ No hay vinos para guardar")
            return
        
        # Crear DataFrame
        df = pd.DataFrame(self.vinos_encontrados)
        
        # Eliminar duplicados por URL
        df_sin_duplicados = df.drop_duplicates(subset=['url'], keep='first')
        
        # Nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"datos_scraping/vivino_blancos_completo_{timestamp}.csv"
        
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
                print(f"   📋 Vinos por categoría:")
                for categoria, cantidad in categorias.head(5).items():
                    print(f"      • {categoria}: {cantidad} vinos")

if __name__ == "__main__":
    scraper = VivinoScraperBlancos()
    scraper.ejecutar_scraping_completo()
