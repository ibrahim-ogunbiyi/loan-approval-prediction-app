import dash
from dash import html
import dash_bootstrap_components as dbc
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
        ], xs=4, sm=4, lg=2, xl=2, xxl=2
        ),

        dbc.Col([
            dash.page_container
        ], xs=8, sm=8, lg=10, xl=10, xxl=10
        )

    ])


], fluid=True)

if __name__ == "__main__":
    app.run(port=8052)
