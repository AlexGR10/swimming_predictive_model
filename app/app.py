from flask import Flask, request, jsonify
from modelo import predecir
import pandas as pd
import os

app = Flask(__name__)

# Cargar las columnas del DataFrame de referencia
ruta_columnas = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'columnas_df.txt')
with open(ruta_columnas, 'r') as f:
    columnas_df = f.read().splitlines()

# Datos ficticios para normalización
df = pd.DataFrame(columns=columnas_df).astype(float)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    nuevo_nadador = data.get('nadador')
    categoria_indicada = data.get('categoria')
    if not nuevo_nadador or not categoria_indicada:
        return jsonify({"error": "nadador and categoria are required"}), 400
    prediccion_svm, categoria_real, es_campeon = predecir(nuevo_nadador, df, categoria_indicada)
    return jsonify({
        'prediccion_svm': int(prediccion_svm[0]),
        'categoria_real': categoria_real,
        'es_campeon': es_campeon
    })

if __name__ == '__main__':
    app.run(debug=True)
