import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from app import app


about_layout = html.Div([
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.P(['As part of our capstone project, we made this dash to give Stanley Martin Homes insight into pricing their homes.', html.Br(),html.Br(),
                'We are Data Science Fellows at the NYC Data Science Academy.'],style={'display': 'inline-block',
                'text-transform' : 'none','padding-top': '15px'}),
            # html.H3("Nicole Wang",style={'white-space' : 'nowrap',  'clear': 'both','display': 'inline-block','overflow': 'hidden','text-align' : 'center'}), 
            # html.H3('Tony Pennoyer',style={'white-space' : 'nowrap',  'clear': 'both','display': 'inline-block','overflow': 'hidden','text-align' : 'right'}),
        ], width=12),
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H4("Collaborators",style={'padding-top': '5px','display':'inline-block','text-transform' : 'none'}), 
            # html.H3("Nicole Wang",style={'white-space' : 'nowrap',  'clear': 'both','display': 'inline-block','overflow': 'hidden','text-align' : 'center'}), 
            # html.H3('Tony Pennoyer',style={'white-space' : 'nowrap',  'clear': 'both','display': 'inline-block','overflow': 'hidden','text-align' : 'right'}),
        ], width=12),
    ]),
    dbc.Row([
        html.Div([
            html.Img(src="https://i.ibb.co/DCdcDdB/Git-Hub-Profile-Pic.jpg",style={'height':'63px','border-radius': '50%'}),
            html.H4('Daniel Nie',style={'margin-left': '20px','display':'inline-block','text-transform' : 'none','padding-top': '35px','padding-bottom': '10px'}),
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
            html.Img(src="https://i.ibb.co/R2fnbBg/profile-icon-png-898.png",style={'height':'63px','border-radius': '50%'}),
            html.H4('Jack Copeland',style={'margin-left': '20px','padding-top': '35px','display':'inline-block','text-transform' : 'none','padding-bottom': '10px'}),
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
            html.Img(src="https://i.ibb.co/ThrVy9C/IMG-0412-small.jpg",style={'height':'63px','border-radius': '50%'}),
            html.H4('Nicole Wang',style={'margin-left': '20px','padding-top': '35px','display':'inline-block','text-transform' : 'none','padding-bottom': '10px'}),
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
            html.Img(src="https://i.ibb.co/kcnMR5D/cropped.jpg",style={'height':'63px','border-radius': '50%'}),
            html.H4('Tony Pennoyer',style={'margin-left': '20px','text-transform' : 'none','padding-top': '35px','display':'inline-block','text-align':'center','padding-bottom': '35px'}),
            dbc.Button("LinkedIn", outline=True, color="primary", className="me-1",href='https://www.linkedin.com/in/tony-pennoyer/',target="_blank",
                style={'margin-left': '20px','background-color': '#0e76a8','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
            dbc.Button("GitHub", outline=True, color="secondary", className="me-1",href='https://github.com/tonypennoyer',target="_blank",
                style={'margin-left': '10px','background-color': '#808080','border': 'none','color': 'white','padding': '10px 24px','text-align': 'center',
                'border-radius': '5px','font-size': '16px','width': '150px','display': 'inline-block'}),
        ]),
    ]),
    # dbc.Row([
    #     html.Div([
    #         html.P(' We are currently Data Science Fellows at NYC Data Science Academy',style={'border-radius': '5px','width':'600px'}),
    #     ])
    # ]),
])

