import dash_bootstrap_components as dbc
from dash import Dash, dash_table, dcc, callback, Input, Output
from vega_datasets import data
import pandas as pd


cars = data.cars()

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
table = dash_table.DataTable(
    id='table',
    # The data and columns parameters are set in the callback instead
    column_selectable="single",
    selected_columns=['Miles_per_Gallon'],
    page_size=10,
    sort_action='native',
    filter_action='native',
)
dropdown = dcc.Dropdown(
    id='dropdown',
    options=cars.columns,
    value=['Name', 'Miles_per_Gallon', 'Horsepower'],
    multi=True
)

# Layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([dropdown, table]),
        dbc.Col(dcc.Markdown(id='output-div'))
    ])
)

# This callback sets the default values of the table
# (since there is a default value in the dropdown)
# and then updates each time the dropdown is changes
@callback(
    Output('table', "columns"),
    Output('table', "data"),
    Input('dropdown', "value"),
)
def update_table(dropdown_cols):
    print(dropdown_cols)
    return(
        [  # A list of dictionaries, each representing a column
            {
                "name": col.replace('_', ' '),
                "id": col,
                'selectable': False if col == 'Name' else True
            }
            for col in dropdown_cols
        ],
        cars[dropdown_cols].to_dict('records')
    )


@callback(
    Output('output-div', "children"),
    Input('table', "derived_virtual_data"),
    Input('table', "selected_columns"),
    prevent_initial_call=True  # Avoid triggering before the table has a selected column
)
def update_markdown(table_rows, table_column):
    return pd.DataFrame(table_rows)[table_column].to_markdown()

if __name__ == '__main__':
    app.run()
