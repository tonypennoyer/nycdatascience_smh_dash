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

rf_distance = pd.read_csv('rf_distance.csv')
smh_centroid = pd.read_csv('smh_centroid.csv')
metroCentroidGuide = pd.read_csv('centroid_guide.csv')
rf_metroMeanPrice = 0

afford_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Affordability")
        ], width=12)
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
        dcc.Dropdown(
            id='distance-dropdown',
            options=[
                {'label': 'Less than 5 miles', 'value': '5'},
                {'label': '10 Miles', 'value': '10'},
                {'label': '25 Miles', 'value': '25'},
                {'label': '50 Miles', 'value': '50'},
                {'label': '100 Miles', 'value': '100'},
                {'label': '250 Miles', 'value': '250'},
                {'label': '500 Miles', 'value': '500'},
            ],
            value='10'
        ),
        html.Div(id='display-distance')
    ]),
    dbc.Col(
        html.Div([
            html.P(id='display-area'),
            html.Hr(),
            html.P(id='display-distance'),
            html.Br(),
            html.P(id='display-affordability'),
        ]),
    ),
    html.Hr(),
])


@app.callback(
    Output('display-area', 'children'),
    Input('area-dropdown', 'value'))
def area_selected(selected_area):
    return f'You have selected the {selected_area} area'

@app.callback(
    Output('display-distance', 'children'),
    Input('distance-dropdown', 'value'))
def distance_selected(selected_distance):
    return f'You have selected {selected_distance} Miles'





@app.callback(
    Output('display-affordability', 'children'),
    Input('area-dropdown', 'value'),
    Input('distance-dropdown', 'value'))
def affordability(selected_area,selected_distance, rf_metroMeanPrice=rf_metroMeanPrice) :
    selected_distance = int(selected_distance)
    radiusInput = float(selected_distance) * 1.60934
    radiusInput = int(radiusInput)

    # gets only smh homes in inputted area
    smh_metro = smh_centroid[smh_centroid['Area'] == selected_area]

    # if input isn't florida then get rid of all FL Refin homes (saves time)
    if selected_area != 'Orlando' :
        rf_metro = rf_distance[rf_distance['STATE OR PROVINCE'] != 'FL']
    else :  rf_metro = rf_distance[rf_distance['STATE OR PROVINCE'] == 'FL']

    # Get the centroid of inputted metro area
    gotCentroid = metroCentroidGuide[metroCentroidGuide['Area'] == selected_area]
    gotCentroid = gotCentroid['centroid'].item()
    # map that centroid to column
    rf_metro['centroid'] = [gotCentroid] * len(rf_metro)
    # perform distance calculation
    rf_metro['distance'] = rf_metro.apply(lambda x: geopy.distance.geodesic(x.lat_long, x.centroid), axis = 1)

    # clean distance
    rf_metro['distance'] = rf_metro['distance'].astype(str)
    rf_metro['distance'] = rf_metro['distance'].str.rstrip(' km')
    rf_metro['distance'] = rf_metro['distance'].astype(float)
    rf_metro['distance'] = rf_metro['distance'].round(2)
    rf_metro = rf_metro[rf_metro['distance'] < selected_distance]

    # if no homes produce error msg
    if len(rf_metro) < 1 | len(smh_metro) :
        print('No homes in this radius, pick a larger radius')
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
        
            
        return f'Average resale home price in this area is ${rf_metroMeanPrice}'
        return f'Average resale home in this area is {rf_metroYearMean} years old'
        print(f'Expected resale premium is {expectedResalePrem}')
        print(f'Actual resale premium is ${actualResalePrem}')
        print(f'The Relative Afford Score is {score}')
