# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:33:41 2024

@author: 20151

Arcivo que ejecuta un análisis exploratorio de los datos
de la base de datos de Mongo DB
"""

import pandas as pd
import matplotlib.pyplot as plt
import pymongo

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]
collection = db["datos_nadadores"]
data = pd.DataFrame(list(collection.find()))

# Análisis exploratorio
print(data.describe())
data.hist(bins=50, figsize=(20,15))
plt.show()
