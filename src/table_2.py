from dash_bootstrap_components import Table


def table_2(df):
    table_2 = Table.from_dataframe(df, 
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
        'text-align': 'center'
    }

    for header in table_2.children[0].children[0].children:
        header.style = header_style

    return table_2
