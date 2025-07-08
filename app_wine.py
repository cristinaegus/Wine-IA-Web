import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
import os
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Cargar el modelo y el scaler al iniciar la aplicación
try:
    model = pickle.load(open('static/wine_model.pkl', 'rb'))
    scaler = pickle.load(open('static/wine_scaler.pkl', 'rb'))
    print("✅ Modelo y scaler cargados exitosamente")
except FileNotFoundError:
    print("⚠️  Archivos del modelo no encontrados. Ejecute train_wine_model.py primero")
    model = None
    scaler = None

# Mapeo de calidades transformadas a originales
quality_mapping = {0: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Verificar que el modelo esté cargado
            if model is None or scaler is None:
                return render_template('wine_index.html',
                                    prediction_text='Error: Modelo no disponible. Entrene el modelo primero.',
                                    show_result=True,
                                    error=True)

            # 1. Obtener datos del formulario web
            fixed_acidity = float(request.form['fixed_acidity'])
            volatile_acidity = float(request.form['volatile_acidity'])
            citric_acid = float(request.form['citric_acid'])
            residual_sugar = float(request.form['residual_sugar'])
            chlorides = float(request.form['chlorides'])
            free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])
            density = float(request.form['density'])
            pH = float(request.form['pH'])
            sulphates = float(request.form['sulphates'])
            alcohol = float(request.form['alcohol'])

            # 2. Crear DataFrame con los datos
            input_data = pd.DataFrame({
                'fixed acidity': [fixed_acidity],
                'volatile acidity': [volatile_acidity],
                'citric acid': [citric_acid],
                'residual sugar': [residual_sugar],
                'chlorides': [chlorides],
                'free sulfur dioxide': [free_sulfur_dioxide],
                'total sulfur dioxide': [total_sulfur_dioxide],
                'density': [density],
                'pH': [pH],
                'sulphates': [sulphates],
                'alcohol': [alcohol]
            })

            # 3. Normalizar los datos usando el scaler cargado
            scaled_data = scaler.transform(input_data)

            # 4. Hacer la predicción con el modelo cargado
            prediction_encoded = model.predict(scaled_data)
            prediction_proba = model.predict_proba(scaled_data)

            # 5. Convertir predicción a calidad original
            predicted_quality = quality_mapping[prediction_encoded[0]]
            confidence = round(max(prediction_proba[0]) * 100, 1)

            # 6. Determinar categoría de calidad
            if predicted_quality <= 4:
                quality_category = "Baja"
                category_color = "text-danger"
            elif predicted_quality <= 6:
                quality_category = "Media"
                category_color = "text-warning"
            else:
                quality_category = "Alta"
                category_color = "text-success"

            return render_template('wine_index.html',
                                prediction_text=f'Calidad del Vino Predicha: {predicted_quality}/10',
                                quality_category=f'Categoría: {quality_category}',
                                confidence=f'Confianza: {confidence}%',
                                category_color=category_color,
                                show_result=True,
                                error=False)

        except ValueError as e:
            return render_template('wine_index.html',
                                prediction_text='Error: Por favor, ingrese valores numéricos válidos.',
                                show_result=True,
                                error=True)
        except Exception as e:
            return render_template('wine_index.html',
                                prediction_text=f'Error inesperado: {str(e)}',
                                show_result=True,
                                error=True)

    return render_template('wine_index.html', show_result=False)

@app.route('/about')
def about():
    return render_template('wine_about.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint para predicciones programáticas"""
    try:
        data = request.get_json()
        
        # Crear DataFrame con los datos recibidos
        input_data = pd.DataFrame([data])
        
        # Normalizar y predecir
        scaled_data = scaler.transform(input_data)
        prediction_encoded = model.predict(scaled_data)
        prediction_proba = model.predict_proba(scaled_data)
        
        # Convertir a calidad original
        predicted_quality = quality_mapping[prediction_encoded[0]]
        confidence = round(max(prediction_proba[0]) * 100, 1)
        
        return jsonify({
            'predicted_quality': predicted_quality,
            'confidence': confidence,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

if __name__ == '__main__':
    print("🍷 Iniciando aplicación de clasificación de vinos...")
    print("📊 Navegue a http://127.0.0.1:5000 para usar la aplicación")
    app.run(debug=True, host='0.0.0.0', port=5000)
