#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del sistema de registro
"""

import sys
import os

# Agregar el directorio raíz al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from app_sommelier import app, db, User
from datetime import datetime, date

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando conexión a la base de datos...")
    
    with app.app_context():
        try:
            # Contar usuarios existentes
            user_count = User.query.count()
            print(f"✅ Conexión exitosa. Usuarios en BD: {user_count}")
            
            # Listar usuarios existentes
            if user_count > 0:
                users = User.query.all()
                print("\n👥 Usuarios registrados:")
                for user in users:
                    print(f"   - {user.get_full_name()} ({user.email}) - Creado: {user.created_at}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False

def test_user_registration():
    """Prueba el registro de un nuevo usuario"""
    print("\n🧪 Probando registro de nuevo usuario...")
    
    with app.app_context():
        try:
            # Datos de prueba
            test_email = "test@wineai.com"
            
            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=test_email).first()
            if existing_user:
                print(f"⚠️ Usuario {test_email} ya existe, eliminando para la prueba...")
                db.session.delete(existing_user)
                db.session.commit()
            
            # Crear nuevo usuario de prueba
            new_user = User(
                email=test_email,
                password="test123456",
                first_name="Usuario",
                last_name="Prueba",
                birth_date=date(1990, 1, 1),
                newsletter_subscription=True
            )
            
            # Guardar en base de datos
            db.session.add(new_user)
            db.session.commit()
            
            print(f"✅ Usuario creado exitosamente:")
            print(f"   - ID: {new_user.id}")
            print(f"   - Nombre: {new_user.get_full_name()}")
            print(f"   - Email: {new_user.email}")
            print(f"   - Edad: {new_user.get_age()} años")
            print(f"   - Es adulto: {new_user.is_adult()}")
            
            # Verificar que se puede hacer login
            password_check = new_user.check_password("test123456")
            print(f"   - Verificación password: {'✅ Correcta' if password_check else '❌ Incorrecta'}")
            
            # Contar usuarios totales
            total_users = User.query.count()
            print(f"\n📊 Total de usuarios en BD: {total_users}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en registro: {e}")
            db.session.rollback()
            return False

def test_user_validation():
    """Prueba las validaciones del usuario"""
    print("\n🔍 Probando validaciones...")
    
    with app.app_context():
        try:
            # Probar usuario menor de edad
            young_user = User(
                email="young@test.com",
                password="test123456",
                first_name="Joven",
                last_name="Menor",
                birth_date=date(2010, 1, 1),  # 15 años
                newsletter_subscription=False
            )
            
            print(f"   - Usuario menor de edad: {young_user.get_age()} años")
            print(f"   - Es adulto: {'✅ Sí' if young_user.is_adult() else '❌ No'}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en validaciones: {e}")
            return False

def main():
    """Función principal de pruebas"""
    print("🍷 PRUEBAS DEL SISTEMA DE REGISTRO - WINE IA")
    print("=" * 50)
    
    # Test 1: Conexión a base de datos
    db_ok = test_database_connection()
    
    if not db_ok:
        print("❌ No se puede continuar sin conexión a BD")
        return
    
    # Test 2: Registro de usuario
    registration_ok = test_user_registration()
    
    # Test 3: Validaciones
    validation_ok = test_user_validation()
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   - Conexión BD: {'✅ OK' if db_ok else '❌ FALLO'}")
    print(f"   - Registro: {'✅ OK' if registration_ok else '❌ FALLO'}")
    print(f"   - Validaciones: {'✅ OK' if validation_ok else '❌ FALLO'}")
    
    if db_ok and registration_ok and validation_ok:
        print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✅ El sistema de registro está funcionando correctamente")
    else:
        print("\n⚠️ Hay problemas que necesitan ser revisados")

if __name__ == "__main__":
    main()
