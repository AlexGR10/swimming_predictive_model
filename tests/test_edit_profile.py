import requests

# Añadir o actualizar un registro de pruebas
response = requests.post(
    'http://127.0.0.1:5000/edit_profile',
    json={
        "user": "alexg10",
        "updates": {
            "pruebas": {
                "date": "16/12/2024",
                "time": "2'15''"
            }
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
