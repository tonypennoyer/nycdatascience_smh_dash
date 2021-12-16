import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import os
assets_path = os.getcwd() +'/model_assets'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, assets_folder=assets_path,
                suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = app.server