import re
from app.utils.mongo import get_db
import pandas as pd
from joblib import load
import os

# Ruta del modelo
ruta_modelo = os.path.join(os.path.dirname(__file__), '..', 'models', 'modelo_svm.joblib') 
modelo_svm = load(ruta_modelo)

with open(os.path.join(os.path.dirname(__file__),  '..','models', 'columnas_df.txt'), 'r') as f:
    columnas_df = [line.strip() for line in f]

def login_user(username, password):
    db = get_db()
    user = db.usuarios.find_one({"user": username}, {'_id': 0})  # Excluir el campo _id

    if user and user['password'] == password:
        return {"message": "Login successful", "user_data": user}, 200
    else:
        return {"error": "Invalid username or password"}, 401

def is_valid_email(email):
    """Valida el formato del email usando una expresión regular"""
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None

def is_valid_gender(gender):
    """Valida que el género sea 'male' o 'female'"""
    return gender in ["male", "female"]

def register_user(user, nombre, email, password, confirm_password, gender, height_cm, weight_kg, competition_time_s, current_age, competition_years, best_time_s, imc, training_hours_week):
    db = get_db()
    # Verificar si el usuario ya existe
    if db.usuarios.find_one({"user": user}):
        return {"error": "User already exists"}, 400

    # Verificar si el email es válido
    if not is_valid_email(email):
        return {"error": "Invalid email address"}, 400

    # Verificar si el género es válido
    if not is_valid_gender(gender):
        return {"error": "Invalid gender, must be 'male' or 'female'"}, 400

    # Verificar si las contraseñas coinciden
    if password != confirm_password:
        return {"error": "Passwords do not match"}, 400

    # Crear un nuevo usuario
    nuevo_usuario = {
        "user": user,
        "nombre": nombre,
        "email": email,
        "password": password,
        "gender": gender,
        "biografia": "",
        "training": [],
        "pruebas": [],
        "categoria": "",  # Este campo será actualizado por el modelo
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "competition_time_s": competition_time_s,
        "current_age": current_age,
        "competition_years": competition_years,
        "best_time_s": best_time_s,
        "imc": imc,
        "training_hours_week": training_hours_week
    }

    # Insertar el nuevo usuario en la colección
    result = db.usuarios.insert_one(nuevo_usuario)
    nuevo_usuario['_id'] = str(result.inserted_id)  # Convertir ObjectId a cadena

    return {"message": "User registered successfully", "user_data": nuevo_usuario}, 201

def update_profile(username, updates):
    db = get_db()
    user = db.usuarios.find_one({"user": username})

    if not user:
        return {"error": "User not found"}, 404

    # Actualizar campos permitidos
    if "biografia" in updates:
        user["biografia"] = updates["biografia"]

    # Actualizar o añadir registros de entrenamiento
    if "training" in updates:
        training_update = updates["training"]
        existing_training = next((item for item in user.get("training", []) if item["date"] == training_update["date"]), None)
        if existing_training:
            existing_training["hours"] = training_update["hours"]
        else:
            if "training" not in user:
                user["training"] = []
            user["training"].append(training_update)

    # Actualizar o añadir registros de pruebas
    if "pruebas" in updates:
        pruebas_update = updates["pruebas"]
        existing_prueba = next((item for item in user.get("pruebas", []) if item["date"] == pruebas_update["date"]), None)
        if existing_prueba:
            existing_prueba["time"] = pruebas_update["time"]
        else:
            if "pruebas" not in user:
                user["pruebas"] = []
            user["pruebas"].append(pruebas_update)

    # Actualizar user (verificar que el nuevo user no exista ya)
    if "user" in updates:
        new_user = updates["user"]
        if db.usuarios.find_one({"user": new_user}):
            return {"error": "Username already exists"}, 400
        user["user"] = new_user

    # Actualizar nombre (verificar que no esté vacío)
    if "nombre" in updates:
        new_nombre = updates["nombre"]
        if not new_nombre.strip():
            return {"error": "Name cannot be empty"}, 400
        user["nombre"] = new_nombre

    # Actualizar email (verificar formato del email)
    if "email" in updates:
        new_email = updates["email"]
        if not is_valid_email(new_email):
            return {"error": "Invalid email address"}, 400
        user["email"] = new_email

    # Actualizar password (verificar que tenga al menos 8 caracteres)
    if "password" in updates:
        new_password = updates["password"]
        if len(new_password) < 8:
            return {"error": "Password must be at least 8 characters long"}, 400
        user["password"] = new_password

    # Actualizar gender (verificar que sea 'male' o 'female')
    if "gender" in updates:
        new_gender = updates["gender"]
        if not is_valid_gender(new_gender):
            return {"error": "Invalid gender, must be 'male' or 'female'"}, 400
        user["gender"] = new_gender

    if "height_cm" in updates:
        user["height_cm"] = updates["height_cm"]

    if "weight_kg" in updates:
        user["weight_kg"] = updates["weight_kg"]

    if "competition_time_s" in updates:
        user["competition_time_s"] = updates["competition_time_s"]

    if "current_age" in updates:
        user["current_age"] = updates["current_age"]

    if "competition_years" in updates:
        user["competition_years"] = updates["competition_years"]

    if "best_time_s" in updates:
        user["best_time_s"] = updates["best_time_s"]

    if "imc" in updates:
        user["imc"] = updates["imc"]

    if "training_hours_week" in updates:
        user["training_hours_week"] = updates["training_hours_week"]

    db.usuarios.update_one({"user": username}, {"$set": user})

    # Asegurarse de que siempre se devuelva una respuesta JSON válida
    user['_id'] = str(user['_id'])  # Convertir ObjectId a cadena si no se hizo ya
    return {"message": "Profile updated successfully", "user_data": user}, 200

def get_user_data(username):
    db = get_db()
    user = db.usuarios.find_one({"user": username}, {'_id': 0})  # Excluir el campo _id

    if not user:
        return {"error": "User not found"}, 404

    # Validar que los datos críticos para la predicción estén presentes
    required_fields = [
        "height_cm", "weight_kg", "competition_time_s", "current_age",
        "competition_years", "best_time_s", "imc", "training_hours_week",
        "gender"
    ]

    for field in required_fields:
        if field not in user:
            return {"error": f"Missing field: {field}"}, 400

    # Convertir gender a numérico (male -> 0, female -> 1)
    gender_numeric = 0 if user["gender"] == "male" else 1

    # Extraer los datos necesarios para la predicción
    nuevo_nadador = {
        "Height (cm)": user["height_cm"],
        "Weight (kg)": user["weight_kg"],
        "Competition Time (s)": user["competition_time_s"],
        "Current Age": user["current_age"],
        "Competition Years": user["competition_years"],
        "Best Time (s)": user["best_time_s"],
        "IMC": user["imc"],
        "Training Hours/Week": user["training_hours_week"],
        "Gender": gender_numeric
    }

    # Convertir nuevo_nadador a DataFrame
    nuevo_nadador_df = pd.DataFrame([nuevo_nadador])

    # Añadir cualquier columna faltante con valor por defecto 0
    for col in columnas_df:
        if col not in nuevo_nadador_df.columns:
            nuevo_nadador_df[col] = 0
    
    # Reordenar las columnas para que coincidan con las utilizadas durante el entrenamiento
    nuevo_nadador_df = nuevo_nadador_df[columnas_df]
    nuevo_nadador_df = nuevo_nadador_df.fillna(0)  # Rellenar NaN con ceros

    # Asegurarse de que los datos sean del tipo adecuado (convertir a int donde sea necesario)
    nuevo_nadador_df = nuevo_nadador_df.astype(float).astype(int)

    # Lógica para pasar los datos al modelo de predicción y obtener el resultado real
    prediction = predecir(nuevo_nadador_df, user["categoria"])

    return {"message": "Prediction generated successfully", "prediction": prediction}, 200

def predecir(nuevo_nadador_df, categoria_indicada):
    # Predicción con el modelo SVM
    prediccion_svm = modelo_svm.predict(nuevo_nadador_df)
    
    # Evaluar nadador
    username = nuevo_nadador_df.index[0]  # Suponiendo que el índice es el username
    categoria_real, es_campeon = evaluar_nadador(
        username,
        int(nuevo_nadador_df['Gender'].iloc[0]),
        int(nuevo_nadador_df['Current Age'].iloc[0]),
        float(nuevo_nadador_df['Competition Time (s)'].iloc[0])
    )
    
    return {
        "prediccion_svm": int(prediccion_svm[0]),
        "categoria_real": categoria_real,
        "es_campeon": bool(es_campeon)
    }

def evaluar_nadador(username, gender, current_age, competition_time_s):
    # Conectar a MongoDB para obtener los umbrales
    db = get_db()
    umbrales = db.umbrales.find_one()

    # Determinar el género como 'hombre' o 'mujer'
    genero = 'hombre' if gender == 0 else 'mujer'

    # Determinar el rango de edad
    if 18 <= current_age <= 24:
        rango_edad = "18-24"
    elif 25 <= current_age <= 35:
        rango_edad = "25-35"
    else:
        rango_edad = "36 y más"

    # Evaluar la categoría basada en los umbrales
    categoria_real = "Fuera de rango"
    for categoria, rangos in umbrales[genero].items():
        if rango_edad in rangos and rangos[rango_edad]['min'] <= competition_time_s <= rangos[rango_edad]['max']:
            categoria_real = categoria
            break

    # Actualizar la categoría del usuario en la base de datos
    db.usuarios.update_one({"user": username}, {"$set": {"categoria": categoria_real}})

    # Determinar si es campeón en la categoría calculada con margen de 2 segundos
    margen_segundos = 2.0
    es_campeon = competition_time_s < (umbrales[genero][categoria_real][rango_edad]["min"] + margen_segundos)

    return categoria_real, es_campeon