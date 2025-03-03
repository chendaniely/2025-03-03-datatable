import dash_bootstrap_components as dbc
from dash import Dash, dash_table
from vega_datasets import data


cars = data.cars().iloc[:, :5]  # First 5 columns to make it easier to demo/read

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
table = dash_table.DataTable(
    cars.to_dict('records'),
    # columns=[{"name": col, "id": col} for col in cars.columns],
    columns=[{"name": col.replace('_', ' '), "id": col} for col in cars.columns],
    page_size=10,
    sort_action='native',
    filter_action='native',
)


# Layout
app.layout = dbc.Container(
    dbc.Row(
        dbc.Col(table)
    )
)

if __name__ == '__main__':
    app.run()
