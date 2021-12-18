import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import pickle
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np 
import geopy.distance
from dash.dependencies import Output, Input, State
from app import app

rf_distance = pd.read_csv('afford_assets/rf_distance.csv')
smh_centroid = pd.read_csv('afford_assets/smh_centroid.csv')
rf_metroMeanPrice = 0

distance_areas_list = ['Distance_from_Atlanta', 'Distance_from_Richmond', 'Distance_from_Charleston', 'Distance_from_Northern Virginia',
           'Distance_from_Charlottesville','Distance_from_Maryland','Distance_from_Raleigh','Distance_from_Charlotte',
           'Distance_from_Greenville/Spartanburg','Distance_from_Orlando','Distance_from_Aiken/Augusta','Distance_from_Columbia']

afford_layout = html.Div([
     html.Div([
        dbc.Row([
            dbc.Col([
                html.P("Specify Metro Area", style={'padding-top':'5px','padding-bottom':'10px'})
            ], width=12)
        ]),
    ]),
    html.Div([
        dcc.Dropdown(
            id='area-dropdown',
            options=[
                {'label': 'Aiken/Augusta', 'value': 'Aiken/Augusta'},
                {'label': 'Atlanta', 'value': 'Atlanta'},
                {'label': 'Charleston', 'value': 'Charleston'},
                {'label': 'Charlotte', 'value': 'Charlotte'},
                {'label': 'Charlottesville', 'value': 'Charlottesville'},
                {'label': 'Columbia', 'value': 'Columbia'},
                {'label': 'Greenville/Spartanburg', 'value': 'Greenville/Spartanburg'},
                {'label': 'Maryland', 'value': 'Maryland'},
                {'label': 'Northern Virginia', 'value': 'Northern Virginia'},
                {'label': 'Orlando', 'value': 'Orlando'},
                {'label': 'Raleigh', 'value': 'Raleigh'},
                {'label': 'Richmond', 'value': 'Richmond'},
            ],
            value='Aiken/Augusta'
        ),
        html.Div(id='display-area')
    ]),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.P("Specify Distance from Metro Area", style={'padding-top':'30px','padding-bottom':'10px'})
            ], width=12)
        ]),
    ]),
    html.Div([
        dcc.Slider(
            id='distance-dropdown',
            min=0,
            max=200,
            step=1,
            value=20,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Div(id='display-distance')
    ]),
     html.Div([
        dbc.Row([
            dbc.Col([
                html.P("", style={'padding-top':'30px','padding-bottom':'10px'})
            ], width=12)
        ]),
    ]),
    dbc.Col(
        html.Div([
            html.Br(),
            html.P('Average resale home price in this area: ',style={'display':'inline-block','white-space': 'pre'}),
            html.P(id='display-resale-price',style={'display':'inline-block','font-weight':'bold'}),
            html.Br(),
            html.H5(id='display-resale-year'),
            html.Br(),
            html.H5(id='display-expected-resale-premium'),
            html.Br(),
            html.H5(id='display-actual-resale-premium'),
            html.Br(),
            html.H5(id='display-score'),
        ]),
    ),
])


# @app.callback(
#     Output('display-area', 'children'),
#     Input('area-dropdown', 'value'))
# def area_selected(selected_area):
#     return f'You have selected the {selected_area} area'

@app.callback(
    Output('display-distance', 'children'),
    Input('distance-dropdown', 'value'))
def distance_selected(selected_distance):
    return f'You have selected {selected_distance} Miles'





@app.callback(
    [
        Output('display-resale-price', 'children'),
        Output('display-resale-year', 'children'),
        Output('display-expected-resale-premium', 'children'),
        Output('display-actual-resale-premium', 'children'),
        Output('display-score', 'children')
    ],
    Input('area-dropdown', 'value'),
    Input('distance-dropdown', 'value'))
def affordability(selected_area,selected_distance) :
    # gets only smh homes in inputted area
    smh_metro = smh_centroid[smh_centroid['Area'] == selected_area]
        
    # if input isn't florida then get rid of all FL Refin homes (saves time)
    if selected_area != 'Orlando' :
        rf_metro = rf_distance[rf_distance['STATE OR PROVINCE'] != 'FL']
    else :  rf_metro = rf_distance[rf_distance['STATE OR PROVINCE'] == 'FL']

    chosen_column = []
    for area in distance_areas_list :
        if area.split('_')[2] == selected_area :
            chosen_column = area

    selected_distance = int(selected_distance)
    rf_metro = rf_distance[rf_distance[chosen_column] < selected_distance]

    # if no homes produce error msg
    if len(rf_metro) < 1 | len(smh_metro) :
        resale_price = 'No homes in this radius, pick a larger radius'
        resale_yr = ''
        resale_expPrem = ''
        resale_actPrem = ''
        score = ''
        return resale_price, resale_yr,resale_expPrem, resale_actPrem, score
    elif len(rf_metro) > 1 : 
        smh_metroMeanPrice = round(smh_metro["MedianSalesPrice"].mean())
        rf_metroMeanPrice = round(rf_metro["PRICE"].mean())
        rf_metroYearMean = 2021 - (round(rf_metro["YEAR BUILT"].mean()))
        actualResalePrem = round(((smh_metroMeanPrice - rf_metroMeanPrice) / rf_metroMeanPrice),2)
        
        if (rf_metroYearMean >= 0 and rf_metroYearMean <= 5) == True :
            rf_metroExpectPrem = .95
        elif (rf_metroYearMean >= 6 and rf_metroYearMean <= 10) == True :
            rf_metroExpectPrem = .9
        elif (rf_metroYearMean >= 11 and rf_metroYearMean <= 15) == True :
            rf_metroExpectPrem = .8
        elif (rf_metroYearMean >= 16 and rf_metroYearMean <= 20) == True :
            rf_metroExpectPrem = .75
        elif (rf_metroYearMean >= 21 and rf_metroYearMean <= 30) == True :
            rf_metroExpectPrem = .6
        elif (rf_metroYearMean >= 31 and rf_metroYearMean <= 40) == True :
            rf_metroExpectPrem = .5
        elif (rf_metroYearMean > 40) == True :
            rf_metroExpectPrem = .4
            
        expectedResalePrem = round(rf_metroMeanPrice * rf_metroExpectPrem)
        
        if actualResalePrem > expectedResalePrem :
            score = '1 Above Expected Premium'
        elif actualResalePrem < expectedResalePrem :
            score = '3 Below Expected Premium'
        elif actualResalePrem == expectedResalePrem :
            score = '2 In Line with Expected Premium'

        rf_metroMeanPrice = '{:,}'.format(rf_metroMeanPrice)
        # rf_metroYearMean = format(rf_metroMeanPrice , ',')
        # expectedResalePrem = format(rf_metroMeanPrice , ',')
        # actualResalePrem = format(rf_metroMeanPrice , ',')
        # score = format(rf_metroMeanPrice , ',')


        resale_price = f'${rf_metroMeanPrice}'
        resale_yr = f'Average resale home in this area is {rf_metroYearMean} years old'
        resale_expPrem = f'Expected resale premium is ${expectedResalePrem}'
        resale_actPrem = f'Actual resale premium is ${actualResalePrem}'
        score = f'The Relative Afford Score is {score}'
        
        return resale_price, resale_yr,resale_expPrem, resale_actPrem, score

        
    
    