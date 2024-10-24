# -*- coding: utf-8 -*-
"""Created on Wed Sep 25 16:34:50 2024
@author: 20151
Archivo que genera un modelo predictivo"""
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]
collection = db["datos_nadadores"]
data = pd.DataFrame(list(collection.find()))

# Revisar las primeras filas y nombres de columnas
print(data.head())
print(data.columns)

# Asegurarse de que las columnas sean numéricas
data['Height (cm)'] = pd.to_numeric(data['Height (cm)'], errors='coerce')
data['Weight (kg)'] = pd.to_numeric(data['Weight (kg)'], errors='coerce')
data['Competition Time (s)'] = pd.to_numeric(data['Competition Time (s)'], errors='coerce')
data['Gender'] = pd.to_numeric(data['Gender'], errors='coerce')

# Separar variables independientes y dependientes
X = data[['Height (cm)', 'Weight (kg)', 'Gender']]
y = data['Competition Time (s)']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Hacer predicciones
y_pred = modelo.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Error cuadrático medio: {mse}')
print(f'R2 Score: {r2}')

# Función para generar el reporte
def generar_reporte(nombre, altura, peso, genero, tiempos_pasados):
    # Tiempo estimado
    tiempo_estimado = modelo.predict(np.array([[altura, peso, genero]]))[0]
    
    # Comparación con Benchmarks
    benchmarks = data.groupby('Gender')['Competition Time (s)'].mean()
    
    # Seguimiento del Progreso
    if tiempos_pasados:
        plt.plot(tiempos_pasados, marker='o')
        plt.title(f'Progreso de {nombre}')
        plt.xlabel('Competencias')
        plt.ylabel('Tiempo (s)')
        plt.grid(True)
        plt.show()

    # Predicciones en Competencias
    predicciones = modelo.predict(X_test)
    r2 = r2_score(y_test, predicciones)
    
    # Puntos Fuertes y Débiles
    diferencia = tiempo_estimado - benchmarks[genero]
    puntos_fuertes = 'Buena técnica y constancia en entrenamientos.'
    puntos_debiles = 'Necesita mejorar para alcanzar el promedio de su categoría.'

    if diferencia < 0:
        puntos_fuertes += f' {nombre} tiene un tiempo mejor que el promedio.'
    else:
        puntos_debiles += f' {nombre} necesita mejorar para alcanzar el promedio.'

    # Imprimir el reporte
    print(f'Reporte para {nombre}:')
    print(f'Tiempo Estimado: {tiempo_estimado:.2f} segundos')
    print(f'Comparación con Benchmarks: {diferencia:.2f} segundos del promedio')
    print(f'Seguimiento del Progreso: Ver gráfico')
    print(f'Predicciones en Competencias: R2 Score = {r2:.2f}')
    print(f'Puntos Fuertes: {puntos_fuertes}')
    print(f'Puntos Débiles: {puntos_debiles}')

# Ejemplo de uso:
generar_reporte('Juan Pérez', 180, 75, 0, [52.5, 51.8, 50.7])
