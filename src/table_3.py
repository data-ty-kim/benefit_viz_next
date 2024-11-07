from dash_bootstrap_components import Table
import dash_bootstrap_components as dbc


def table_3(df):
    if df.empty:
        return None

    table_3 = Table.from_dataframe(df, 
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
        # 'font-size': '0.75rem'
    }

    for header in table_3.children[0].children[0].children:
        header.style = header_style

    return table_3
