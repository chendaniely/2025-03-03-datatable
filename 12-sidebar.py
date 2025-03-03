import dash_bootstrap_components as dbc
from dash import Dash, html, dcc


# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
title = html.H1(
    'My splashboard demo',
    style={
        'backgroundColor': 'steelblue',
        'padding': 20,
        'color': 'white',
        'margin-top': 20,
        'margin-bottom': 20,
        'text-align': 'center',
        'font-size': '48px',
        'border-radius': 3,
    }
)
sidebar = dbc.Col([
    html.H5('Global controls'),
    html.Br(),
    dcc.Dropdown(),
    html.Br(),
    dcc.Dropdown(),
    html.Br(),
    dcc.Dropdown(),
    ],
    md=3,
    style={
        'background-color': '#e6e6e6',
        'padding': 15,
        'border-radius': 3
    }
)

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row(dbc.Col(sidebar)),
])

if __name__ == '__main__':
    app.run()
