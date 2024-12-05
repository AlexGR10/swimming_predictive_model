import requests

# Añadir o actualizar un registro de pruebas
response = requests.post(
    'http://127.0.0.1:5000/edit_profile',
    json={
        "user": "alexg10",
        "updates": {
            "competition_time_s": 69,
            "best_time_s" : 69
        }
    }
)
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Imprimir solo si la respuesta es JSON válida
try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta no es JSON válida.")
