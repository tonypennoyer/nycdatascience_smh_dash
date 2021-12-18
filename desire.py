import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from app import app
import pandas as pd

zip_data = pd.read_csv("https://nycdsacapstone2021.blob.core.windows.net/additionaldata/cluster_by_zip.csv", low_memory = False)
zip_data['cluster'] = zip_data['cluster'].astype(object)

grouped = zip_data.groupby('cluster').median()
grouped = grouped.reset_index()

## Create fig1 (Scatter plot with different colors by cluster)
fig1 = px.scatter(zip_data, y = 'IncomePerHousehold', x = 'Population', color = 'cluster', size= 'AverageHouseValue', title = "Scatterplot by Cluster")
fig1.update_layout(title_x = 0.5)

## Create fig2 (Parallel line graph with characteristics )
fig2  = px.parallel_coordinates(grouped, color = 'cluster', dimensions = ['cluster','Population', 'AverageHouseValue', 'IncomePerHousehold'], title = "Median Characteristics by Cluster")
fig2.update_layout(title_x = 0.5)

## Create fig3 (Cluster size by zipcode count )
zip_data = zip_data.reset_index()
cluster_size_by_state = zip_data.groupby(['cluster', 'State'])['ZipCode'].count()
cluster_size_by_state = pd.DataFrame(cluster_size_by_state)
cluster_size_by_state = cluster_size_by_state.reset_index()
cluster_size_by_state['cluster'] = cluster_size_by_state['cluster'].astype(object)
fig3 = px.bar(cluster_size_by_state, x = 'ZipCode' , y = 'cluster', color = 'State', title = "Zipcode Count by Cluster")
fig3.update_layout(title_x = 0.5)

desire_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("Desirability"),
            html.Br(),
            html.Br(),
            html.Br(),
            
        ], style = {"width": 12})
    ])
,
    dbc.Row([
        html.H4("Cluster Characteristics")
    ], style = {'textAlign': 'center'}
),
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig3)
       ] , style = {"width":"50%", "border":"1px black solid"}),
       dbc.Col([
            dcc.Graph(figure=fig1)
       ] , style = {"width":"50%", "border":"1px black solid"})
    ], style = {"textAlign" : 'center'})

,
       dbc.Row([
            dcc.Graph(figure=fig2),
       ] , style = {"textAlign" : 'center',"border":"1px black solid"},
    ),
    dbc.Row(
        html.Img(src="https://i.ibb.co/2WNHQkH/cluster-interpretation.png" ,
                            style={'height':'350', 'width':'100%',"border":"1px black solid", 'padding-top':60, "padding-bottom": 60, "align":'center'}))
    ])
