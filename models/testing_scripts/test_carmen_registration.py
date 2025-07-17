#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de Registro Carmen Castro - Wine IA Web
==============================================

Script para probar específicamente el registro de Carmen Castro
y verificar que el logging funcione correctamente.

Creado el: 2024-12-30
"""

import requests
import json
from datetime import datetime
import time

def test_carmen_registration():
    """Prueba el registro de Carmen Castro via API"""
    
    print("🧪 PRUEBA DE REGISTRO - CARMEN CASTRO")
    print("=" * 45)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Datos de Carmen Castro
    data = {
        'firstName': 'Carmen',
        'lastName': 'Castro',
        'email': 'carmencastro@wineai.com',
        'password': 'carmen123',
        'confirmPassword': 'carmen123',
        'birthDate': '1985-03-15',
        'newsletter': 'on',
        'terms': 'on'
    }
    
    print("📋 Datos a enviar:")
    for key, value in data.items():
        if key not in ['password', 'confirmPassword']:
            print(f"   {key}: {value}")
    
    print("\n🔍 Verificando si la aplicación está corriendo...")
    
    try:
        # Verificar si Flask está corriendo
        response = requests.get('http://localhost:5001', timeout=5)
        print("✅ Aplicación Flask detectada")
        
        # Intentar registro
        print("\n📤 Enviando datos de registro...")
        
        register_response = requests.post(
            'http://localhost:5001/register',
            data=data,
            timeout=10,
            allow_redirects=False
        )
        
        print(f"📥 Respuesta del servidor:")
        print(f"   Status Code: {register_response.status_code}")
        print(f"   Headers: {dict(register_response.headers)}")
        
        if register_response.status_code == 302:
            print("✅ Redirección detectada - Posible registro exitoso")
        elif register_response.status_code == 200:
            print("⚠️  Respuesta 200 - Verificar formulario o errores")
        else:
            print(f"❌ Status inesperado: {register_response.status_code}")
            
        print(f"\n📄 Contenido de respuesta (primeros 500 chars):")
        print(register_response.text[:500])
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la aplicación Flask")
        print("💡 Asegúrate de que esté corriendo en http://localhost:5001")
        print("   Ejecuta: python app_sommelier.py")
        
    except requests.exceptions.Timeout:
        print("⏱️  Timeout - La aplicación tardó demasiado en responder")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

def check_database_for_carmen():
    """Verifica si Carmen está en la base de datos"""
    print("\n🔍 VERIFICACIÓN EN BASE DE DATOS")
    print("=" * 35)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        
        # Usar la app y base de datos de app_sommelier
        from app_sommelier import app, User
        
        with app.app_context():
            # Buscar Carmen Castro
            results = User.query.filter(
                (User.first_name.ilike('%carmen%')) | 
                (User.last_name.ilike('%castro%'))
            ).all()
            
            if results:
                print(f"👥 Usuarios encontrados con 'Carmen' o 'Castro': {len(results)}")
                for user in results:
                    print(f"   🆔 ID: {user.id} | 📧 {user.email} | 👤 {user.first_name} {user.last_name} | 📅 {user.created_at}")
            else:
                print("❌ No se encontraron usuarios con 'Carmen' o 'Castro'")
        
    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")

def main():
    """Función principal"""
    print("🍷 Wine IA - Prueba de Registro Carmen Castro")
    print("=============================================\n")
    
    print("Esta prueba va a:")
    print("1. 🧪 Intentar registrar a Carmen Castro")
    print("2. 🔍 Verificar la respuesta del servidor")
    print("3. 📊 Buscar en la base de datos")
    print("4. 📝 Mostrar logs detallados")
    
    input("\nPresiona Enter para continuar...")
    print()
    
    # Ejecutar pruebas
    test_carmen_registration()
    check_database_for_carmen()
    
    print("\n" + "=" * 45)
    print("🏁 Prueba completada")
    print("💡 Revisa los logs de la aplicación Flask para más detalles")
    print("=" * 45)

if __name__ == "__main__":
    main()
