# -*- coding: utf-8 -*-
"""
Integración de preprocesamiento de datos y análisis en base a umbrales.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
import pymongo

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]

# Cargar datos de nadadores y umbrales
collection_nadadores = db["datos_nadadores"]
df = pd.DataFrame(list(collection_nadadores.find()))

collection_umbrales = db["umbrales"]
umbrales = collection_umbrales.find_one()

# Asegurarse de que las columnas sean numéricas
df['Height (cm)'] = pd.to_numeric(df['Height (cm)'], errors='coerce')
df['Weight (kg)'] = pd.to_numeric(df['Weight (kg)'], errors='coerce')
df['Competition Time (s)'] = pd.to_numeric(df['Competition Time (s)'], errors='coerce')
df['Current Age'] = pd.to_numeric(df['Current Age'], errors='coerce')
df['Competition Years'] = pd.to_numeric(df['Competition Years'], errors='coerce')
df['Best Time (s)'] = pd.to_numeric(df['Best Time (s)'], errors='coerce')
df['IMC'] = pd.to_numeric(df['IMC'], errors='coerce')
df['Training Hours/Week'] = pd.to_numeric(df['Training Hours/Week'], errors='coerce')
df['Gender'] = pd.to_numeric(df['Gender'], errors='coerce')
df['Position'] = pd.to_numeric(df['Position'], errors='coerce')

# Eliminar columnas innecesarias
df = df.drop(columns=['Last Injury', 'Nivel de Competencia', 'Categoria IMC'], errors='ignore')

# Eliminar filas con datos faltantes
df = df.dropna()

# Normalización de variables numéricas
variables_a_normalizar = ['Height (cm)', 'Weight (kg)', 'Competition Time (s)', 'Current Age', 
                          'Competition Years', 'Best Time (s)', 'IMC', 'Training Hours/Week']
df[variables_a_normalizar] = df[variables_a_normalizar] / df[variables_a_normalizar].max()

# Convertir variables categóricas a numéricas
df = pd.get_dummies(df, columns=['Country', 'Competition', 'Entrenador', 'Historial de competencias'], drop_first=True)

# Separación de características y variable objetivo
df['champion'] = df['Position'].apply(lambda x: 1 if x == 1 else 0)

# Eliminamos columnas no numéricas y la columna '_id' generada por MongoDB
X = df.drop(['champion', 'Name', 'Event Date', 'Position', '_id'], axis=1, errors='ignore')
Y = df['champion']  # Variable objetivo

# Asegurarse de que todas las columnas de X sean numéricas
X = X.apply(pd.to_numeric, errors='coerce')

# Verificación y eliminación de valores NaN
X = X.dropna()

# Manejar clases desbalanceadas usando oversampling
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
x_train, y_train = smote.fit_resample(X, Y)

# División de los datos en entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.3, random_state=42, stratify=y_train)

# Modelo SVM
modelo_svm = svm.SVC(C=1.0, kernel='rbf', gamma='scale', probability=True)
modelo_svm.fit(x_train, y_train)

# Evaluación del modelo
y_pred_svm = modelo_svm.predict(x_test)
acc_svm = accuracy_score(y_test, y_pred_svm)

# Función para determinar la categoría y si es campeón
def evaluar_nadador(genero, edad, tiempo, categoria_indicada):
    if edad <= 24:
        grupo_edad = '18-24'
    elif edad <= 35:
        grupo_edad = '25-35'
    else:
        grupo_edad = '36 y más'
    
    genero_clave = 'hombre' if genero == 0 else 'mujer'
    umbral_categoria = umbrales[genero_clave][categoria_indicada.lower()][grupo_edad]
    tiempo_campeon = umbral_categoria['min'] + 3

    # Determinar la categoría real
    categorias = ['olimpico', 'profesional', 'amateur']
    categoria_real = 'Sin Categoría'
    for categoria in categorias:
        umbral = umbrales[genero_clave][categoria][grupo_edad]
        if umbral['min'] <= tiempo <= umbral['max']:
            categoria_real = categoria.capitalize()
            break

    # Evaluar si es campeón
    es_campeon = tiempo <= tiempo_campeon or (
        categoria_real != categoria_indicada and tiempo <= umbrales[genero_clave][categoria_real.lower()][grupo_edad]['max']
    )

    return categoria_real, es_campeon

# Solicitar la categoría indicada por el usuario y sus tiempos
categoria_indicada = 'profesional'  # Reemplazar con la entrada del usuario

# Datos del nuevo nadador proporcionados por el usuario
nuevo_nadador = {
    'Height (cm)': 167,
    'Weight (kg)': 70,
    'Competition Time (s)': 69.00,
    'Current Age': 22,
    'Competition Years': 4,
    'Best Time (s)': 74.00,
    'IMC': 25.09,
    'Training Hours/Week': 15,
    'Gender': 0  # 0 para hombre, 1 para mujer
}

# Normalización del nuevo nadador
nuevo_nadador_normalizado = {key: value / df[key].max() for key, value in nuevo_nadador.items() if key in df.columns}
nuevo_nadador_df = pd.DataFrame([nuevo_nadador_normalizado])

# Asegurar que las columnas del nuevo nadador coincidan con el entrenamiento
nuevo_nadador_df = nuevo_nadador_df.reindex(columns=x_train.columns, fill_value=0)

# Predicciones para el nuevo nadador
prediccion_svm = modelo_svm.predict(nuevo_nadador_df)

# Evaluar la categoría y si es campeón
categoria_real, es_campeon = evaluar_nadador(
    nuevo_nadador['Gender'],
    nuevo_nadador['Current Age'],
    nuevo_nadador['Competition Time (s)'],
    categoria_indicada
)

# Resultados
print(f"\nPrecisión del modelo SVM: {acc_svm:.2f}")
print(f"Categoría indicada por el usuario: {categoria_indicada.capitalize()}")
print(f"Categoría real del nadador: {categoria_real}")
print(f"Predicción del modelo SVM (1 = campeón): {prediccion_svm[0]}")
print(f"¿Es campeón en la categoría indicada?: {'Sí' if es_campeon else 'No'}")
