import dash
from dash import html

from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

# connect with main app.py file
from app import app
from app import server

# import tab layouts
from desire import desire_layout
from afford import afford_layout
from predict import predict_layout
from eda import eda_layout 
from about import about_layout



# our app's Tabs *********************************************************

app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Desirability Scored", tab_id="tab-desire", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Affordability Index", tab_id="tab-afford", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Prediction", tab_id="tab-predict", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="EDA", tab_id="tab-eda", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="About", tab_id="tab-about", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-desire",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.Img(src="https://i.ibb.co/TmrkhDP/final-smh-final.jpg" ,
                            style={'height':'185px'}))),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])

])


@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-desire":
        return desire_layout
    elif tab_chosen == "tab-afford":
        return afford_layout
    elif tab_chosen == "tab-predict":
        return predict_layout
    elif tab_chosen == "tab-eda":
        return eda_layout
    elif tab_chosen == "tab-about":
        return about_layout
    return html.P("This shouldn't be displayed for now...")



if __name__=='__main__':
    app.run_server(debug=True)