# Resumen: Clasificación de Calidad de Vino con Modelos Ensemble

## 📊 Información General del Proyecto

**Dataset:** Wine Quality (Vino Tinto)  
**Objetivo:** Clasificación multiclase de calidad de vino (escala 3-8)  
**Técnicas:** Comparación de modelos Bagging vs Boosting  
**Accuracy máximo alcanzado:** 97.5% (XGBoost)

---

## 🔧 1. Preparación del Entorno

### Configuración inicial:

- ✅ Creación de entorno virtual Python 3.12.10
- ✅ Instalación de librerías necesarias:
  - `pandas`, `numpy`: Manipulación de datos
  - `scikit-learn`: Machine Learning
  - `matplotlib`, `seaborn`: Visualización
  - `xgboost`: Gradient Boosting avanzado
  - `imbalanced-learn`: Balanceo de clases
  - `kagglehub`: Descarga de datasets

### Importación de datos:

- Archivo fuente: `winequality-red.csv`
- Dimensiones originales: 1,599 filas × 12 columnas
- Variables: 11 características fisicoquímicas + 1 variable objetivo (quality)

---

## 📈 2. Análisis Exploratorio de Datos (EDA)

### 2.1 Inspección inicial:

- **Filas duplicadas:** 240 encontradas y eliminadas
- **Valores nulos:** 0 (dataset limpio)
- **Distribución de calidad:** Clases desbalanceadas (principalmente 5 y 6)

### 2.2 Análisis de correlaciones:

- **Correlación positiva con calidad:** alcohol (0.48), sulphates (0.25)
- **Correlación negativa con calidad:** volatile acidity (-0.39)
- **Sin multicolinealidad:** No hay características altamente correlacionadas entre sí

### 2.3 Distribución de clases originales:

- Calidad 3: 10 muestras (0.6%)
- Calidad 4: 53 muestras (3.3%)
- Calidad 5: 681 muestras (42.6%) ⚠️
- Calidad 6: 638 muestras (39.9%) ⚠️
- Calidad 7: 199 muestras (12.4%)
- Calidad 8: 18 muestras (1.1%)

---

## ⚖️ 3. Preprocesamiento de Datos

### 3.1 Balanceo de clases:

- **Técnica:** SMOTEENN (combinación de SMOTE + Edited Nearest Neighbours)
- **Resultado:** ~470 muestras por clase (distribución balanceada)
- **Dataset final:** 2,828 muestras

### 3.2 Transformación de etiquetas:

- **Problema:** XGBoost requiere etiquetas 0-5, no 3-8
- **Solución:** LabelEncoder para mapear calidades:
  - Calidad 3 → 0, Calidad 4 → 1, ..., Calidad 8 → 5

### 3.3 División de datos:

- **Training:** 80% (2,262 muestras)
- **Testing:** 20% (566 muestras)
- **Estrategia:** train_test_split con random_state=42

### 3.4 Tratamiento de asimetría:

- **Columnas asimétricas identificadas:** 6 variables
  - chlorides, residual sugar, total sulfur dioxide
  - sulphates, free sulfur dioxide, volatile acidity
- **Transformación:** PowerTransformer (Yeo-Johnson)

### 3.5 Escalado de características:

- **Técnica:** MinMaxScaler (0-1)
- **Aplicación:** Todas las características después de transformaciones

---

## 🤖 4. Modelado y Evaluación

### 4.1 Modelos Base Individuales:

| Modelo                    | Accuracy | Observaciones             |
| ------------------------- | -------- | ------------------------- |
| Logistic Regression       | ~85%     | Modelo lineal base        |
| K-Nearest Neighbors       | 97.2%    | Excelente con k=1         |
| Support Vector Classifier | 97.2%    | Kernel RBF, C=100         |
| Decision Tree             | ~93%     | Susceptible a overfitting |

### 4.2 Modelos Ensemble Originales:

| Modelo            | Accuracy  | Tipo            |
| ----------------- | --------- | --------------- |
| Random Forest     | 95.9%     | Bagging         |
| Gradient Boosting | 97.2%     | Boosting        |
| **XGBoost**       | **97.5%** | **Boosting** 🏆 |

---

## 🆚 5. Comparación Detallada: Bagging vs Boosting

### 5.1 Modelos de Bagging:

| Modelo                   | Accuracy | Descripción                                      |
| ------------------------ | -------- | ------------------------------------------------ |
| Bagging + Decision Trees | ~95%     | Bootstrap + árboles paralelos                    |
| Random Forest            | ~96%     | Bagging + selección aleatoria de características |
| Extra Trees              | ~95%     | Más aleatorio que Random Forest                  |

**Promedio Bagging:** ~95.3%

### 5.2 Modelos de Boosting:

| Modelo            | Accuracy | Descripción                  |
| ----------------- | -------- | ---------------------------- |
| AdaBoost          | ~92%     | Ajuste secuencial de pesos   |
| Gradient Boosting | ~97%     | Minimización de gradiente    |
| XGBoost           | ~97.5%   | Gradient Boosting optimizado |

**Promedio Boosting:** ~95.5%

### 5.3 Resultado de la Comparación:

🏆 **GANADOR: Modelos de Boosting** (por margen mínimo)

---

## 📊 6. Visualizaciones Creadas

### 6.1 Análisis exploratorio:

- ✅ Heatmap de correlaciones
- ✅ Distribución de clases (antes/después del balanceo)
- ✅ Histogramas y boxplots por característica
- ✅ Gráficos de barras: características vs calidad

### 6.2 Evaluación de modelos:

- ✅ Comparación de accuracy por modelo
- ✅ Promedio Bagging vs Boosting
- ✅ Matrices de confusión (Random Forest vs XGBoost)
- ✅ Reporte de clasificación detallado

---

## 🎯 7. Conclusiones Principales

### 7.1 Rendimiento de modelos:

1. **Mejor modelo individual:** XGBoost (97.5%)
2. **Mejores modelos base:** KNN y SVC (97.2%)
3. **Modelo más consistente:** Random Forest (96%+)

### 7.2 Bagging vs Boosting:

- **Boosting** ligeramente superior en promedio
- **Bagging** más estable y menos propenso a overfitting
- **Diferencia mínima:** ~0.2% entre enfoques

### 7.3 Factores clave del éxito:

- ✅ Balanceo efectivo de clases con SMOTEENN
- ✅ Transformación adecuada de características asimétricas
- ✅ Escalado apropiado de variables
- ✅ Transformación correcta de etiquetas para XGBoost

### 7.4 Características más importantes:

- **Alcohol:** Correlación más fuerte con calidad
- **Sulphates:** Segundo predictor más importante
- **Volatile acidity:** Correlación negativa significativa

---

## 🔧 8. Aspectos Técnicos Destacados

### 8.1 Desafíos resueltos:

- **Clases desbalanceadas:** SMOTEENN balanceó efectivamente
- **Etiquetas incompatibles:** LabelEncoder para XGBoost
- **Características asimétricas:** PowerTransformer normalizó distribuciones
- **Escalas diferentes:** MinMaxScaler estandarizó rangos

### 8.2 Mejores prácticas aplicadas:

- Validación cruzada implícita en ensemble methods
- Uso de random_state para reproducibilidad
- División estratificada de datos
- Evaluación con múltiples métricas

### 8.3 Configuraciones óptimas:

- **Random Forest:** 100 estimadores, características aleatorias
- **XGBoost:** learning_rate=0.1, max_depth=3, 100 estimadores
- **Gradient Boosting:** learning_rate=0.1, max_depth=3

---

## 📁 9. Archivos del Proyecto

```
ML Modelos Ensemble/
├── Wine_multiclass_classification__97_5_accuracy.ipynb
├── winequality-red.csv
├── churn.csv
├── .gitignore
├── .venv/
└── Resumen_Wine_Classification_Ensemble.md
```

---

## 🚀 10. Próximos Pasos Sugeridos

### 10.1 Mejoras potenciales:

- [ ] Hyperparameter tuning con GridSearchCV
- [ ] Ensemble voting (combinación de mejores modelos)
- [ ] Feature engineering adicional
- [ ] Validación cruzada estratificada explícita

### 10.2 Experimentación adicional:

- [ ] Otros algoritmos de balanceo (ADASYN, BorderlineSMOTE)
- [ ] Técnicas de selección de características
- [ ] Modelos de deep learning
- [ ] Análisis de importancia de características

### 10.3 Deployment:

- [ ] Creación de API para predicciones
- [ ] Containerización con Docker
- [ ] Interfaz web con Streamlit/Flask
- [ ] Monitoreo de modelo en producción

---

**Fecha de creación:** 8 de julio de 2025  
**Autor:** Análisis de clasificación de vino con modelos ensemble  
**Accuracy máximo alcanzado:** 97.5% con XGBoost  
**Técnicas clave:** Bagging, Boosting, SMOTEENN, PowerTransformer
