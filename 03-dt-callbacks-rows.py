import dash_bootstrap_components as dbc
from dash import Dash, dash_table, dcc, callback, Input, Output
from vega_datasets import data
import pandas as pd


cars = data.cars().iloc[:, :5]  # First 5 columns to make it easier to demo/read

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
table = dash_table.DataTable(
    id='table', # <<
    data=cars.to_dict('records'),
    columns=[{"name": col.replace('_', ' '), "id": col} for col in cars.columns],
    page_size=10,
    sort_action='native',
    filter_action='native',
)

# Layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(table),
        dcc.Markdown(id='output-div')
    ])
)

@callback(
    Output('output-div', "children"), # <<
    Input('table', "derived_virtual_data"), # <<
)
def update_markdown(rows):
    [print(row) for row in rows]  # To see the returned data in the console
    return(pd.DataFrame(rows).to_markdown())

if __name__ == '__main__':
    app.run()
