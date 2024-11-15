# train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score
import pymongo
from joblib import dump

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]

# Cargar datos de nadadores y umbrales
collection_nadadores = db["datos_nadadores"]
df = pd.DataFrame(list(collection_nadadores.find()))

collection_umbrales = db["umbrales"]
umbrales = collection_umbrales.find_one()

# Asegurarse de que las columnas sean numéricas
df['Height (cm)'] = pd.to_numeric(df['Height (cm)'], errors='coerce')
df['Weight (kg)'] = pd.to_numeric(df['Weight (kg)'], errors='coerce')
df['Competition Time (s)'] = pd.to_numeric(df['Competition Time (s)'], errors='coerce')
df['Current Age'] = pd.to_numeric(df['Current Age'], errors='coerce')
df['Competition Years'] = pd.to_numeric(df['Competition Years'], errors='coerce')
df['Best Time (s)'] = pd.to_numeric(df['Best Time (s)'], errors='coerce')
df['IMC'] = pd.to_numeric(df['IMC'], errors='coerce')
df['Training Hours/Week'] = pd.to_numeric(df['Training Hours/Week'], errors='coerce')
df['Gender'] = pd.to_numeric(df['Gender'], errors='coerce')
df['Position'] = pd.to_numeric(df['Position'], errors='coerce')

# Eliminar columnas innecesarias
df = df.drop(columns=['Last Injury', 'Nivel de Competencia', 'Categoria IMC'], errors='ignore')

# Eliminar filas con datos faltantes
df = df.dropna()

# Normalización de variables numéricas
variables_a_normalizar = ['Height (cm)', 'Weight (kg)', 'Competition Time (s)', 'Current Age', 
                          'Competition Years', 'Best Time (s)', 'IMC', 'Training Hours/Week']
df[variables_a_normalizar] = df[variables_a_normalizar] / df[variables_a_normalizar].max()

# Convertir variables categóricas a numéricas
df = pd.get_dummies(df, columns=['Country', 'Competition', 'Entrenador', 'Historial de competencias'], drop_first=True)

# Guardar las columnas del DataFrame
columnas_df = df.drop(columns=['Name', 'Event Date', 'Position', '_id']).columns.tolist()
with open('columnas_df.txt', 'w') as f:
    for columna in columnas_df:
        f.write("%s\n" % columna)

# Separación de características y variable objetivo
df['champion'] = df['Position'].apply(lambda x: 1 if x == 1 else 0)

# Eliminamos columnas no numéricas y la columna '_id' generada por MongoDB
X = df.drop(['champion', 'Name', 'Event Date', 'Position', '_id'], axis=1, errors='ignore')
Y = df['champion']  # Variable objetivo

# Asegurarse de que todas las columnas de X sean numéricas
X = X.apply(pd.to_numeric, errors='coerce')

# Verificación y eliminación de valores NaN
X = X.dropna()

# Manejar clases desbalanceadas usando oversampling
from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
x_train, y_train = smote.fit_resample(X, Y)

# División de los datos en entrenamiento y prueba
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.3, random_state=42, stratify=y_train)

# Modelo SVM
modelo_svm = svm.SVC(C=1.0, kernel='rbf', gamma='scale', probability=True)
modelo_svm.fit(x_train, y_train)

# Evaluación del modelo
y_pred_svm = modelo_svm.predict(x_test)
acc_svm = accuracy_score(y_test, y_pred_svm)
print(f"Precisión del modelo SVM: {acc_svm:.2f}")

# Guardar el modelo entrenado
dump(modelo_svm, 'modelo_svm.joblib')
print("Modelo SVM guardado exitosamente en 'modelo_svm.joblib'")
