import requests

url = 'http://127.0.0.1:5000/login'
data = {
    "user": "alexg10",
    "password": "alex1234"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response Text:", response.text)

# Imprimir solo si la respuesta es JSON válida
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta no es JSON válida.")
