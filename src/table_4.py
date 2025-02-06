import dash_bootstrap_components as dbc
from dash_bootstrap_components import Table
from dash import html

def table_4(df, table_prefix='df'):
    if df.empty:
        return None

    table_component = Table.from_dataframe(
        df.iloc[:, :-1], 
        striped=True, 
        bordered=False, 
        borderless=True,
        hover=True, 
        responsive=True,
        style={
            "border-collapse": "collapse",
            "color": "#241914",
            "text-align": "center",
            "font-size": "0.875rem",
            "font-style": "normal",
            "font-weight": 400,
            "line-height": "normal",
        } 
    )

    header_style = {
        'background-color': '#F15C6A',
        'color': 'white',
        'text-align': 'center',
    }

    for header in table_component.children[0].children[0].children:
        header.style = header_style

    tooltips = []
    tbody = table_component.children[1]

    for i, row in enumerate(tbody.children):
        last_cell = row.children[-1]
        cell_id = f"{table_prefix}-cell-{i}"
        last_cell.id = cell_id

        full_text = str(table_prefix.iloc[i, -1])

        tooltips.append(
            dbc.Tooltip(
                full_text, 
                target=cell_id, 
                placement="top", 
                style={"whiteSpace": "normal", "maxWidth": "none", "width":"max-content"}
            )
        )


    return html.Div([table_component] + tooltips)