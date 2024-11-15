# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 08:55:46 2024

@author: 20151

Análisis de correlación para el conjunto de datos de nadadores.
"""

import pandas as pd
import numpy as np  # Importar NumPy
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]
collection = db["datos_nadadores"]
data = pd.DataFrame(list(collection.find()))

# Asegurarse de que las columnas sean numéricas
data['Height (cm)'] = pd.to_numeric(data['Height (cm)'], errors='coerce')
data['Weight (kg)'] = pd.to_numeric(data['Weight (kg)'], errors='coerce')
data['Competition Time (s)'] = pd.to_numeric(data['Competition Time (s)'], errors='coerce')
data['Gender'] = pd.to_numeric(data['Gender'], errors='coerce')
data['Current Age'] = pd.to_numeric(data['Current Age'], errors='coerce')
data['Competition Years'] = pd.to_numeric(data['Competition Years'], errors='coerce')
data['Best Time (s)'] = pd.to_numeric(data['Best Time (s)'], errors='coerce')
data['IMC'] = pd.to_numeric(data['IMC'], errors='coerce')
data['Training Hours/Week'] = pd.to_numeric(data['Training Hours/Week'], errors='coerce')

# Convertir la fecha del evento a un formato de fecha y extraer el año y mes
data['Event Date'] = pd.to_datetime(data['Event Date'], dayfirst=True, errors='coerce')
data['Year'] = data['Event Date'].dt.year
data['Month'] = data['Event Date'].dt.month

# Convertir las variables categóricas 'Competition', 'Country', 'Entrenador' y 'Historial de competencias' en variables dummy
data = pd.get_dummies(data, columns=['Competition', 'Country', 'Entrenador', 'Historial de competencias'], drop_first=True)

# Eliminar filas con datos faltantes
data = data.dropna()

# Filtrar solo columnas numéricas para la correlación
numeric_data = data.select_dtypes(include=[np.number])

# Comprobar la correlación entre variables
correlation_matrix = numeric_data.corr()

# Imprimir la matriz de correlación
print(correlation_matrix)

# Visualizar la matriz de correlación
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Matriz de Correlación')
plt.show()
