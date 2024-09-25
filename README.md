# Predicción de Rendimiento en Natación Estilo Mariposa con Big Data

## Descripción
Este proyecto utiliza técnicas de Big Data y aprendizaje automático para predecir el rendimiento de nadadores en competencias de estilo mariposa. Se integran y analizan datos físicos de los atletas (como estatura, peso, índice de masa corporal, flexibilidad, entre otros) junto con los tiempos obtenidos en diversas distancias de mariposa. El objetivo es identificar patrones y relaciones entre las variables para generar predicciones más certeras sobre el rendimiento de los nadadores y su capacidad para alcanzar los primeros lugares en competencias.

## Estructura del Proyecto
- `data/`: Contiene los archivos CSV con los datos de los nadadores.
- `notebooks/`: Contiene los notebooks de Spyder para el análisis exploratorio de datos (EDA) y el desarrollo de modelos predictivos.
- `scripts/`: Contiene los scripts de Python para la carga de datos en MongoDB y el procesamiento de datos con Spark.
- `dash_app/`: Contiene la aplicación Dash para la visualización interactiva de los datos y las predicciones.
- `README.md`: Este archivo.

## Requisitos
- Anaconda
- Spyder
- MongoDB
- Hadoop
- Apache Spark
- Apache NiFi
- Python 3.x
- Bibliotecas de Python: pandas, numpy, scikit-learn, pymongo, dash, plotly

## Instalación
1. **Instalar Anaconda y Spyder**:
   - Descarga e instala Anaconda.
   - Abre Anaconda Navigator y lanza Spyder.

2. **Instalar MongoDB**:
   - Descarga e instala MongoDB.
   - Inicia el servidor de MongoDB.

3. **Instalar Hadoop y Spark**:
   - Descarga e instala Hadoop.
   - Descarga e instala Apache Spark.

4. **Instalar Apache NiFi**:
   - Descarga e instala Apache NiFi.

5. **Instalar Bibliotecas de Python**:
   - Abre una terminal en Anaconda y ejecuta:
     ```bash
     conda install pandas numpy scikit-learn pymongo dash plotly
     ```

## Uso
1. **Cargar Datos en MongoDB**:
   - Utiliza el script `scripts/load_data_to_mongodb.py` para cargar los datos en MongoDB.
     ```python
     import pymongo
     import pandas as pd

     # Conectar a MongoDB
     client = pymongo.MongoClient("mongodb://localhost:27017/")
     db = client["natacion"]
     collection = db["datos_nadadores"]

     # Cargar datos desde un archivo CSV
     data = pd.read_csv('data/datos_nadadores.csv')
     data_dict = data.to_dict("records")

     # Insertar datos en MongoDB
     collection.insert_many(data_dict)
     ```

2. **Procesar Datos con Spark**:
   - Utiliza el script `scripts/process_data_with_spark.py` para procesar los datos con Spark.
     ```python
     from pyspark import SparkContext, SparkConf

     conf = SparkConf().setAppName("NatacionMapReduce")
     sc = SparkContext(conf=conf)

     # Leer datos desde HDFS
     datos = sc.textFile("hdfs://ruta_al_archivo/datos_nadadores.csv")

     # Procesamiento MapReduce
     def map_func(line):
         fields = line.split(',')
         return (fields[0], float(fields[1]))

     def reduce_func(a, b):
         return a + b

     resultados = datos.map(map_func).reduceByKey(reduce_func)
     resultados.saveAsTextFile("hdfs://ruta_al_archivo/resultados")
     ```

3. **Análisis Exploratorio de Datos (EDA) en Spyder**:
   - Abre el notebook `notebooks/eda.py` en Spyder para realizar el análisis exploratorio de datos.
     ```python
     import pandas as pd
     import matplotlib.pyplot as plt

     # Cargar datos desde MongoDB
     client = pymongo.MongoClient("mongodb://localhost:27017/")
     db = client["natacion"]
     collection = db["datos_nadadores"]
     data = pd.DataFrame(list(collection.find()))

     # Análisis exploratorio
     print(data.describe())
     data.hist(bins=50, figsize=(20,15))
     plt.show()
     ```

4. **Desarrollo de Modelos Predictivos**:
   - Abre el notebook `notebooks/modelo_predictivo.py` en Spyder para desarrollar y entrenar los modelos predictivos.
     ```python
     from sklearn.model_selection import train_test_split
     from sklearn.linear_model import LinearRegression
     from sklearn.metrics import mean_squared_error

     # Separar variables independientes y dependientes
     X = data[['estatura', 'peso', 'IMC', 'flexibilidad']]
     y = data['tiempo_mariposa']

     # Dividir los datos en conjuntos de entrenamiento y prueba
     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

     # Entrenar el modelo
     modelo = LinearRegression()
     modelo.fit(X_train, y_train)

     # Hacer predicciones
     y_pred = modelo.predict(X_test)

     # Evaluar el modelo
     mse = mean_squared_error(y_test, y_pred)
     print(f'Error cuadrático medio: {mse}')
     ```

5. **Visualización de Datos con Dash**:
   - Ejecuta la aplicación Dash en `dash_app/app.py` para visualizar los datos y las predicciones.
     ```python
     import dash
     import dash_core_components as dcc
     import dash_html_components as html
     from dash.dependencies import Input, Output
     import pandas as pd
     import plotly.express as px

     # Cargar datos desde MongoDB
     client = pymongo.MongoClient("mongodb://localhost:27017/")
     db = client["natacion"]
     collection = db["datos_nadadores"]
     data = pd.DataFrame(list(collection.find()))

     # Crear la aplicación Dash
     app = dash.Dash(__name__)

     app.layout = html.Div([
         dcc.Graph(id='grafico'),
         dcc.Dropdown(
             id='dropdown',
             options=[{'label': col, 'value': col} for col in data.columns],
             value='estatura'
         )
     ])

     @app.callback(
         Output('grafico', 'figure'),
         [Input('dropdown', 'value')]
     )
     def update_graph(selected_column):
         fig = px.histogram(data, x=selected_column)
         return fig

     if __name__ == '__main__':
         app.run_server(debug=True)
     ```

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para discutir cualquier cambio que te gustaría realizar.
