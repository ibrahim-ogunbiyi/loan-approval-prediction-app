from dash import dcc, html, Input, Output, State, Dash
import dash_bootstrap_components as dbc
import numpy as np
import pickle
import dash


dash.register_page(__name__, path="/") #homepage

layout = html.Div([
    html.Div([
        dbc.Row(
            dbc.Col(html.H1("Loan Approval Prediction"),
                width="auto"),
        ),
        html.Hr(),
        html.Br(),
        dbc.Row([
            dbc.Col([          
                html.P("Married"),
                dbc.RadioItems(id="married_id", options=[{'label': i, 'value':i} for i in ["No", "Yes"]]),        

            ],
                width=2
            ),
            dbc.Col([
                html.P("Dependents"),
                dcc.Dropdown(id ="dependents_id", options = ["0", "1", "2", "3+"], value="1"),
            ],
               width={"size":8}
            )]),
        dbc.Row([ 
            dbc.Col([
                html.P("Gender"),
                dbc.RadioItems(id = "gender_id", options=[{'label': i, 'value':i} for i in ["Female", "Male"]]),
            ],
                width=2
            ),
            dbc.Col([
                html.P("Property Area"),
                dcc.Dropdown(id = "property_id", options = ["Rural", "Semi-Urban", "Urban"], value="Rural"),
            ],
                width=8
            )
        ]),
        dbc.Row([ 
            dbc.Col([
                html.P("Credit History"),
                dbc.RadioItems(id = "credit_id", options=[{'label': i, 'value':i} for i in ["No", "Yes"]])
            ],
                width=2
            ),
            dbc.Col([
                html.P("Applicant Income"),
                dbc.Input(id="applicant_id", type="number", min=100, max=1e6, placeholder="Enter your Income"),
            ],
                width=8
            )
        ]),
        dbc.Row([ 
            dbc.Col([
                html.P("Education"),
                dbc.RadioItems(id = "education_id", options=[{'label': i, 'value':i} for i in ["Not-Graduate", "Graduate"]]),
                html.P("Self Employed"),
                dbc.RadioItems(id = "self_employed_id", options=[{'label': i, 'value':i} for i in ["No", "Yes"]]),
                ],
                width=2
            ),
            dbc.Col([
                html.P("Co-Applicant Income"),
                dbc.Input(id = "co_applicant_id", type="number", min=100, max=1e6, placeholder="Enter your Income"),
                html.P("Loan Amount Term"),
                dbc.Input(id = "loan_term_id", type="number", min=12, max=480, placeholder="Enter the Loan Amount Term(Number)"),
                html.P("Loan Amount"),
                dbc.Input(id = "loan_amount_id", type="number", min=10, max=1e3, placeholder="Enter the Loan Amount")

                ],

                width=8
            )
        ])]),
    html.Hr(),
    html.Div([
            html.Button("Predict", id = "start-experiment-button", n_clicks=0),
            html.Div(id = "result-display")]
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

        #Append Education to it
        features.append(np.where(education=="Not-Graduate", 0, 1))
        #Append gender
        features.extend([np.where(gender=="Female", 0, 1), np.where(married=="No", 0, 1), np.where(self_employed=="No", 0, 1)])
        features.extend([loan_term, np.where(credit == "No", 0, 1)])
        if property_id == "Rural":
            features.append(0)
        elif property_id == "Semi-Urban":
            features.append(1)
        else:
            features.append(2)
        features.extend([applicant, co_applicant, loan_amount])
        print(features)

        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        preds = model.named_steps["model"].predict([features])
        if preds == 0:
            note = "You are not Eligible for a Loan"
        else:
            note = "Congratulations You are Eligible for a Loan"
        html.Br(),
        html.Br()
        return html.Div(note)