import requests

# Solicitar una predicción para el usuario
response = requests.post(
    'http://127.0.0.1:5000/predict',
    json={
        "user": "alexg10"
    }
)
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Imprimir solo si la respuesta es JSON válida
try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta no es JSON válida.")
