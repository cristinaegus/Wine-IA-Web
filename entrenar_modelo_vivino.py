# Script para entrenar un modelo Random Forest y guardarlo en modelos generados
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from sklearn.preprocessing import StandardScaler

# Ruta de datos y modelo
DATA_PATH = 'datos_scraping/vivino_diversificado_20250716_130100.csv'
MODEL_DIR = 'modelos generados'
MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_random_forest_vivino.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler_vivino.pkl')

# Crear carpeta si no existe
os.makedirs(MODEL_DIR, exist_ok=True)

# Cargar datos
print('Cargando datos...')
df = pd.read_csv(DATA_PATH)


# Selección de variables adaptadas
features = ['precio_eur', 'rating', 'num_reviews']
target = 'categoria_calidad'


# Eliminar filas con NaN en las columnas relevantes
df = df.dropna(subset=features + [target])


# Preparar X y y
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y = df[target]
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)

# Separar datos
test_size = 0.2
random_state = 42
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=test_size, random_state=random_state)

# Entrenar modelo
print('Entrenando modelo Random Forest...')
clf = RandomForestClassifier(n_estimators=100, random_state=random_state)
clf.fit(X_train, y_train)


# Guardar modelo y scaler (solo le_target)
joblib.dump({'model': clf, 'le_target': le_target}, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
print(f'Modelo guardado en {MODEL_PATH}')
print(f'Scaler guardado en {SCALER_PATH}')


# --- Prueba de predicción con el modelo generado ---
print('\nProbando la predicción con el modelo guardado...')
modelo_cargado = joblib.load(MODEL_PATH)
clf_loaded = modelo_cargado['model']
le_target_loaded = modelo_cargado['le_target']

# Tomar una muestra aleatoria del conjunto de test
import numpy as np
idx = np.random.choice(len(X_test), 1)[0]
sample = X_test[idx].reshape(1, -1)
true_label = y_test[idx]
pred = clf_loaded.predict(sample)
pred_label = le_target_loaded.inverse_transform(pred)[0]
true_label_name = le_target_loaded.inverse_transform([true_label])[0]
print(f'Valores de entrada: {sample.tolist()[0]}')
print(f'Categoría real: {true_label_name}')
print(f'Predicción del modelo: {pred_label}')
