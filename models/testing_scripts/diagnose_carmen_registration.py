#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de registro
Revisar por qué el registro de Carmen Castro no se guardó
"""

import sys
import os

# Agregar el directorio raíz al path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from app_sommelier import app, db, User
from datetime import datetime, date

def diagnose_registration_issues():
    """Diagnostica problemas con el registro"""
    print("🔍 DIAGNÓSTICO DE PROBLEMAS DE REGISTRO")
    print("=" * 50)
    
    with app.app_context():
        try:
            # 1. Verificar usuarios existentes
            print("👥 Usuarios actuales en la base de datos:")
            users = User.query.all()
            for i, user in enumerate(users, 1):
                print(f"   {i}. {user.get_full_name()} ({user.email})")
                print(f"      - ID: {user.id}")
                print(f"      - Creado: {user.created_at}")
                print(f"      - Activo: {user.is_active}")
                print()
            
            print(f"📊 Total de usuarios: {len(users)}")
            
            # 2. Buscar específicamente a Carmen Castro
            print("\n🔍 Buscando específicamente a Carmen Castro...")
            carmen_emails = [
                'carmen.castro@gmail.com',
                'carmencastro@gmail.com', 
                'carmen@gmail.com',
                'castro@gmail.com'
            ]
            
            for email in carmen_emails:
                user = User.query.filter_by(email=email).first()
                if user:
                    print(f"✅ Encontrada: {user.get_full_name()} ({user.email})")
                else:
                    print(f"❌ No encontrada: {email}")
            
            # 3. Buscar por nombre
            print("\n🔍 Buscando por nombre 'Carmen'...")
            carmen_users = User.query.filter(User.first_name.ilike('%carmen%')).all()
            if carmen_users:
                for user in carmen_users:
                    print(f"✅ Encontrada: {user.get_full_name()} ({user.email})")
            else:
                print("❌ No se encontraron usuarios con nombre Carmen")
            
            # 4. Buscar por apellido
            print("\n🔍 Buscando por apellido 'Castro'...")
            castro_users = User.query.filter(User.last_name.ilike('%castro%')).all()
            if castro_users:
                for user in castro_users:
                    print(f"✅ Encontrada: {user.get_full_name()} ({user.email})")
            else:
                print("❌ No se encontraron usuarios con apellido Castro")
            
            # 5. Verificar estructura de la tabla
            print("\n🔍 Verificando estructura de la tabla 'users'...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = inspector.get_columns('users')
            
            print("📋 Columnas de la tabla 'users':")
            for col in columns:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f" DEFAULT {col['default']}" if col['default'] else ""
                print(f"   - {col['name']}: {col['type']} {nullable}{default}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en diagnóstico: {e}")
            return False

def test_registration_with_carmen_data():
    """Prueba el registro con datos similares a Carmen Castro"""
    print("\n🧪 PRUEBA DE REGISTRO CON DATOS DE CARMEN")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Datos de prueba similares a lo que Carmen habría ingresado
            test_data = {
                'firstName': 'Carmen',
                'lastName': 'Castro',
                'email': 'carmen.castro.test@gmail.com',
                'password': 'password123',
                'confirmPassword': 'password123',
                'birthDate': '1985-05-15',
                'newsletter': True,
                'terms': True
            }
            
            print(f"📝 Intentando registrar: {test_data['firstName']} {test_data['lastName']}")
            print(f"📧 Email: {test_data['email']}")
            print(f"📅 Fecha nacimiento: {test_data['birthDate']}")
            
            # Verificar si ya existe
            existing = User.query.filter_by(email=test_data['email']).first()
            if existing:
                print(f"⚠️ Usuario ya existe, eliminando para la prueba...")
                db.session.delete(existing)
                db.session.commit()
            
            # Crear usuario de prueba
            birth_date = datetime.strptime(test_data['birthDate'], '%Y-%m-%d').date()
            new_user = User(
                email=test_data['email'],
                password=test_data['password'],
                first_name=test_data['firstName'],
                last_name=test_data['lastName'],
                birth_date=birth_date,
                newsletter_subscription=test_data['newsletter']
            )
            
            # Intentar guardar
            db.session.add(new_user)
            db.session.commit()
            
            print("✅ Registro exitoso!")
            print(f"   - ID: {new_user.id}")
            print(f"   - Nombre completo: {new_user.get_full_name()}")
            print(f"   - Email: {new_user.email}")
            print(f"   - Edad: {new_user.get_age()} años")
            
            # Verificar que se guardó
            saved_user = User.query.filter_by(email=test_data['email']).first()
            if saved_user:
                print("✅ Confirmación: Usuario encontrado en BD después del registro")
            else:
                print("❌ Error: Usuario no encontrado en BD después del registro")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en registro de prueba: {e}")
            db.session.rollback()
            return False

def check_constraints_and_validations():
    """Verifica constraints y validaciones que podrían estar causando fallos"""
    print("\n🔍 VERIFICANDO CONSTRAINTS Y VALIDACIONES")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Verificar constraints de la tabla
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            
            # Obtener constraints
            constraints = inspector.get_check_constraints('users')
            foreign_keys = inspector.get_foreign_keys('users')
            indexes = inspector.get_indexes('users')
            unique_constraints = inspector.get_unique_constraints('users')
            
            print("🔒 Constraints únicos:")
            for constraint in unique_constraints:
                print(f"   - {constraint['name']}: {constraint['column_names']}")
            
            print("\n🔍 Índices:")
            for index in indexes:
                unique = " (UNIQUE)" if index['unique'] else ""
                print(f"   - {index['name']}: {index['column_names']}{unique}")
            
            print("\n📋 Claves foráneas:")
            for fk in foreign_keys:
                print(f"   - {fk['name']}: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
            
            # Verificar si hay emails duplicados
            print("\n🔍 Verificando emails duplicados...")
            result = db.session.execute(text("""
                SELECT email, COUNT(*) as count 
                FROM users 
                GROUP BY email 
                HAVING COUNT(*) > 1
            """))
            
            duplicates = result.fetchall()
            if duplicates:
                print("⚠️ Emails duplicados encontrados:")
                for row in duplicates:
                    print(f"   - {row[0]}: {row[1]} veces")
            else:
                print("✅ No hay emails duplicados")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verificando constraints: {e}")
            return False

def main():
    """Función principal de diagnóstico"""
    print("🍷 DIAGNÓSTICO COMPLETO - REGISTRO CARMEN CASTRO")
    print("🔍 Investigando por qué no se guardó el registro")
    print("=" * 60)
    
    # Ejecutar diagnósticos
    diag1 = diagnose_registration_issues()
    diag2 = test_registration_with_carmen_data()
    diag3 = check_constraints_and_validations()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO:")
    print(f"   - Búsqueda de usuarios: {'✅ OK' if diag1 else '❌ FALLO'}")
    print(f"   - Prueba de registro: {'✅ OK' if diag2 else '❌ FALLO'}")
    print(f"   - Verificación constraints: {'✅ OK' if diag3 else '❌ FALLO'}")
    
    if diag1 and diag2 and diag3:
        print("\n💡 CONCLUSIÓN:")
        print("El sistema de registro funciona correctamente.")
        print("Posibles causas de que Carmen Castro no aparezca:")
        print("   1. Error en el formulario web (JavaScript)")
        print("   2. Validación fallida (términos, edad, etc.)")
        print("   3. Email ya existente")
        print("   4. Error de red durante el envío")
        print("   5. Datos incorrectos en el formulario")
    else:
        print("\n⚠️ Se encontraron problemas que requieren atención")

if __name__ == "__main__":
    main()
