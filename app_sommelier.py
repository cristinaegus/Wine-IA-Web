import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
import os
import glob
import warnings
from config_sommelier import get_config
from models import db, bcrypt, User, UserSession, WineRecommendation
from datetime import datetime, timedelta
import json
warnings.filterwarnings("ignore")

# Configuración de la aplicación
config = get_config('development')
app = Flask(__name__)
app.config.from_object(config)

# Inicializar extensiones
db.init_app(app)
bcrypt.init_app(app)

# Cargar el modelo de Vivino y datos al iniciar la aplicación
try:
    # Cargar modelos usando configuración centralizada
    model, scaler, label_encoder, model_info = config.cargar_modelo()
    
    if model is None:
        raise FileNotFoundError("No se pudieron cargar los modelos")
    
    # Mostrar información del modelo si está disponible
    if model_info:
        print(f"🍷 Sommelier usando modelo v{model_info.get('version', 'desconocida')}")
        print(f"📊 Precisión: {model_info.get('accuracy', 'N/A')}")
        print(f"🎯 Features: {len(model_info.get('caracteristicas', []))}")
        
        # Cargar label encoders del modelo
        label_encoders = model_info.get('label_encoders', {})
        caracteristicas_modelo = model_info.get('caracteristicas', [])
        print(f"🔧 Label encoders disponibles: {list(label_encoders.keys())}")
    else:
        label_encoders = {}
        caracteristicas_modelo = []
    
    # Cargar datos del último scraping usando configuración
    if config.LATEST_CSV:
        df_vinos = pd.read_csv(config.LATEST_CSV)
        print(f"✅ Datos cargados desde: {config.LATEST_CSV}")
        print(f"✅ Total de vinos disponibles: {len(df_vinos)}")
    else:
        df_vinos = pd.DataFrame()
        print("⚠️ No se encontraron archivos de scraping")
    
    print("✅ Modelo Sommelier y datos cargados exitosamente")
except FileNotFoundError as e:
    print(f"⚠️ Archivos del modelo no encontrados: {e}")
    model = None
    scaler = None
    label_encoder = None
    df_vinos = pd.DataFrame()

def categorizar_precio(precio):
    """Categorizar precio según rangos"""
    if precio >= 40:
        return 'Premium'
    elif precio >= 25:
        return 'Alto'
    elif precio >= 18:
        return 'Medio'
    elif precio >= 12:
        return 'Económico'
    else:
        return 'Muy Económico'

def categorizar_popularidad(num_reviews):
    """Categorizar popularidad según número de reviews"""
    if num_reviews >= 1000:
        return 'Muy Popular'
    elif num_reviews >= 500:
        return 'Popular'
    elif num_reviews >= 200:
        return 'Conocido'
    else:
        return 'Nicho'

def predecir_calidad_vino_completo(precio, rating, año, bodega="Desconocida", region="España", num_reviews=500):
    """Predice la categoría de calidad usando el modelo completo con 15 características"""
    try:
        import numpy as np
        import pandas as pd
        
        # Verificar que tenemos los componentes necesarios
        if not label_encoders or not caracteristicas_modelo:
            print("⚠️ Usando predicción simplificada - modelo incompleto")
            return predecir_calidad_vino_simple(precio, rating, año, bodega, region)
        
        # Crear DataFrame temporal para procesamiento
        vino_data = pd.DataFrame({
            'precio_eur': [precio],
            'rating': [rating],
            'año': [año],
            'num_reviews': [num_reviews],
            'region': [region],
            'bodega': [bodega]
        })
        
        # 1. Características numéricas básicas
        caracteristicas = {}
        
        # Precio
        caracteristicas['precio_eur'] = precio
        caracteristicas['log_precio'] = np.log1p(precio)
        
        # Rating
        caracteristicas['rating'] = rating
        rating_min, rating_max = 3.0, 5.0  # Asumimos rangos típicos
        caracteristicas['rating_normalizado'] = (rating - rating_min) / (rating_max - rating_min)
        
        # Año
        caracteristicas['año'] = año
        caracteristicas['antiguedad'] = 2025 - año
        
        # Reviews
        caracteristicas['num_reviews'] = num_reviews
        caracteristicas['log_reviews'] = np.log1p(num_reviews)
        
        # 2. Características categóricas codificadas
        # Procesar región
        region_especifica = region if region != "España" else "Otras Regiones"
        if 'region_especifica' in label_encoders:
            try:
                caracteristicas['region_especifica_encoded'] = label_encoders['region_especifica'].transform([region_especifica])[0]
            except:
                caracteristicas['region_especifica_encoded'] = 0  # Valor por defecto
        else:
            caracteristicas['region_especifica_encoded'] = 0
        
        # Procesar rango de precio
        if precio <= 15:
            rango_precio = 'Económico'
        elif precio <= 25:
            rango_precio = 'Medio'
        elif precio <= 40:
            rango_precio = 'Premium'
        elif precio <= 60:
            rango_precio = 'Lujo'
        else:
            rango_precio = 'Ultra-Premium'
            
        if 'rango_precio' in label_encoders:
            try:
                caracteristicas['rango_precio_encoded'] = label_encoders['rango_precio'].transform([rango_precio])[0]
            except:
                caracteristicas['rango_precio_encoded'] = 1  # Valor por defecto
        else:
            caracteristicas['rango_precio_encoded'] = 1
        
        # Procesar rango de rating
        if rating < 4.0:
            rango_rating = 'Bueno'
        elif rating < 4.2:
            rango_rating = 'Muy Bueno'
        elif rating < 4.4:
            rango_rating = 'Excelente'
        else:
            rango_rating = 'Excepcional'
            
        if 'rango_rating' in label_encoders:
            try:
                caracteristicas['rango_rating_encoded'] = label_encoders['rango_rating'].transform([rango_rating])[0]
            except:
                caracteristicas['rango_rating_encoded'] = 1  # Valor por defecto
        else:
            caracteristicas['rango_rating_encoded'] = 1
        
        # Procesar época
        if año <= 2000:
            epoca = 'Clásicos'
        elif año <= 2010:
            epoca = 'Millennium'
        elif año <= 2015:
            epoca = 'Década 2010'
        elif año <= 2020:
            epoca = 'Modernos'
        else:
            epoca = 'Recientes'
            
        if 'epoca' in label_encoders:
            try:
                caracteristicas['epoca_encoded'] = label_encoders['epoca'].transform([epoca])[0]
            except:
                caracteristicas['epoca_encoded'] = 2  # Valor por defecto
        else:
            caracteristicas['epoca_encoded'] = 2
        
        # Procesar bodega simplificada
        bodega_simplificada = ' '.join(bodega.split()[:2])
        if 'bodega_simplificada' in label_encoders:
            try:
                caracteristicas['bodega_simplificada_encoded'] = label_encoders['bodega_simplificada'].transform([bodega_simplificada])[0]
            except:
                caracteristicas['bodega_simplificada_encoded'] = 0  # Valor por defecto
        else:
            caracteristicas['bodega_simplificada_encoded'] = 0
        
        # 3. Características de interacción
        caracteristicas['precio_rating_ratio'] = precio / rating
        caracteristicas['precio_por_año'] = precio / (caracteristicas['antiguedad'] + 1)
        
        # 4. Ordenar características según el modelo
        X = np.array([[caracteristicas[feat] for feat in caracteristicas_modelo]])
        
        print(f"🔧 Características creadas: {len(X[0])}")
        print(f"📊 Features esperadas: {len(caracteristicas_modelo)}")
        
        # 5. Escalar y predecir
        X_scaled = scaler.transform(X)
        
        # Hacer predicción
        if 'objetivo' in label_encoders:
            prediccion_encoded = model.predict(X_scaled)[0]
            prediccion = label_encoders['objetivo'].inverse_transform([prediccion_encoded])[0]
        else:
            # Fallback a clases del modelo
            clases_calidad = model_info.get('clases_calidad', ['Bueno', 'Muy Bueno', 'Excelente'])
            prediccion_encoded = model.predict(X_scaled)[0]
            prediccion = clases_calidad[prediccion_encoded] if prediccion_encoded < len(clases_calidad) else 'Muy Bueno'
        
        # Obtener probabilidades
        if hasattr(model, 'predict_proba'):
            probabilidades = model.predict_proba(X_scaled)[0]
            confianza = max(probabilidades) * 100
        else:
            confianza = 85.0
        
        print(f"✅ Predicción exitosa: {prediccion} ({confianza:.1f}%)")
        return prediccion, confianza
        
    except Exception as e:
        print(f"❌ Error en predicción completa: {e}")
        print("🔄 Intentando predicción simplificada...")
        return predecir_calidad_vino_simple(precio, rating, año, bodega, region)

def predecir_calidad_vino_simple(precio, rating, año, bodega="Desconocida", region="España"):
    """Función de predicción simplificada como fallback"""
    try:
        # Valores por defecto
        posicion = 1
        num_reviews = 500
        categoria_calidad = "Good Value"
        categoria_precio = categorizar_precio(precio)
        categoria_popularidad = categorizar_popularidad(num_reviews)
        
        # Crear características numéricas
        caracteristicas_numericas = [precio, rating, año, posicion, num_reviews]
        
        # Para variables categóricas, usar valores codificados simples
        bodega_encoded = 0
        region_encoded = 0
        categoria_calidad_encoded = 1
        categoria_precio_encoded = 2
        categoria_popularidad_encoded = 1
        
        # Combinar todas las características
        caracteristicas = np.array([caracteristicas_numericas + 
                                  [bodega_encoded, region_encoded, categoria_calidad_encoded, 
                                   categoria_precio_encoded, categoria_popularidad_encoded]])
        
        # Escalar características
        caracteristicas_scaled = scaler.transform(caracteristicas)
        
        # Hacer predicción
        if label_encoder:
            prediccion_encoded = model.predict(caracteristicas_scaled)[0]
            prediccion = label_encoder.inverse_transform([prediccion_encoded])[0]
        else:
            clases_calidad = ['Bueno', 'Muy Bueno', 'Excelente']
            prediccion_encoded = model.predict(caracteristicas_scaled)[0]
            prediccion = clases_calidad[prediccion_encoded] if prediccion_encoded < len(clases_calidad) else 'Muy Bueno'
        
        # Obtener probabilidades
        if hasattr(model, 'predict_proba'):
            probabilidades = model.predict_proba(caracteristicas_scaled)[0]
            confianza = max(probabilidades) * 100
        else:
            confianza = 75.0
        
        return prediccion, confianza
        
    except Exception as e:
        print(f"❌ Error en predicción simple: {e}")
        return "Error en predicción", 0

def buscar_vinos_similares(precio_min, precio_max, rating_min=4.0):
    """Busca vinos similares en el dataset"""
    if df_vinos.empty:
        return []
    
    # Filtrar vinos por criterios
    vinos_filtrados = df_vinos[
        (df_vinos['precio_eur'] >= precio_min) &
        (df_vinos['precio_eur'] <= precio_max) &
        (df_vinos['rating'] >= rating_min)
    ].copy()
    
    # Limpiar y convertir rating
    def limpiar_rating(rating_str):
        try:
            if isinstance(rating_str, (int, float)):
                return float(rating_str)
            import re
            numeros = re.findall(r'(\d+\.?\d*)', str(rating_str))
            if numeros:
                return float(numeros[0])
            return 4.0
        except:
            return 4.0
    
    vinos_filtrados['rating_limpio'] = vinos_filtrados['rating'].apply(limpiar_rating)
    vinos_filtrados = vinos_filtrados[vinos_filtrados['rating_limpio'] >= rating_min]
    
    # Ordenar por rating y precio
    vinos_filtrados = vinos_filtrados.sort_values(['rating_limpio', 'precio_eur'], ascending=[False, True])
    
    return vinos_filtrados.head(6).to_dict('records')

def validate_registration_data(data):
    """Valida los datos de registro"""
    errors = []
    
    # Validar campos requeridos
    required_fields = ['firstName', 'lastName', 'email', 'password', 'confirmPassword', 'birthDate']
    for field in required_fields:
        if not data.get(field):
            errors.append(f'El campo {field} es requerido')
    
    # Validar email
    email = data.get('email', '').strip().lower()
    if email:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors.append('Formato de email inválido')
        
        # Verificar si el email ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            errors.append('Este email ya está registrado')
    
    # Validar contraseñas
    password = data.get('password', '')
    confirm_password = data.get('confirmPassword', '')
    
    if password != confirm_password:
        errors.append('Las contraseñas no coinciden')
    
    if len(password) < 8:
        errors.append('La contraseña debe tener al menos 8 caracteres')
    
    # Validar edad
    birth_date_str = data.get('birthDate')
    if birth_date_str:
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            today = datetime.now().date()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
            
            if age < 18:
                errors.append('Debes ser mayor de 18 años para registrarte')
        except ValueError:
            errors.append('Fecha de nacimiento inválida')
    
    return errors

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro con conexión a base de datos"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            data = {
                'firstName': request.form.get('firstName', '').strip(),
                'lastName': request.form.get('lastName', '').strip(),
                'email': request.form.get('email', '').strip().lower(),
                'password': request.form.get('password', ''),
                'confirmPassword': request.form.get('confirmPassword', ''),
                'birthDate': request.form.get('birthDate', ''),
                'newsletter': request.form.get('newsletter') == 'on',
                'terms': request.form.get('terms') == 'on'
            }
            
            # Validar términos y condiciones
            if not data['terms']:
                flash('Debes aceptar los términos y condiciones', 'error')
                return render_template('register.html')
            
            # Validar datos
            errors = validate_registration_data(data)
            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('register.html')
            
            # Crear nuevo usuario
            birth_date = datetime.strptime(data['birthDate'], '%Y-%m-%d').date()
            new_user = User(
                email=data['email'],
                password=data['password'],
                first_name=data['firstName'],
                last_name=data['lastName'],
                birth_date=birth_date,
                newsletter_subscription=data['newsletter']
            )
            
            # Guardar en base de datos
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'¡Bienvenido {new_user.get_full_name()}! Tu cuenta ha sido creada exitosamente.', 'success')
            flash('Ahora puedes iniciar sesión con tu email y contraseña.', 'info')
            
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la cuenta: {str(e)}', 'error')
            return render_template('register.html')
    
    # GET request - mostrar formulario
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login con autenticación"""
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            remember = request.form.get('remember') == 'on'
            
            if not email or not password:
                flash('Email y contraseña son requeridos', 'error')
                return render_template('login.html')
            
            # Buscar usuario
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    flash('Tu cuenta está desactivada. Contacta al administrador.', 'error')
                    return render_template('login.html')
                
                # Actualizar último login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Crear sesión
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['user_name'] = user.get_full_name()
                session.permanent = remember
                
                flash(f'¡Bienvenido de vuelta, {user.first_name}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email o contraseña incorrectos', 'error')
                return render_template('login.html')
                
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
            return render_template('login.html')
    
    # GET request - mostrar formulario
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    user_name = session.get('user_name', 'Usuario')
    session.clear()
    flash(f'¡Hasta luego, {user_name}!', 'info')
    return redirect(url_for('home'))

@app.route('/home')
def home():
    """Página de inicio con navegación"""
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Verificar que el modelo esté cargado
            if model is None or scaler is None:
                return render_template('sommelier_index.html',
                                    prediction_text='Error: Modelo Sommelier no disponible.',
                                    show_result=True,
                                    error=True)

            # Obtener datos del formulario
            precio_min = float(request.form['precio_min'])
            precio_max = float(request.form['precio_max'])
            rating_min = float(request.form.get('rating_min', 4.0))
            ocasion = request.form.get('ocasion', 'general')
            gusto = request.form.get('gusto', 'equilibrado')
            
            # Calcular precio promedio para predicción
            precio_promedio = (precio_min + precio_max) / 2
            
            # Ajustar rating esperado según el gusto
            rating_objetivo = rating_min
            if gusto == 'premium':
                rating_objetivo = max(4.15, rating_min)
            elif gusto == 'equilibrado':
                rating_objetivo = max(4.12, rating_min)
            
            # Predecir calidad
            prediccion, confianza = predecir_calidad_vino_completo(precio_promedio, rating_objetivo, 2021)
            
            # Buscar vinos similares
            vinos_recomendados = buscar_vinos_similares(precio_min, precio_max, rating_min)
            
            # Preparar contexto de respuesta
            prediction_text = f"Recomendación: {prediccion}"
            
            # Determinar color según predicción
            color_map = {
                'Excelente': 'text-success',
                'Muy Bueno': 'text-info', 
                'Bueno': 'text-primary',
                'Regular': 'text-warning',
                'Básico': 'text-secondary'
            }
            category_color = color_map.get(prediccion, 'text-primary')
            
            # Mensaje personalizado según ocasión
            ocasion_messages = {
                'romantica': 'Perfecto para una velada romántica',
                'fiesta': 'Ideal para compartir en celebraciones',
                'regalo': 'Excelente opción como obsequio',
                'cena': 'Perfecto para acompañar una buena cena',
                'general': 'Excelente elección para cualquier ocasión'
            }
            ocasion_text = ocasion_messages.get(ocasion, ocasion_messages['general'])
            
            return render_template('sommelier_index.html',
                                prediction_text=prediction_text,
                                quality_category=prediccion,
                                category_color=category_color,
                                confidence=f"Confianza: {confianza:.1f}%",
                                ocasion_text=ocasion_text,
                                vinos_recomendados=vinos_recomendados,
                                show_result=True,
                                error=False)

        except ValueError as e:
            return render_template('sommelier_index.html',
                                prediction_text='Error: Por favor, ingrese valores numéricos válidos.',
                                show_result=True,
                                error=True)
        except Exception as e:
            return render_template('sommelier_index.html',
                                prediction_text=f'Error inesperado: {str(e)}',
                                show_result=True,
                                error=True)

    # GET request - mostrar formulario inicial
    return render_template('sommelier_index.html', show_result=False)

@app.route('/api/vinos')
def api_vinos():
    """API endpoint para obtener lista de vinos"""
    if df_vinos.empty:
        return jsonify({'error': 'No hay datos de vinos disponibles'})
    
    # Convertir a diccionario y limitar a 50 vinos
    vinos_json = df_vinos.head(50).to_dict('records')
    return jsonify({'vinos': vinos_json, 'total': len(df_vinos)})

@app.route('/api/recomendar')
def api_recomendar():
    """API endpoint para recomendaciones"""
    precio_min = float(request.args.get('precio_min', 10))
    precio_max = float(request.args.get('precio_max', 50))
    rating_min = float(request.args.get('rating_min', 4.0))
    
    vinos = buscar_vinos_similares(precio_min, precio_max, rating_min)
    return jsonify({'recomendaciones': vinos})

@app.route('/about')
def about():
    """Página de información sobre el modelo"""
    model_info = {
        'nombre': 'Sommelier Inteligente - Vivino Dataset',
        'tipo': 'Random Forest Classifier',
        'dataset': 'Vinos españoles extraídos de Vivino',
        'total_vinos': len(df_vinos) if not df_vinos.empty else 0,
        'caracteristicas': ['Precio', 'Rating', 'Año', 'Bodega', 'Región', 'Popularidad'],
        'accuracy': '100% (en conjunto de prueba)',
        'fecha_entrenamiento': 'Julio 2025'
    }
    
    return render_template('sommelier_about.html', model_info=model_info)

if __name__ == '__main__':
    print("🍷 Iniciando Sommelier Inteligente...")
    
    # Crear tablas de base de datos
    with app.app_context():
        try:
            print("📊 Conectando a la base de datos PostgreSQL...")
            db.create_all()
            print("✅ Tablas de base de datos creadas/verificadas")
            
            # Verificar conexión
            user_count = User.query.count()
            print(f"👥 Usuarios registrados: {user_count}")
            
        except Exception as e:
            print(f"❌ Error con la base de datos: {e}")
            print("⚠️ La aplicación funcionará sin registro de usuarios")
    
    print(f"🌐 Servidor disponible en: http://{config.HOST}:{config.PORT}")
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
