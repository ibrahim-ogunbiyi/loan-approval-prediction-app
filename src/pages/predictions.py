import pickle

import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import Input, Output, State, callback, dcc, html

dash.register_page(__name__, path="/", name="Prediction")  # homepage

layout = html.Div([
    html.Div([
        html.P("Please input the values for the following features and click on the predict button to know if you are eligible for the loan."),
        html.Br(),
        # 1
        html.Div([
            html.Div([
                html.Label('Married', htmlFor="married_id", className="d-block my-2"),
                dcc.Dropdown(id="married_id", options=[
                             "No", "Yes"], value=None),
            ], className="col col-md-3"),
            html.Div([
                html.Label('Dependents', htmlFor="dependents_id", className="d-block my-2"),
                
                dcc.Dropdown(id="dependents_id", options=[
                             "0", "1", "2", "3+"], value="1"),
            ], className="col col-md-5"),
        ],className="row py-3"),

        # 2
        html.Div([
            html.Div([
                html.Label('Gender', htmlFor="gender_id", className="d-block my-2"),
                dcc.Dropdown(id="gender_id", options=[
                             "Female", "Male"], value=None),
            ], className="col col-md-3"),
            html.Div([
                html.Label('Property Area', htmlFor="property_id", className="d-block my-2"),
                dcc.Dropdown(id="property_id", options=[
                             "Rural", "Semi-Urban", "Urban"], value="Rural"),
            ], className="col col-md-5"),
        ],className="row py-3"),

        # 3
        html.Div([
            html.Div([
                html.Label('Credit History', htmlFor="credit_id", className="d-block my-2"),
                dcc.Dropdown(id="credit_id", options=["No", "Yes"], value=None),
            ], className="col col-md-3"),
            html.Div([
                html.Label('Applicant Income', htmlFor="applicant_id", className="d-block my-2"),
                dbc.Input(id="applicant_id", type="number", min=100,
                          max=1e6, placeholder="Enter your Income", className="form-control"),
            ], className="col col-md-5"),
        ],className="row py-3"),

        # 4
        html.Div([
            html.Div([
                html.Label('Education', htmlFor="education_id", className="d-block my-2"),
                dcc.Dropdown(id="education_id", options=["Not-Graduate", "Graduate"], value=None),

            ], className="col col-md-3"),
            html.Div([
                html.Label('Co-Applicant Income', htmlFor="co_applicant_id", className="d-block my-2"),
                dbc.Input(id="co_applicant_id", type="number", min=100,
                          max=1e6, placeholder="Enter your Income", className="form-control"),
            ], className="col col-md-5"),
        ],className="row py-3"),

        # 5
        html.Div([
            html.Div([
                html.Label('Self Employed', htmlFor="self_employed_id", className="d-block my-2"),
                dcc.Dropdown(id="self_employed_id", options=["No", "Yes"], value=None),

            ], className="col col-md-3"),
            html.Div([
                html.Label('Loan Amount Term', htmlFor="loan_term_id", className="d-block my-2"),
                dbc.Input(id="loan_term_id", type="number", min=12,
                          max=480, placeholder="Enter the Loan Amount Term (Number)", className="form-control"),
            ], className="col col-md-5"),
        ],className="row py-3"),
        
        # 6
        html.Div([
            html.Div([
                html.Label('Loan Amount ', htmlFor="loan_amount_id", className="d-block my-2"),
                dbc.Input(id="loan_amount_id", type="number", min=10,
                          max=1e3, placeholder="Enter the Loan Amount", className="form-control"),
            ], className="col-md-8"),
        ],className="row py-3"),
                ]),
   
    html.Hr(),
    html.Div(
        [
        dbc.Button("Start Predict", id="start-experiment-button", className="btn btn-secondary w-55", n_clicks=0),
        html.Br(),
        html.Br(),
        html.Div(id="result-display", className="col-md-8")], className="py-3"
    )
])


@callback(
    Output("result-display", "children"),
    Input("start-experiment-button", "n_clicks"),
    State("dependents_id", "value"),
    State("education_id", "value"),
    State("applicant_id", "value"),
    State("co_applicant_id", "value"),
    State("loan_amount_id", "value"),
    State("gender_id", "value"),
    State("married_id", "value"),
    State("self_employed_id", "value"),
    State("loan_term_id", "value"),
    State("credit_id", "value"),
    State("property_id", "value"),
)
def predict_loan(n_clicks, dependents, education, applicant, co_applicant,
                 loan_amount, gender, married, self_employed, loan_term, credit, property_id):
    if n_clicks == 0:
        return html.Div()
    else:
        features = []
        if dependents == "0":
            features.extend([1, 0, 0, 0])
        elif dependents == "1":
            features.extend([0, 1, 0, 0])
        elif dependents == "2":
            features.extend([0, 0, 1, 0])
        else:
            features.extend([0, 0, 0, 1])

        # Append Education to it
        features.append(np.where(education == "Not-Graduate", 0, 1))
        # Append gender
        features.extend([np.where(gender == "Female", 0, 1), np.where(
            married == "No", 0, 1), np.where(self_employed == "No", 0, 1)])
        features.extend([loan_term, np.where(credit == "No", 0, 1)])
        if property_id == "Rural":
            features.append(0)
        elif property_id == "Semi-Urban":
            features.append(1)
        else:
            features.append(2)
        features.extend([applicant, co_applicant, loan_amount])
        print(features)
        
        with open("src\pages\model.pkl", "rb") as f:
            model = pickle.load(f)
        preds = model.named_steps["model"].predict([features])
        if preds == 0:
            note = "Sorry😢! You are not Eligible for a Loan at this Time❌."
            return html.Div(note, className="alert alert-danger")
        else:
            note = "Congratulations🎉 You are Eligible for a Loan😎💸💷."
            return html.Div(note,  className="alert alert-success")
