import requests

url = 'http://127.0.0.1:5000/register'
data = {
    "user": "zarah08",
    "nombre": "Zarah Cornejo",
    "email": "zarah08@gmail.com",
    "password": "zarah1234",
    "confirm_password": "zarah1234",
    "gender": "female"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Imprimir solo si la respuesta es JSON válida
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta no es JSON válida.")
