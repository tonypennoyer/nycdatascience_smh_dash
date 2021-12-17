import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from app import app
import os
map_path = os.getcwd() + '\map_assets'

#--------------------------------------------------------------------------------------------------
#---------Definitions----------
# data = pd.read_csv(map_path+'\choro_data.csv')

eda_layout = html.Div(
    [
    # Title Row
    dbc.Row(dbc.Col(html.H3("Exploring Data"))),
    dbc.Row([
        dbc.Col([
            html.H5("Choose State:"),
            dcc.RadioItems(id='map-radio',
            options=[
                {'label': 'District of Columbia', 'value': 'DC'},
                {'label': 'Florida', 'value': 'FL'},
                {'label': 'Georgia', 'value': 'GA'},
                {'label': 'Maryland', 'value': 'MD'},
                {'label': 'North Carolina', 'value': 'NC'},
                {'label': 'South Carolina', 'value': 'SC'},
                {'label': 'Virginia', 'value': 'VA'},
                {'label': 'West Virginia', 'value': 'WV'}
            ],
            value='DC',
            labelStyle={'display': 'block'})
        ], width=3),
        dbc.Col([
            html.Iframe(id='map', width='100%', height='600')
        ], width=9),
    ]),
])

@app.callback(
    Output('map', 'srcDoc'), 
    Input('map-radio', 'value'))
def update_map(selected_state):
    choice = {
        'DC': '\map_DC.html',
        'FL': '\map_FL.html',
        'GA': '\map_GA.html',
        'MD': '\map_MD.html',
        'NC': '\map_NC.html',
        'SC': '\map_SC.html',
        'VA': '\map_VA.html',
        'WV': '\map_WV.html',
    }
    return open(map_path+choice[selected_state],'r').read()