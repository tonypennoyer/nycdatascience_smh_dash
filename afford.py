import plotly.express as px
import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from app import app


afford_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2("affordability")
        ], width=12)
    ]),
])

################################################### Convert below code to dash ###################################################

# # converts user input to km
# radiusInput = input('Enter a radius in miles: ') 
# radiusInput = float(radiusInput) * 1.60934
# radiusInput = int(radiusInput)
# # input metro area
# metroAreaInput = input('Enter your metro area: ')
# if metroAreaInput not in validMetroAreas :
#     raise ValueError("Invalid metro area")

# # gets only smh homes in inputted area
# smh_metro = smh_centroid[smh_centroid['Area'] == metroAreaInput]

# # if input isn't florida then get rid of all FL Refin homes (saves time)
# if metroAreaInput != 'Orlando' :
#     rf_metro = rf_distance[rf_distance['STATE OR PROVINCE'] != 'FL']
# else :  rf_metro = rf_distance[rf_distance['STATE OR PROVINCE'] == 'FL']

# # Get the centroid of inputted metro area
# gotCentroid = metroCentroidGuide[metroCentroidGuide['Area'] == metroAreaInput]
# gotCentroid = gotCentroid['centroid'].item()
# # map that centroid to column
# rf_metro['centroid'] = [gotCentroid] * len(rf_metro)
# # perform distance calculation
# rf_metro['distance'] = rf_metro.apply(lambda x: geopy.distance.geodesic(x.lat_long, x.centroid), axis = 1)

# # clean distance
# rf_metro['distance'] = rf_metro['distance'].astype(str)
# rf_metro['distance'] = rf_metro['distance'].str.rstrip(' km')
# rf_metro['distance'] = rf_metro['distance'].astype(float)
# rf_metro['distance'] = rf_metro['distance'].round(2)
# rf_metro = rf_metro[rf_metro['distance'] < radiusInput]

# # if no homes produce error msg
# if len(rf_metro) < 1 | len(smh_metro) :
#     print('No homes in this radius, pick a larger radius')
# elif len(rf_metro) > 1 : 
#     smh_metroMeanPrice = round(smh_metro["MedianSalesPrice"].mean())
#     rf_metroMeanPrice = round(rf_metro["PRICE"].mean())
#     rf_metroYearMean = 2021 - (round(rf_metro["YEAR BUILT"].mean()))
#     actualResalePrem = round(((smh_metroMeanPrice - rf_metroMeanPrice) / rf_metroMeanPrice),2)
    
#     if (rf_metroYearMean >= 0 and rf_metroYearMean <= 5) == True :
#         rf_metroExpectPrem = .95
#     elif (rf_metroYearMean >= 6 and rf_metroYearMean <= 10) == True :
#         rf_metroExpectPrem = .9
#     elif (rf_metroYearMean >= 11 and rf_metroYearMean <= 15) == True :
#         rf_metroExpectPrem = .8
#     elif (rf_metroYearMean >= 16 and rf_metroYearMean <= 20) == True :
#         rf_metroExpectPrem = .75
#     elif (rf_metroYearMean >= 21 and rf_metroYearMean <= 30) == True :
#         rf_metroExpectPrem = .6
#     elif (rf_metroYearMean >= 31 and rf_metroYearMean <= 40) == True :
#         rf_metroExpectPrem = .5
#     elif (rf_metroYearMean > 40) == True :
#         rf_metroExpectPrem = .4
        
#     expectedResalePrem = round(rf_metroMeanPrice * rf_metroExpectPrem)
    
#     if actualResalePrem > expectedResalePrem :
#         score = '1 Above Expected Premium'
#     elif actualResalePrem < expectedResalePrem :
#         score = '3 Below Expected Premium'
#     elif actualResalePrem == expectedResalePrem :
#         score = '2 In Line with Expected Premium'
    
        
#     print(f'Average resale home price in this area is ${rf_metroMeanPrice}')
#     print(f'Average resale home in this area is {rf_metroYearMean} years old')
#     print(f'Expected resale premium is {expectedResalePrem}')
#     print(f'Actual resale premium is ${actualResalePrem}')
#     print(f'The Relative Afford Score is {score}')
