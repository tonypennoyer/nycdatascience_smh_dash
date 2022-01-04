import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from app import app
from datetime import date
todays_date = date.today()

import os
model_path = os.getcwd() + '/model_assets'

import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from catboost import CatBoostRegressor
import numpy as np

#--------------------------------------------------------------------------------------------------
#---------Definitions----------
locs = pd.read_csv(model_path+'/locations.csv')
pickled_model = pickle.load(open(model_path+'/SMH_model.pkl', 'rb'))
zip_encoder = pickle.load(open(model_path+'/zip_encoder.pkl', 'rb'))
zip_model_data = pd.read_csv(model_path+'/zip_model_data.csv', index_col='ZipCode')
X_pred = pd.read_csv(model_path+'/X_base.csv', index_col=0, squeeze=True, dtype={'zip':'object'})
prop_encode = {'Single Family Residential':0,
               'Condo/Co-op':1,
               'Townhouse':2,
               'Multi-Family (2-4 Unit)':3,
               'Ranch':4,
               'Multi-Family (5+ Unit)':5}
clusters = pd.read_csv(model_path+'/clusters.csv', index_col='ZipCode')

# Prepares prediction inputs
X_pred = X_pred.append(zip_model_data.loc[20002])
X_pred['Prop_Type'] = prop_encode[X_pred['Prop_Type']]
X_pred['zip'] = zip_encoder.transform(pd.Series([20002]))[0]
#--------------------------------------------------------------------------------------------------
#---------Functions----------
def clean_num(integer):
    '''
    takes an integer and return a string representation of that integer with commas correctly separating groups of three digits
    '''
    if isinstance(integer, int):
        pass
    else:
        integer = int(round(integer))
    collector = []
    sub = ''
    for idx, char in enumerate(str(integer)[::-1]):
        if (idx+1)%3 != 0:
            sub += char
        else:
            sub += char
            collector.append(sub)
            sub = ''
    if sub == '':
        pass
    else:
        collector.append(sub)
    return ','.join(collector)[::-1]


predict_layout = html.Div( # Total Row Width = 12
    [    
    # Title Row
    dbc.Row(dbc.Col(html.H3("House Pricing Guideline"))),
    html.Hr(),
    dbc.Row(
        [
        # Column1 - sidebar
        dbc.Col(
            html.Div([
            # Metro Dropdown Selector
            dcc.Dropdown(id='msa-drop',
                options=[
                    {'label': msa, 'value': msa} for msa in locs.Metro_Area.unique()
                ],
                placeholder="Select Metro Area", value='Washington Arlington Alexandria'
            ),
            html.Br(),
            # ZipCode Dropdown Selector
            dcc.Dropdown(id='zip-drop',
                placeholder="Select ZIP Code",
            ),
            html.Br(),
            html.Hr(),
            # House Details
            html.P("Specify Type of Property"),
            dcc.Dropdown(id='proptype-drop',
                options=[
                    {'label': pt, 'value': pt} for pt in prop_encode.keys()
                ],
                placeholder="Select Property Type", value=list(prop_encode.keys())[0]
            ),
            html.Br(),
            html.P("Specify Square-Footage"),
            dcc.Slider(
                id='sf-slider',
                min=500,
                max=4000,
                step=1,
                value=1000,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Br(),
            html.P("Specify BEDs"),
            dcc.Slider(
                id='bed-slider',
                min=1,
                max=6,
                step=1,
                value=2,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Br(),
            html.P("Specify BATHs"),
            dcc.Slider(
                id='bath-slider',
                min=1,
                max=4,
                step=0.5,
                value=1,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Br(),
            html.P("Specify Year Built"),
            dcc.Slider(
                id='year-slider',
                min=1900,
                max=todays_date.year+2,
                step=1,
                value=todays_date.year,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            html.Br(),
            ])
        , width=4),
        
        # Column2 - Content
        dbc.Col(
            html.Div([
                html.P('Suggested Price Range:'),
                html.H2(id='model-price'),
                html.Br(),
                html.Hr(),
                html.Br(),
                html.P(id='display-proptype'),
                html.Plaintext(id='display-sf'),
                html.Plaintext(id='display-bed'),
                html.Plaintext(id='display-bath')
            ])
        , width=4),
        dbc.Col(
            html.Div([
                html.P(id='display-loc'),
                html.H4(id='display-ZIP'),
                html.Br(),
                html.Hr(),
                html.H4(id='display-cluster'),
                html.Br(),
                html.P("On average, houses in this cluster have the following characteristics: "),
                html.Plaintext(id = 'display-cluster-sf'),
                html.Plaintext(id = 'display-cluster-bedrooms'),
                html.Plaintext(id = 'display-cluster-bathrooms'),
                html.Plaintext(id = 'display-cluster-year'),
                html.Plaintext(id = 'display-cluster-pricepersf'),
                html.P("On average, zip codes in this cluster have the following characteristics: "),
                html.Plaintext(id = 'display-cluster-zip-income'),
                html.Plaintext(id = 'display-cluster-zip-population'),
                html.Plaintext(id = 'display-cluster-zip-numhouses')
            ])
        , width=4),
    ]),
    html.Hr(),
    # Testing
    dbc.Row([html.Plaintext("price prediction based on gradient boosting tree model trained on 80,000 datapoints")])
    
])

@app.callback(
    Output('zip-drop', 'options'),
    Input('msa-drop', 'value'))
def set_zip_options(selected_msa):
    zip_choices = locs.groupby('Metro_Area')['ZipCode'].agg(['unique']).loc[selected_msa][0]
    return [{'label': i, 'value': i} for i in zip_choices]

@app.callback(
    Output('zip-drop', 'value'),
    Input('zip-drop', 'options'))
def set_zip_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('display-loc', 'children'),
    Input('msa-drop', 'value'))
def set_display_loc(selected_msa):
    return f'{selected_msa}'

@app.callback(
    Output('display-ZIP', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    return f'ZipCode: {selected_zip}'

@app.callback(
    Output('display-cluster', 'children'),
    Input('zip-drop', 'value'))
def set_display_clust(selected_zip):
    clust_dict = {
        0:'Average',
        1:'Cheap',
        2:'Expensive',
        3:'Affordable'
    }
    return f'Cluster {int(clusters.loc[selected_zip,"cluster"])}: {clust_dict[int(clusters.loc[selected_zip,"cluster"])]}'

@app.callback(
    Output('display-cluster-bedrooms', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    return f'{np.round(clusters.loc[selected_zip,"avg_cluster_beds"],2)} Bedrooms'

@app.callback(
    Output('display-cluster-price', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    price = clusters.loc[selected_zip,"avg_cluster_price"]
    return f'Avg. Price: ${clean_num(round(price))}'

@app.callback(
    Output('display-cluster-pricepersf', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    price = clusters.loc[selected_zip,"avg_cluster_price_persf"]
    return f'Avg. Price per square foot: ${clean_num(round(price))}'

@app.callback(
    Output('display-cluster-bathrooms', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    return f'{np.round(clusters.loc[selected_zip,"avg_cluster_baths"],2)} Bathrooms'

@app.callback(
    Output('display-cluster-year', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    return f'Year Built: {np.round(clusters.loc[selected_zip,"avg_cluster_year"],2)}'

@app.callback(
    Output('display-cluster-zip-income', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    x = clusters.loc[selected_zip,"IncomePerHousehold"]
    return f'Income Per Household: ${clean_num(round(x))}'

@app.callback(
    Output('display-cluster-zip-population', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    return f'Population: {clean_num(round(clusters.loc[selected_zip,"Population"]))}'

@app.callback(
    Output('display-cluster-zip-numhouses', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    return f'Number of Houses: {clean_num(round(clusters.loc[selected_zip,"HouseholdsPerZipCode"]))}'


@app.callback(
    Output('display-cluster-sf', 'children'),
    Input('zip-drop', 'value'))
def set_display_loc(selected_zip):
    return f'{np.round(clusters.loc[selected_zip,"avg_cluster_sf"],2)} Sq. Ft.'

@app.callback(
    Output('display-proptype', 'children'),
    Input('proptype-drop', 'value'),
    Input('year-slider', 'value'))
def set_display_pt(selected_pt, selected_yr):
    return f'{selected_pt}: built in {selected_yr}'

@app.callback(
    Output('display-sf', 'children'),
    Input('sf-slider', 'value'))
def set_display_sf(selected_sf):
    return f'{selected_sf} Sq.Ft.'

@app.callback(
    Output('display-bed', 'children'),
    Input('bed-slider', 'value'))
def set_display_bed(selected_bed):
    return f'{selected_bed} Bedrooms'

@app.callback(
    Output('display-bath', 'children'),
    Input('bath-slider', 'value'))
def set_display_bath(selected_bath):
    return f'{selected_bath} Bathrooms'

@app.callback(
    Output('model-price', 'children'),
    Input('zip-drop', 'value'),
    Input('proptype-drop', 'value'),
    Input('sf-slider', 'value'),
    Input('bed-slider', 'value'),
    Input('bath-slider', 'value'),
    Input('year-slider', 'value'),
    )
def set_price_display(selected_zip, selected_pt, selected_sf, selected_bed, selected_bath, selected_year, 
                        X_pred=X_pred, prop_encode=prop_encode):
    X_pred = X_pred.append(zip_model_data.loc[selected_zip])
    X_pred['Prop_Type'] = prop_encode[selected_pt]
    try:
        X_pred['zip'] = zip_encoder.transform(pd.Series(selected_zip))[0]
    except:
        return 'ZIP not seen in data, please select another'
    else:
        X_pred['SF'] = selected_sf
        X_pred['BEDS'] = selected_bed
        X_pred['BATHS'] = selected_bath
        X_pred['YearBuilt'] = selected_year
        pred_prx = 10**pickled_model.predict(X_pred)
        return f'$ {clean_num(round(pred_prx - pred_prx*0.05,-4))} - {clean_num(round(pred_prx + pred_prx*0.05,-4))}'