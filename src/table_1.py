import dash_bootstrap_components as dbc


def table_1(df):
    table_1 = dbc.Table.from_dataframe(df
                                        , striped=True       # 행마다 음영 넣기
                                        , bordered=False     # 표와 칸에 선 넣기
                                        , borderless=True    # 세로선도 없애기
                                    #    , hover=True
                                    #    , dark=True
                                        , responsive=True
                                    #    , color="secondary"
                                        , style={
                                            # "border": "2px solid #0F491B",
                                            # "border-top-right-radius": "15px",
                                            # "border-top-left-radius": "15px",
                                        #    "border-radius": "10px",
                                        #    "background": "#FFF",
                                        #    "border-style": "hidden",
                                        "border-collapse": "collapse",
                                        #    "box-shadow": "0 0 0 1px #000"
                                            }
                                        )

    header_style = {
        'background-color': '#0F491B',
        'color': 'white', 
        'text-align': 'center'
    }

    for header in table_1.children[0].children[0].children:
        header.style = header_style

    return table_1