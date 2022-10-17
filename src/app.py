import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__, use_pages=True)

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server
sidebar = dbc.Nav([
    dbc.NavLink(
        [
            html.Div(page["name"], className="btn btn-outline-secondary")
        ],
        href=page["path"],
    )
    for page in dash.page_registry.values()
],
    vertical=True,
    pills=True,

)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div("Loan Approval Prediction", style={
                     "fontSize": 50, "textAlign": "center"})
        ])
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            sidebar
        ], md=3
        ),

        dbc.Col([
            dash.page_container
        ], md=9
        )

    ])


], fluid=True)

if __name__ == "__main__":
    app.run(port=8052)
