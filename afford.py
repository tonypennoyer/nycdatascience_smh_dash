import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_table
import pickle
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np 
import geopy.distance
from dash.dependencies import Output, Input, State
from app import app

rf_distance = pd.read_csv('afford_assets/rf_distance.csv',low_memory=False)
smh_centroid = pd.read_csv('afford_assets/smh_centroid.csv')
rf_metroMeanPrice = 0

distance_areas_list = ['Distance_from_Atlanta', 'Distance_from_Richmond', 'Distance_from_Charleston', 'Distance_from_Northern Virginia',
           'Distance_from_Charlottesville','Distance_from_Maryland','Distance_from_Raleigh','Distance_from_Charlotte',
           'Distance_from_Greenville/Spartanburg','Distance_from_Orlando','Distance_from_Aiken/Augusta','Distance_from_Columbia']
columns = [
            {"id": 0, "name": "Complaint ID"},
            {"id": 1, "name": 'Property Type'},
            {"id": 2, "name": 'Address'},
            {"id": 3, "name": 'City'},
            {"id": 4, "name": 'State'},
            {"id": 5, "name": 'Zipcode'},
            {"id": 6, "name": 'Price'},
            {"id": 7, "name": 'Beds'},
            {"id": 8, "name": 'Baths'},
]

afford_layout = html.Div([
    # Title Row
    dbc.Row(dbc.Col(html.H3("Affordability Index"))),
    html.Hr(),
    dbc.Row(
        [
        # Column1 - sidebar
        dbc.Col(
            html.Div([
            # Metro Dropdown Selector
            dcc.Dropdown(id='area-dropdown',
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
                placeholder="Select Metro Area", value='Richmond',
            ),
            html.Br(),
            html.P("Specify Radius"),
            dcc.Slider(
                id='distance-dropdown',
                min=0,
                max=100,
                step=1,
                value=20,
                tooltip={"placement": "bottom", "always_visible": True}),
            html.Br(),
            ])
        , width=4),

        dbc.Col(
            html.Div([
                html.P('Relative Afford Score: ',style={'white-space': 'pre'}),
                html.H3(id='display-score',style={'font-weight':'bold'}),
                html.Br(),
                html.Hr(),
                html.Br(),
                html.P('Average resale home value: ',style={'display':'inline-block','white-space': 'pre'}),
                html.P(id='display-resale-price',style={'display':'inline-block'}),
                html.Br(),
                html.P('Average resale home age: ',style={'display':'inline-block','white-space': 'pre'}),
                html.P(id='display-resale-year',style={'display':'inline-block'}),
                html.Br(),
                html.P('Expected resale premium: ',style={'display':'inline-block','white-space': 'pre'}),
                html.P(id='display-expected-resale-premium',style={'display':'inline-block'}),
                html.Br(),
                html.P('Actual resale premium: ',style={'display':'inline-block','white-space': 'pre'}),
                html.P(id='display-actual-resale-premium',style={'display':'inline-block'}),
                html.Br(),
            ])
        , width=5),
        dbc.Col(
            html.Div([
                html.P(id='display-area'),
                html.H4(id='display-distance',style={'padding-bottom':'5px'}),
                html.Br(),
                html.Hr(),
                html.P(id='display-house-num'),
            ])
        , width=3),
    ]),
    html.Hr(),
    html.Div([
        dash_table.DataTable(
            id='table-data',
            data=[],
            columns=[],
            page_size = 10,
            style_cell={'textAlign': 'center'},
            style_header={
            'backgroundColor': '#40522b18',
            'color': '#585858'
            },
            style_data={
                'backgroundColor': '#40603420',
                'color': '#585858'
            },
        ),
    ]),
    html.Div([
        html.P('* This data was scraped from Redfin in early December 2021',style={'font-style':'italic'}),
    ]),
])


@app.callback(
    Output('display-area', 'children'),
    Input('area-dropdown', 'value'))
def area_selected(selected_area):
    return f'{selected_area}'

@app.callback(
    Output('display-distance', 'children'),
    Input('distance-dropdown', 'value'))
def distance_selected(selected_distance):
    return f'{selected_distance} Miles'





@app.callback(
    [
        Output('display-resale-price', 'children'),
        Output('display-resale-year', 'children'),
        Output('display-expected-resale-premium', 'children'),
        Output('display-actual-resale-premium', 'children'),
        Output('display-score', 'children'),
        Output('display-house-num','children'),
        Output('table-data','data'),
        Output('table-data', 'columns')

    ],
    Input('area-dropdown', 'value'),
    Input('distance-dropdown', 'value'))
def affordability(selected_area,selected_distance) :
    # gets only smh homes in inputted area
    smh_metro = smh_centroid[smh_centroid['Area'] == selected_area]
        
    # if input isn't florida then get rid of all FL Refin homes (saves time)
    if selected_area != 'Orlando' :
        rf_metro = rf_distance[rf_distance['State'] != 'FL']
    else :  rf_metro = rf_distance[rf_distance['State'] == 'FL']

    chosen_column = []
    for area in distance_areas_list :
        if area.split('_')[2] == selected_area :
            chosen_column = area

    selected_distance = int(selected_distance)
    rf_metro = rf_distance[rf_distance[chosen_column] < selected_distance]

    # if no homes produce error msg
    if len(rf_metro) < 1 | len(smh_metro) :
        rf_metro = rf_metro.drop(['Unnamed: 0','SALE TYPE', 'DAYS ON MARKET',
            '$/SQUARE FEET', 'HOA/MONTH','Location', 'zip', 'lat_long','LOT SIZE',
            'Distance_from_Atlanta', 'Distance_from_Richmond',
            'Distance_from_Charleston', 'Distance_from_Northern Virginia',
            'Distance_from_Charlottesville', 'Distance_from_Maryland',
            'Distance_from_Raleigh', 'Distance_from_Charlotte',
            'Distance_from_Greenville/Spartanburg', 'Distance_from_Orlando',
            'Distance_from_Aiken/Augusta', 'Distance_from_Columbia'], axis=1)
        resale_price = 'No homes in this radius, pick a larger radius'
        resale_yr = ''
        resale_expPrem = ''
        resale_actPrem = ''
        score = ''
        house_num = ''
        table_data = rf_metro.to_dict('records')
        table_cols = [{"name": i, "id": i} for i in rf_metro.columns]
    
        return resale_price, resale_yr,resale_expPrem, resale_actPrem, score , house_num, table_data, table_cols
    elif len(rf_metro) > 1 : 
        smh_metroMeanPrice = round(smh_metro["MedianSalesPrice"].mean())
        rf_metroMeanPrice = round(rf_metro["Price"].mean())
        rf_metroYearMean = 2021 - (round(rf_metro["Year Built"].mean()))
        actualResalePrem = int(round(((smh_metroMeanPrice - rf_metroMeanPrice) / rf_metroMeanPrice),2)*100)
        
        if (rf_metroYearMean >= 0 and rf_metroYearMean <= 5) == True :
            rf_metroExpectPrem = 5
        elif (rf_metroYearMean >= 6 and rf_metroYearMean <= 10) == True :
            rf_metroExpectPrem = 10
        elif (rf_metroYearMean >= 11 and rf_metroYearMean <= 15) == True :
            rf_metroExpectPrem = 20
        elif (rf_metroYearMean >= 16 and rf_metroYearMean <= 20) == True :
            rf_metroExpectPrem = 25
        elif (rf_metroYearMean >= 21 and rf_metroYearMean <= 30) == True :
            rf_metroExpectPrem = 40
        elif (rf_metroYearMean >= 31 and rf_metroYearMean <= 40) == True :
            rf_metroExpectPrem = 50
        elif (rf_metroYearMean > 40) == True :
            rf_metroExpectPrem = 60
            
        expectedResalePrem = rf_metroExpectPrem
        
        if actualResalePrem > expectedResalePrem :
            score = '1 (Above Expected Premium)'
        elif actualResalePrem < expectedResalePrem :
            score = '3 (Below Expected Premium)'
        elif actualResalePrem == expectedResalePrem :
            score = '2 (In Line with Expected Premium)'

        rf_metroMeanPrice = '{:,}'.format(rf_metroMeanPrice)
        house_num_data = len(rf_metro)

        rf_metro = rf_metro.drop(['Unnamed: 0','SALE TYPE', 'DAYS ON MARKET',
            '$/SQUARE FEET', 'HOA/MONTH','Location', 'zip', 'lat_long','LOT SIZE',
            'Distance_from_Atlanta', 'Distance_from_Richmond',
            'Distance_from_Charleston', 'Distance_from_Northern Virginia',
            'Distance_from_Charlottesville', 'Distance_from_Maryland',
            'Distance_from_Raleigh', 'Distance_from_Charlotte',
            'Distance_from_Greenville/Spartanburg', 'Distance_from_Orlando',
            'Distance_from_Aiken/Augusta', 'Distance_from_Columbia'], axis=1)

        rf_metro = rf_metro.fillna('NaN')


        resale_price = f'${rf_metroMeanPrice}'
        resale_yr = f'{rf_metroYearMean} years old'
        resale_expPrem = f'{expectedResalePrem}%'
        resale_actPrem = f'{actualResalePrem}%'
        score = f'{score}'
        house_num = f'{house_num_data} homes'
        table_data = rf_metro.to_dict('records')
        table_cols = [{"name": i, "id": i} for i in rf_metro.columns]
    
        
        return resale_price, resale_yr,resale_expPrem, resale_actPrem, score, house_num, table_data, table_cols




        
    
    