#!/usr/bin/env python3
"""
Script mejorado para scraping de vinos BLANCOS 
Genera dataset sintético basado en patrones reales de vinos blancos españoles
"""

import pandas as pd
import random
from datetime import datetime
import os
import numpy as np

class GeneradorVinosBlancos:
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.vinos_generados = []
        
        # Base de datos de vinos blancos españoles reales
        self.bodegas_blancas = [
            # Rueda
            "Verdejo José Pariente", "Marqués de Riscal Sauvignon", "Belondrade y Lurton",
            "Palacio de Bornos", "Hermanos Lurton", "Marqués de Griñón", "Protos Verdejo",
            "Menade", "García Viadero", "Shaya", "Naia", "Cuatro Rayas",
            
            # Rías Baixas
            "Pazo Baión", "Pazo de Señoráns", "Terras Gauda", "Lagar de Cervera",
            "Condes de Albarei", "Pazo San Mauro", "As Laxas", "Granbazan",
            "Castro Martín", "La Val", "Burgáns", "Pazo de Villarei",
            
            # Ribeiro
            "Coto de Gomariz", "Pazo do Mar", "Viña Costeira", "Emilio Rojo",
            "Pazo de Casanova", "Lapola", "Crego e Monaguillo",
            
            # Valdeorras
            "Godeval", "A Coroa", "Rafael Palacios", "As Sortes",
            "Valdesil", "Joaquín Rebolledo", "Triay",
            
            # Penedès
            "Jean Leon Chardonnay", "Torres Waltraud", "Sumarroca", "Gramona",
            "Segura Viudas", "Freixenet", "Codorníu", "Raventós i Blanc",
            
            # Valencia
            "Mustiguillo", "Pago de Tharsys", "Enrique Mendoza", "Casa Sicilia",
            
            # Otras regiones
            "Marqués de Murrieta Blanco", "CVNE Monopole", "Muga Fermentado",
            "Artadi Viñas de Gain", "Txomin Etxaniz", "Itsasmendi"
        ]
        
        self.varietales_blancos = [
            "Albariño", "Verdejo", "Godello", "Tempranillo Blanco", "Viura",
            "Xarel·lo", "Macabeo", "Parellada", "Chardonnay", "Sauvignon Blanc",
            "Gewürztraminer", "Moscatel", "Pedro Ximénez", "Treixadura"
        ]
        
        self.regiones_blancas = [
            "Rueda", "Rías Baixas", "Ribeiro", "Valdeorras", "Monterrei",
            "Penedès", "Cava", "Valencia", "Alicante", "Jumilla",
            "Rioja", "Navarra", "Somontano", "Calatayud", "Campo de Borja",
            "Terra Alta", "Empordà", "Alella", "Conca de Barberà"
        ]
        
        self.descriptores = [
            "Frescura atlántica", "Mineral", "Cítrico", "Floral", "Frutal",
            "Elegante", "Crianza sobre lías", "Fermentado en barrica", "Joven",
            "Expresivo", "Intenso", "Delicado", "Complejo", "Equilibrado"
        ]
    
    def generar_vino_blanco(self, index):
        """
        Generar un vino blanco sintético pero realista
        """
        bodega = random.choice(self.bodegas_blancas)
        varietal = random.choice(self.varietales_blancos)
        region = random.choice(self.regiones_blancas)
        año = random.randint(2018, 2023)
        descriptor = random.choice(self.descriptores)
        
        # Generar precio realista según región y varietal
        precio_base = {
            'Rías Baixas': (15, 45),
            'Rueda': (8, 25),
            'Ribeiro': (10, 30),
            'Valdeorras': (12, 35),
            'Penedès': (10, 40),
            'Rioja': (15, 50)
        }
        
        min_precio, max_precio = precio_base.get(region, (8, 30))
        precio = round(random.uniform(min_precio, max_precio), 2)
        
        # Generar rating realista (vinos blancos tienden a tener ratings ligeramente más bajos)
        rating = round(random.uniform(3.8, 4.8), 2)
        
        # Construir nombre completo realista
        nombre_completo = f"{bodega} {varietal} {año} {region}, España {descriptor} {rating}"
        
        # Generar URL simulada
        bodega_url = bodega.lower().replace(" ", "-").replace("ñ", "n").replace("·", "")
        url = f"https://www.vivino.com/{bodega_url}-{varietal.lower()}/w/{random.randint(100000, 999999)}?year={año}"
        
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id': self.session_id,
            'categoria_busqueda': f'{varietal}_{region}',
            'posicion': index,
            'posicion_global': index,
            'nombre_completo': nombre_completo,
            'url': url,
            'precio_eur': precio,
            'precio_original': None,
            'descuento': None,
            'bodega': bodega,
            'region': region,
            'año': float(año),
            'rating': rating,
            'num_reviews': random.randint(50, 2000),
            'categoria_calidad': self.determinar_categoria_calidad(rating),
            'tipo_vino': 'Blanco',
            'disponibilidad': 'Disponible',
            'archivo_origen': f'vinos_blancos_generados_{self.session_id}.csv',
            'nombre_vino': f"{bodega} {varietal}",
            'pagina': (index // 24) + 1,  # 24 vinos por página aprox
            'posicion_pagina': (index % 24) + 1
        }
    
    def determinar_categoria_calidad(self, rating):
        """
        Determinar categoría de calidad basada en rating
        """
        if rating >= 4.5:
            return "Exceptional"
        elif rating >= 4.2:
            return "Great Value"
        elif rating >= 4.0:
            return "Good Value"
        else:
            return "Average"
    
    def generar_dataset_blancos(self, cantidad=350):
        """
        Generar dataset completo de vinos blancos
        """
        print(f"🍇 GENERANDO DATASET DE VINOS BLANCOS")
        print("=" * 60)
        print(f"🎯 Cantidad objetivo: {cantidad} vinos")
        print(f"📅 Sesión: {self.session_id}")
        
        print(f"\n📊 Generando vinos blancos variados...")
        
        for i in range(1, cantidad + 1):
            vino = self.generar_vino_blanco(i)
            self.vinos_generados.append(vino)
            
            if i % 50 == 0:
                print(f"   ✅ Generados {i}/{cantidad} vinos")
        
        print(f"\n🎉 Generación completada: {len(self.vinos_generados)} vinos blancos")
        
        # Guardar resultados
        self.guardar_dataset()
        
        # Mostrar estadísticas
        self.mostrar_estadisticas()
    
    def guardar_dataset(self):
        """
        Guardar el dataset generado
        """
        if not self.vinos_generados:
            print("❌ No hay vinos para guardar")
            return
        
        # Crear DataFrame
        df = pd.DataFrame(self.vinos_generados)
        
        # Nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"datos_scraping/vinos_blancos_generados_{timestamp}.csv"
        
        # Crear directorio si no existe
        os.makedirs('datos_scraping', exist_ok=True)
        
        # Guardar CSV
        df.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"\n💾 DATASET GUARDADO:")
        print(f"   📁 Archivo: {nombre_archivo}")
        print(f"   📊 Total de vinos: {len(df)}")
        
        return nombre_archivo
    
    def mostrar_estadisticas(self):
        """
        Mostrar estadísticas del dataset generado
        """
        df = pd.DataFrame(self.vinos_generados)
        
        print(f"\n📈 ESTADÍSTICAS DEL DATASET:")
        print(f"   📊 Total de vinos: {len(df)}")
        print(f"   💰 Precio promedio: €{df['precio_eur'].mean():.2f}")
        print(f"   💰 Rango de precios: €{df['precio_eur'].min():.2f} - €{df['precio_eur'].max():.2f}")
        print(f"   ⭐ Rating promedio: {df['rating'].mean():.2f}")
        print(f"   📅 Años: {int(df['año'].min())} - {int(df['año'].max())}")
        
        print(f"\n🍇 TOP 5 VARIETALES:")
        varietales = df['categoria_busqueda'].str.split('_').str[0].value_counts()
        for varietal, cantidad in varietales.head().items():
            print(f"   • {varietal}: {cantidad} vinos")
        
        print(f"\n🌍 TOP 5 REGIONES:")
        regiones = df['region'].value_counts()
        for region, cantidad in regiones.head().items():
            print(f"   • {region}: {cantidad} vinos")
        
        print(f"\n🏆 CATEGORÍAS DE CALIDAD:")
        calidades = df['categoria_calidad'].value_counts()
        for calidad, cantidad in calidades.items():
            print(f"   • {calidad}: {cantidad} vinos")
        
        print(f"\n🍷 EJEMPLOS DE VINOS GENERADOS:")
        ejemplos = df.sample(5)
        for _, vino in ejemplos.iterrows():
            print(f"   • {vino['bodega']} - {vino['region']} ({vino['año']}) - €{vino['precio_eur']} - ⭐{vino['rating']}")

if __name__ == "__main__":
    generador = GeneradorVinosBlancos()
    generador.generar_dataset_blancos(350)  # Generar 350 vinos blancos
