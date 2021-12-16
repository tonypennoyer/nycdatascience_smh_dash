import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from app import app


about_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Collaborators",style={'padding-top': '20px'}), 
            # html.H3('Jack Copeland',style={'white-space' : 'nowrap','display': 'inline-block','overflow': 'hidden','text-align' : 'center'}),
            # html.H3("Nicole Wang",style={'white-space' : 'nowrap',  'clear': 'both','display': 'inline-block','overflow': 'hidden','text-align' : 'center'}), 
            # html.H3('Tony Pennoyer',style={'white-space' : 'nowrap',  'clear': 'both','display': 'inline-block','overflow': 'hidden','text-align' : 'right'}),
        ], width=12),
    ]),
    html.Hr(),
    dbc.Row([
        html.Div([
            html.H4('Daniel Nie',style={'display':'inline-block'}),
            dbc.Button("LinkedIn", outline=True, color="primary", className="me-1",href='https://www.linkedin.com/in/danielnie/',target="_blank",
                style={'margin-left': '20px','background-color': '#0e76a8','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
            dbc.Button("GitHub", outline=True, color="secondary", className="me-1",href='https://github.com/dnie44',target="_blank",
                style={'margin-left': '10px','background-color': '#808080','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
        ]),
    ]),
    dbc.Row([
        html.Div([
            html.H4('Jack Copeland',style={'padding-top': '35px','display':'inline-block'}),
            dbc.Button("LinkedIn", outline=True, color="primary", className="me-1",href='https://www.linkedin.com/in/jack-copeland-84417b124/',target="_blank",
                style={'margin-left': '20px','background-color': '#0e76a8','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
            dbc.Button("GitHub", outline=True, color="secondary", className="me-1",href='https://github.com/jackcopeland11',target="_blank",
                style={'margin-left': '10px','background-color': '#808080','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
        ]),
    ]),
    dbc.Row([
        html.Div([
            html.H4('Nicole Wang',style={'padding-top': '35px','display':'inline-block'}),
            dbc.Button("LinkedIn", outline=True, color="primary", className="me-1",href='https://www.linkedin.com/in/nickelworks/',target="_blank",
                style={'margin-left': '20px','background-color': '#0e76a8','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
            dbc.Button("GitHub", outline=True, color="secondary", className="me-1",href='https://github.com/nickelworks',target="_blank",
                style={'margin-left': '10px','background-color': '#808080','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
        ]),
    ]),
    dbc.Row([
        html.Div([
            html.H4('Tony Pennoyer',style={'padding-top': '35px','display':'inline-block'}),
            dbc.Button("LinkedIn", outline=True, color="primary", className="me-1",href='https://www.linkedin.com/in/tony-pennoyer/',target="_blank",
                style={'margin-left': '20px','background-color': '#0e76a8','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
            dbc.Button("GitHub", outline=True, color="secondary", className="me-1",href='https://github.com/tonypennoyer',target="_blank",
                style={'margin-left': '10px','background-color': '#808080','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
        ]),
    ]),
])

