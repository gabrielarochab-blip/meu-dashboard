# @title
# Baixar o Excel do Google Drive via gdown
import gdown

file_id = '1kpu5R_kTpI18SEftFl-B8qM0wVd_kO2D'
output = 'dados_mapa_dash.xlsx'
gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False)

# Ler Excel
import pandas as pd
df = pd.read_excel(output, engine='openpyxl')

# Criar app com Dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)
app.title = "Dashboard Programas Esportivos"

# Layout
app.layout = html.Div([
    html.H2("📍 Dashboard de Programas Esportivos", style={
        'textAlign': 'center',
        'marginTop': '20px',
        'marginBottom': '20px',
        'fontFamily': 'Arial',
        'color': '#2c3e50'
    }),

    html.Div([
        html.Div([
            html.Label("Filtrar por CRE", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in sorted(df['CRE'].dropna().unique())],
                id='cre-dropdown',
                placeholder="Todos"
            )
        ], style={'width': '48%', 'display': 'inline-block', 'paddingRight': '10px'}),

        html.Div([
            html.Label("Filtrar por Modalidade", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in sorted(df['Modalidade'].dropna().unique())],
                id='mod-dropdown',
                placeholder="Todos"
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ], style={'padding': '0 20px 20px 20px'}),

    dcc.Graph(id='mapa')
], style={'backgroundColor': '#f9f9f9'})

# Callback
@app.callback(
    Output('mapa', 'figure'),
    [Input('cre-dropdown', 'value'),
     Input('mod-dropdown', 'value')]
)
def update_map(cre_value, mod_value):
    filtered_df = df.copy()
    if cre_value:
        filtered_df = filtered_df[filtered_df['CRE'] == cre_value]
    if mod_value:
        filtered_df = filtered_df[filtered_df['Modalidade'] == mod_value]

    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Nome do professor",
        hover_data={
            "Programa": True,
            "Modalidade": True,
            "IE vínculada ao programa": True,
            "Latitude": False,
            "Longitude": False
        },
        color="Programa",
        zoom=10,
        height=600
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_title_text='Programa'
    )

    return fig

# Rodar o app

import os

port = int(os.environ.get("PORT", 8050))
app.run(host="0.0.0.0", port=port, debug=False)

