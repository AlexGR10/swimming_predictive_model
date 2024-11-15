import pymongo

# Conectar a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["natacion"]

# Definir los nuevos umbrales
umbrales = {
    'hombre': {
        'olimpico': {
            '18-24': {'min': 20, 'max': 59.29},
            '25-35': {'min': 48.81, 'max': 58.00},
            '36 y más': {'min': 49.23, 'max': 57.76}
        },
        'profesional': {
            '18-24': {'min': 59.30, 'max': 68.08},
            '25-35': {'min': 58.01, 'max': 66.54},
            '36 y más': {'min': 57.77, 'max': 66.15}
        },
        'amateur': {
            '18-24': {'min': 68.09, 'max': 84.45},
            '25-35': {'min': 66.55, 'max': 82.96},
            '36 y más': {'min': 66.16, 'max': 152.49}
        }
    },
    'mujer': {
        'olimpico': {
            '18-24': {'min': 20.69, 'max': 59.17},
            '25-35': {'min': 49.49, 'max': 62.99},
            '36 y más': {'min': 48.60, 'max': 57.86}
        },
        'profesional': {
            '18-24': {'min': 59.18, 'max': 67.91},
            '25-35': {'min': 63.00, 'max': 72.41},
            '36 y más': {'min': 57.87, 'max': 66.30}
        },
        'amateur': {
            '18-24': {'min': 67.92, 'max': 85.04},
            '25-35': {'min': 72.42, 'max': 90.35},
            '36 y más': {'min': 66.31, 'max': 153.11}
        }
    }
}

# Acceder a la colección de umbrales
collection_umbral = db["umbrales"]

# Actualizar los umbrales en la colección
collection_umbral.replace_one({}, umbrales, upsert=True)
print("Umbrales actualizados en MongoDB exitosamente.")
