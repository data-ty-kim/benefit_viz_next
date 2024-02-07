from dash_bootstrap_components import Table


def table_1(df):
    table_1 = Table.from_dataframe(df,
                                   striped=True,       # 행마다 음영 넣기
                                   bordered=False,     # 표와 칸에 선 넣기
                                   borderless=True,    # 세로선도 없애기
                                   hover=True,
                                   responsive=True,
                                   style={
                                        "border-collapse": "collapse",
                                        "color": "#241914",
                                        # "text-align": "center",
                                        "font-size": "0.875rem",
                                        "font-style": "normal",
                                        "font-weight": 400,
                                        "line-height": "normal"
                                   } 
    )

    header_style = {
        'background-color': '#F15C6A',
        'color': 'white', 
        'text-align': 'center'
    }

    for header in table_1.children[0].children[0].children:
        header.style = header_style

    for row in range(df.shape[0]):
        last_cell_style ={'text-align': 'right'}
        table_1.children[1].children[row].children[-1].style = last_cell_style

    return table_1