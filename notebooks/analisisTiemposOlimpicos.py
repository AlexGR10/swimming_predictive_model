# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 02:30:24 2024

@author: 20151
"""

import pandas as pd

# Leer el archivo CSV con el delimitador correcto
ruta_csv = 'C://Users//20151//Documents//UNIVERSIDAD//9//BIG_DATA//swimming_predictive_model//data//datos_nadadores.csv'
df = pd.read_csv(ruta_csv, delimiter=',')

# Imprimir las columnas del DataFrame para verificar
print("Columnas del DataFrame:", df.columns)

# Definir las categorías y grupos de edad
categorias = df['Nivel de Competencia'].unique()
grupos_edad = {
    '18-24': (18, 24),
    '25-35': (25, 35),
    '36 y más': (36, float('inf'))
}

# Diccionario para almacenar los tiempos mínimos y máximos
umbrales = {
    'hombre': {cat: {edad: {'min': float('inf'), 'max': 0} for edad in grupos_edad} for cat in categorias},
    'mujer': {cat: {edad: {'min': float('inf'), 'max': 0} for edad in grupos_edad} for cat in categorias}
}

# Iterar sobre cada fila en el DataFrame
for _, row in df.iterrows():
    genero = 'hombre' if row['Gender'] == 0 else 'mujer'
    edad = row['Current Age']
    tiempo = row['Competition Time (s)']
    categoria = row['Nivel de Competencia']

    # Determinar el grupo de edad
    for grupo_edad, (edad_min, edad_max) in grupos_edad.items():
        if edad_min <= edad <= edad_max:
            # Actualizar los umbrales mínimos y máximos
            umbrales[genero][categoria][grupo_edad]['min'] = min(umbrales[genero][categoria][grupo_edad]['min'], tiempo)
            umbrales[genero][categoria][grupo_edad]['max'] = max(umbrales[genero][categoria][grupo_edad]['max'], tiempo)
            break

# Imprimir los resultados
for genero in umbrales:
    print(f"Umbrales para {genero}:")
    for categoria in umbrales[genero]:
        print(f"  Categoría: {categoria}")
        for grupo_edad in umbrales[genero][categoria]:
            umbral = umbrales[genero][categoria][grupo_edad]
            print(f"    Grupo de Edad: {grupo_edad}, Min: {umbral['min']:.2f}, Max: {umbral['max']:.2f}")

# Guardar los resultados en un archivo JSON si lo necesitas
import json
with open('umbrales_actualizados.json', 'w') as f:
    json.dump(umbrales, f, indent=4)
