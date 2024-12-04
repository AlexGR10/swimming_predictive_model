import re
from app.utils.mongo import get_db

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

def register_user(user, nombre, email, password, confirm_password, gender):
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
        "password": password,  # Almacenar la contraseña en texto plano
        "gender": gender,
        "biografia": "",
        "training": [],
        "pruebas": [],
        "categoria": ""  # Este campo será actualizado por el modelo
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

    db.usuarios.update_one({"user": username}, {"$set": user})

    # Asegúrate de que siempre se devuelva una respuesta JSON válida
    user['_id'] = str(user['_id'])  # Convertir ObjectId a cadena si no se hizo ya
    return {"message": "Profile updated successfully", "user_data": user}, 200

def get_user_data(username):
    db = get_db()
    user = db.usuarios.find_one({"user": username}, {'_id': 0})  # Excluir el campo _id

    if not user:
        return {"error": "User not found"}, 404

    # Validar que los datos críticos para la predicción estén presentes
    required_fields = ["nombre", "email", "gender", "biografia", "training", "pruebas", "categoria"]
    for field in required_fields:
        if field not in user:
            return {"error": f"Missing field: {field}"}, 400

    # Aquí iría la lógica para pasar los datos al modelo de predicción y obtener el resultado
    # Simularemos una predicción simple como ejemplo
    prediction = {
        "prediccion": "Este es un resultado simulado de tu modelo de predicción."
    }

    return {"message": "Prediction generated successfully", "prediction": prediction}, 200
