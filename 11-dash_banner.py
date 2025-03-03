import dash_bootstrap_components as dbc
from dash import Dash, html


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

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
])

if __name__ == '__main__':
    app.run()
