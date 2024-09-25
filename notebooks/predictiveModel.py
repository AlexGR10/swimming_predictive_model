# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:34:50 2024

@author: 20151

Archivo que genera un modelo predictivo
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pymongo
import pandas as pd

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]
collection = db["datos_nadadores"]
data = pd.DataFrame(list(collection.find()))

# Separar variables independientes y dependientes
X = data[['estatura', 'peso', 'IMC', 'flexibilidad']]
y = data['tiempo_mariposa']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Hacer predicciones
y_pred = modelo.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Error cuadrático medio: {mse}')
