# -*- coding: utf-8 -*-
"""Created on Wed Sep 25 16:31:36 2024
@author: 20151
Archivo que carga datos de USA Swimming Association desde un CSV hacia Mongo DB"""

import pymongo
import pandas as pd

# Conectar a MongoDB
try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["natacion"]
    collection = db["datos_nadadores"]
    print("Conexión a MongoDB exitosa.")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")

# Cargar datos desde un archivo CSV
try:
    data = pd.read_csv('C://Users//20151//Documents//UNIVERSIDAD//9//BIG_DATA//swimming_predictive_model//data//datos_nadadores.csv')
    data_dict = data.to_dict("records")

    # Insertar datos en MongoDB
    collection.insert_many(data_dict)
    print("Datos cargados en MongoDB exitosamente.")
except Exception as e:
    print(f"Error al cargar datos en MongoDB: {e}")
