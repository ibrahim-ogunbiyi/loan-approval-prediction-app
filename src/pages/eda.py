
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import business
import dash


gb = business.GraphBuilder()

dash.register_page(__name__, name="Exploratory Data Analysis")

layout = html.Div([
    html.P("These Are the Key Features That Improve the Performance of the Model."),
    html.Br(), html.Br(),
    dcc.Dropdown(
        id="feature_selection",
        options=["Credit History", "Applicant Income",
                 "Loan Amount", "Co-applicant Income", "Property Area"],
        value=None),
    html.Div(id="eda_result"
             )
])


@callback(
    Output("eda_result", "children"),
    Input("feature_selection", "value")
)
def display_result(feature):
    if feature == None:
        return html.Div()
    elif feature == "Credit History":
        fig = gb.build_credit_relationship()
        return fig
    elif feature == "Applicant Income":
        fig = gb.build_app_income_relationship()
        return fig
    elif feature == "Loan Amount":
        fig = gb.build_loan_amount_relationship()
        return fig
    elif feature == "Co-applicant Income":
        fig = gb.build_coapplicant_relationship()
        return fig
    else:
        fig = gb.build_propetry_relationship()
        return fig
