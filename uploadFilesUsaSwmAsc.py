# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:31:36 2024

@author: 20151

Archivo que carga datos de USA Swimming Association desde un CSV
hacia Mongo DB
"""

import pymongo
import pandas as pd

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]
collection = db["datos_nadadores"]

# Cargar datos desde un archivo CSV
data = pd.read_csv('ruta_al_archivo/datos_nadadores.csv')
data_dict = data.to_dict("records")

# Insertar datos en MongoDB
collection.insert_many(data_dict)

print("Datos cargados en MongoDB exitosamente.")
