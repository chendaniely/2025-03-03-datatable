import dash_bootstrap_components as dbc
from dash import Dash, dash_table, dcc, callback, Input, Output
from vega_datasets import data
import pandas as pd


cars = data.cars().iloc[:, :5]  # First 5 columns to make it easier to demo/read

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
table = dash_table.DataTable(
    id='table',
    data=cars.to_dict('records'),
    columns=[  # A list of dictionaries, each representing a column
        {
            "name": col.replace('_', ' '),
            "id": col,
            'selectable': False if col == 'Name' else True # marks if col is selectable
        }
        for col in cars.columns # part of the dict comprehension
    ],
    column_selectable="single", # can be multi
    selected_columns=['Miles_per_Gallon'],
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
    Output('output-div', "children"),
    Input('table', "derived_virtual_data"),
    Input('table', "selected_columns"),
)
def update_markdown(rows, columns):
    print(columns)  # A list of column names as strings
    return(pd.DataFrame(rows)[columns].to_markdown())

if __name__ == '__main__':
    app.run()
