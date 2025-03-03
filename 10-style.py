import dash_bootstrap_components as dbc
from dash import Dash, html


# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div('Hello dash', style={'color': 'blue', 'fontSize': 44}),
            style={'border': '2px solid black', 'padding': 10}
        ),
        dbc.Col(
            html.P('Hi there', id='my-para', style={'background-color':'red'}),
            style={'border': '3px dotted rebeccapurple', 'padding': 20}
        )
    ],
    style={'marginTop': 50, 'border': '5px dashed coral', 'padding': 10}
    )
])

if __name__ == '__main__':
    app.run()
