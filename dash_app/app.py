# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:35:46 2024

@author: 20151

Archivo que genera un dashboard para visualizar los datos
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pymongo
import plotly.express as px

# Conectar a MongoDB
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
