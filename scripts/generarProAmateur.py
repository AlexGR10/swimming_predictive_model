# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 23:37:28 2024

@author: 20151
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Definir listas de posibles valores para las variables adicionales
entrenadores = ['Entrenador A', 'Entrenador B', 'Entrenador C', 'Entrenador D']
lesiones = ['2021-01-15', '2022-06-20', '2023-02-10', '2020-11-01', '2019-05-25', 'Sin lesiones']
historial_competencias = ['5 competencias', '10 competencias', '15 competencias', '20 competencias', '25 competencias']
paises = ['USA', 'China', 'Russia', 'Brazil', 'Japan', 'Australia']
competencias = ['National Championships', 'Regional Meet', 'State Meet', 'Local Meet']

# Definir los umbrales
umbrales_olimpico = {
    'hombre': {
        '18-24': (49.34, 59.29),
        '25-35': (48.81, 58),
        '36 y más': (49.23, 57.76),
    },
    'mujer': {
        '18-24': (50.69, 59.17),
        '25-35': (49.49, 62.99),
        '36 y más': (48.6, 57.86),
    }
}

umbrales_pro = {
    'hombre': {
        '18-24': (56.74, 68.18),
        '25-35': (56.13, 66.70),
        '36 y más': (56.62, 66.42),
    },
    'mujer': {
        '18-24': (58.29, 68.04),
        '25-35': (56.91, 72.44),
        '36 y más': (55.89, 66.54),
    }
}

umbrales_amateur = {
    'hombre': {
        '18-24': (70.93, 85.23),
        '25-35': (70.16, 83.38),
        '36 y más': (70.78, 83.03),
    },
    'mujer': {
        '18-24': (72.86, 85.05),
        '25-35': (71.14, 90.55),
        '36 y más': (69.86, 83.18),
    }
}

# Función para generar un nadador
def generar_nadador(categoria, genero, grupo_edad, umbrales):
    nombre = f'Nadador_{categoria}_{random.randint(1, 1000)}'
    pais = random.choice(paises)
    altura = round(random.uniform(180, 195) if genero == 0 else random.uniform(168, 180), 2)
    peso = round(random.uniform(60, 100), 2)
    tiempo_competencia = round(random.uniform(*umbrales[genero == 0 and 'hombre' or 'mujer'][grupo_edad]), 2)
    fecha_evento = (datetime.today() - timedelta(days=random.randint(0, 365 * 2))).strftime('%d/%m/%Y')
    competencia = random.choice(competencias)
    posicion = random.randint(1, 10)
    edad_actual = random.randint(*[int(x) for x in grupo_edad.split('-')]) if '-' in grupo_edad else random.randint(36, 40)
    anos_competencia = random.randint(1, edad_actual - 15)
    mejor_tiempo = round(random.uniform(tiempo_competencia - 2, tiempo_competencia), 2)
    imc = round(peso / ((altura / 100) ** 2), 2)
    horas_entrenamiento = random.randint(10, 20) if categoria == 'profesional' else random.randint(5, 10)
    ultima_lesion = random.choice(lesiones)
    entrenador = random.choice(entrenadores)
    historial = random.choice(historial_competencias)
    
    return [nombre, pais, altura, peso, genero, tiempo_competencia, fecha_evento, competencia, posicion, edad_actual, anos_competencia, mejor_tiempo, imc, horas_entrenamiento, ultima_lesion, entrenador, historial, categoria.capitalize(), categorizar_imc(imc)]

# Función para categorizar por IMC
def categorizar_imc(imc):
    if imc < 18.5:
        return 'Bajo peso'
    elif 18.5 <= imc < 25:
        return 'Normal'
    elif 25 <= imc < 30:
        return 'Sobrepeso'
    else:
        return 'Obesidad'

# Generar datos para profesionales y amateurs
data_pro = []
data_amateur = []

# Generar registros para hombres y mujeres profesionales
for genero in [0, 1]:  # 0 para hombres, 1 para mujeres
    for grupo_edad in umbrales_pro['hombre'].keys():
        for _ in range(50):  # 50 hombres y 50 mujeres en cada grupo profesional y amateur
            data_pro.append(generar_nadador('profesional', genero, grupo_edad, umbrales_pro))
            data_amateur.append(generar_nadador('amateur', genero, grupo_edad, umbrales_amateur))

# Crear DataFrames y concatenar con el DataFrame original
columnas = ['Name', 'Country', 'Height (cm)', 'Weight (kg)', 'Gender', 'Competition Time (s)', 'Event Date', 'Competition', 'Position', 'Current Age', 'Competition Years', 'Best Time (s)', 'IMC', 'Training Hours/Week', 'Last Injury', 'Entrenador', 'Historial de competencias', 'Nivel de Competencia', 'Categoria IMC']
df_pro = pd.DataFrame(data_pro, columns=columnas)
df_amateur = pd.DataFrame(data_amateur, columns=columnas)

# Cargar el archivo original
df_original = pd.read_csv('C://Users//20151//Documents//UNIVERSIDAD//9//BIG_DATA//swimming_predictive_model//data//datos_nadadores.csv')

# Concatenar todos los DataFrames
df_completo = pd.concat([df_original, df_pro, df_amateur], ignore_index=True)

# Guardar el DataFrame actualizado
df_completo.to_csv('C://Users//20151//Documents//UNIVERSIDAD//9//BIG_DATA//swimming_predictive_model//data//todos_los_nadadores_actualizado.csv', index=False)

print("Datos generados y guardados con éxito.")
