# Script para probar el modelo Random Forest entrenado con las variables seleccionadas
import joblib
import numpy as np

MODEL_PATH = 'modelos generados/modelo_random_forest_vivino.pkl'
SCALER_PATH = 'modelos generados/scaler_vivino.pkl'

# Cargar modelo y scaler
modelo_cargado = joblib.load(MODEL_PATH)
clf = modelo_cargado['model']
le_target = modelo_cargado['le_target']
scaler = joblib.load(SCALER_PATH)

# Ejemplo de entrada: precio_eur, rating, num_reviews
entrada = np.array([[12.5, 4.2, 150]])  # Modifica estos valores para tu prueba
entrada_scaled = scaler.transform(entrada)

# Realizar predicción
pred = clf.predict(entrada_scaled)
pred_label = le_target.inverse_transform(pred)[0]
print(f'Valores de entrada: {entrada.tolist()[0]}')
print(f'Predicción del modelo: {pred_label}')
