import os
from joblib import load
import pandas as pd

ruta_modelo = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'modelo_svm.joblib')
modelo_svm = load(ruta_modelo)

def predecir(nuevo_nadador, categoria_indicada):
    nuevo_nadador_df = normalizar_datos(nuevo_nadador, columnas_df)
    prediccion_svm = modelo_svm.predict(nuevo_nadador_df)
    categoria_real, es_campeon = evaluar_nadador(
        nuevo_nadador['Gender'],
        nuevo_nadador['Current Age'],
        nuevo_nadador['Competition Time (s)'],
        categoria_indicada
    )
    return prediccion_svm, categoria_real, es_campeon
