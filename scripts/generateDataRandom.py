# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 22:46:47 2024

@author: 20151
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Cargar datos existentes desde MongoDB (simulación)
# En esta simulación, leemos un archivo CSV. En la práctica, lo leerías desde MongoDB
df = pd.read_csv('C://Users//20151//Documents//UNIVERSIDAD//9//BIG_DATA//swimming_predictive_model//data//datos_nadadores.csv')

# Definir listas de posibles valores para las variables adicionales
entrenadores = ['Entrenador A', 'Entrenador B', 'Entrenador C', 'Entrenador D']
lesiones = ['2021-01-15', '2022-06-20', '2023-02-10', '2020-11-01', '2019-05-25', 'Sin lesiones']
historial_competencias = ['5 competencias', '10 competencias', '15 competencias', '20 competencias', '25 competencias']

# Función para generar datos aleatorios
def generar_fecha_lesion():
    if random.choice([True, False]):
        return random.choice(lesiones[:-1])
    return lesiones[-1]

def generar_entrenador():
    return random.choice(entrenadores)

def generar_historial():
    return random.choice(historial_competencias)

# Función para generar datos de nadadores
def generar_nadadores(categoria, cantidad):
    data = []
    for _ in range(cantidad):
        nombre = f'Nadador_{categoria}_{random.randint(1, 1000)}'
        pais = random.choice(['USA', 'China', 'Russia', 'Brazil', 'Japan', 'Australia'])
        altura = random.uniform(160, 200)
        peso = random.uniform(60, 100)
        genero = random.choice([0, 1])
        tiempo_competencia = random.uniform(50, 60) if categoria == 'olimpico' else random.uniform(60, 70)
        fecha_evento = (datetime.today() - timedelta(days=random.randint(0, 365 * 5))).strftime('%d/%m/%Y')
        competencia = random.choice(['Olympic Games', 'Pan Pacific Championships', 'European Championships', 'World Championships', 'Swim USA'])
        posicion = random.randint(1, 10)
        edad_actual = random.randint(18, 35) if categoria == 'olimpico' else random.randint(15, 35)
        anos_competencia = random.randint(5, 10) if categoria == 'olimpico' else random.randint(1, 5)
        mejor_tiempo = random.uniform(50, 60)
        imc = peso / ((altura / 100) ** 2)
        horas_entrenamiento = random.randint(10, 20) if categoria == 'olimpico' else random.randint(5, 15)
        ultima_lesion = generar_fecha_lesion()
        entrenador = generar_entrenador()
        historial = generar_historial()
        
        data.append([nombre, pais, altura, peso, genero, tiempo_competencia, fecha_evento, competencia, posicion, edad_actual, anos_competencia, mejor_tiempo, imc, horas_entrenamiento, ultima_lesion, entrenador, historial])
    
    return pd.DataFrame(data, columns=['Name', 'Country', 'Height (cm)', 'Weight (kg)', 'Gender', 'Competition Time (s)', 'Event Date', 'Competition', 'Position', 'Current Age', 'Competition Years', 'Best Time (s)', 'IMC', 'Training Hours/Week', 'Last Injury', 'Entrenador', 'Historial de competencias'])

# Generar datos para profesionales y amateurs
df_profesional = generar_nadadores('profesional', 200)
df_amateur = generar_nadadores('amateur', 200)

# Concatenar los DataFrames
df_completo = pd.concat([df, df_profesional, df_amateur], ignore_index=True)

# Guardar el DataFrame actualizado
df_completo.to_csv('C://Users//20151//Documents//UNIVERSIDAD//9//BIG_DATA//swimming_predictive_model//data//todos_los_nadadores_actualizado.csv', index=False)

print(df_completo.head())
print("Datos generados y guardados con éxito.")
