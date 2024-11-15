import requests

url = 'http://127.0.0.1:5000/predict'
data = {
    "nadador": {
        "Height (cm)": 185,
        "Weight (kg)": 80,
        "Competition Time (s)": 69,
        "Current Age": 24,
        "Competition Years": 6,
        "Best Time (s)": 49.00,
        "IMC": 23.37,
        "Training Hours/Week": 20,
        "Gender": 0
    },
    "categoria": "profesional"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response Text:", response.text)
# Imprimir solo si la respuesta es JSON válida
try:
    print(response.json())
except requests.exceptions.JSONDecodeError:
    print("Error: La respuesta no es JSON válida.")
