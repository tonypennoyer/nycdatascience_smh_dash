import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from app import app


predict_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("predictions")
        ], width=12)
    ]),
])