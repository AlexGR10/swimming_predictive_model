import requests

url = 'http://127.0.0.1:5000/register'
data = {
    "user": "alexg10",
    "nombre": "Alejandro Gutierrez",
    "email": "alex10@gmail.com",
    "password": "alex1234",
    "confirm_password": "alex1234",
    "gender": "male",
    "height_cm": 184,
    "weight_kg": 85,
    "competition_time_s": 110,
    "current_age": 22,
    "competition_years": 3,
    "best_time_s": 105,
    "imc": 22.5,
    "training_hours_week": 11
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Imprimir solo si la respuesta es JSON válida
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta no es JSON válida.")
