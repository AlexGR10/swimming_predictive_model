import os
from joblib import load
import pandas as pd
import numpy as np
import pymongo

# Ruta absoluta para cargar el modelo entrenado
ruta_modelo = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'modelo_svm.joblib')
modelo_svm = load(ruta_modelo)

# Cargar las columnas del DataFrame de referencia
ruta_columnas = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'columnas_df.txt')
with open(ruta_columnas, 'r') as f:
    columnas_df = f.read().splitlines()

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]
collection_umbrales = db["umbrales"]
umbrales = collection_umbrales.find_one()

def normalizar_datos(nuevo_nadador, columnas_referencia):
    nuevo_nadador_normalizado = {key: value / columnas_referencia.get(key, 1) for key, value in nuevo_nadador.items() if key in columnas_referencia}
    nuevo_nadador_df = pd.DataFrame([nuevo_nadador_normalizado])
    # Asegurar que las columnas coincidan con las columnas usadas para entrenar el modelo
    nuevo_nadador_df = nuevo_nadador_df.reindex(columns=columnas_df, fill_value=0)

    # Convertir todas las columnas a tipo numérico
    nuevo_nadador_df = nuevo_nadador_df.apply(pd.to_numeric, errors='coerce').fillna(0)
    
    return nuevo_nadador_df

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

    categorias = ['olimpico', 'profesional', 'amateur']
    categoria_real = 'Sin Categoría'
    for categoria in categorias:
        umbral = umbrales[genero_clave][categoria][grupo_edad]
        if umbral['min'] <= tiempo <= umbral['max']:
            categoria_real = categoria.capitalize()
            break

    es_campeon = tiempo <= tiempo_campeon or (
        categoria_real != categoria_indicada and tiempo <= umbrales[genero_clave][categoria_real.lower()][grupo_edad]['max']
    )

    return categoria_real, es_campeon

def predecir(nuevo_nadador, columnas_referencia, categoria_indicada):
    nuevo_nadador_df = normalizar_datos(nuevo_nadador, columnas_referencia)
    prediccion_svm = modelo_svm.predict(nuevo_nadador_df)
    categoria_real, es_campeon = evaluar_nadador(
        nuevo_nadador['Gender'],
        nuevo_nadador['Current Age'],
        nuevo_nadador['Competition Time (s)'],
        categoria_indicada
    )
    return prediccion_svm, categoria_real, es_campeon
