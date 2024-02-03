import dash
import dash_bootstrap_components as dbc
import pandas as pd
# import numpy as np
# import plotly.graph_objs as go
# import plotly.express as px
from dash import Input, Output, dcc, html, State
from src.fig_area_1 import fig_area_1
from src.table_1 import table_1
from src.table_2 import table_2
from src.fig_area_3 import fig_area_3
from src.explanation import summary_1, summary_2, summary_3, explanation_1, explanation_2, explanation_3

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df_chart = pd.read_csv('./etc/df_test.csv', usecols=[1,2,3,4])
df_top_7 = pd.read_csv('./etc/df_table_2.csv')
std_last_reg = {'semester': '2022-2R', 'tuition_fee': 120000}

dept = 'ㅇㅇ학과'

# content1
## chart-1
fig_area_1 = fig_area_1(df_chart)

## table-1
df_chart_comma = df_chart.copy()
df_chart_comma['수혜금액'] = df_chart_comma['수혜금액'].astype('object')
df_chart_comma.loc[:, "수혜금액"] = '￦ ' + df_chart_comma["수혜금액"].map('{:,.0f}'.format)
table_1 = table_1(df_chart_comma)

# content2
## table-2
table_2 = table_2(df_top_7)

# content3
## chart-2
fig_area_3 = fig_area_3(df_chart, std_last_reg)


app.layout = dbc.Container(
    [
        # dcc.Store(id="store"),
        dcc.Location(id="url"),
        html.Header(children=html.P('장학금 및 연구비 데이터 시각화 서비스', 
                                    className='dbc-header-title'
                                    ),
        ),
        html.Nav(
            [
                dbc.Nav(
                    [
                        dbc.NavLink(children=[
                                        "장학금, 연구비",
                                        html.Br(),
                                        "수혜내역"
                                    ], 
                                    href="/chart-1",
                                    active="exact"
                        ),
                        dbc.NavLink(children=[
                                        "학과 내 최다",
                                        html.Br(),
                                        "수여 장학금",
                                    ],
                                    href="/table",
                                    active="exact"
                        ),
                        dbc.NavLink(children=[
                                        "등록금 대비",
                                        html.Br(),
                                        "수혜금액",
                                    ],
                                    href="/chart-2",
                                    active="exact"
                        ),
                    ],
                    pills=True
                ),

            ],
        ),
        html.Div(children=[
                    html.P(
                        id="page-summary",
                        className="dbc-summary-text"
                    ),
                    dbc.Button(
                        "더 보기",
                        id="collapse-button",
                        # className="mb-3",
                        color="link",
                        n_clicks=0,
                        outline=False,
                        className='dbc-info-more'
                    ),
                    dbc.Collapse(
                        id="collapse",
                        is_open=False,
                    )
                ],
                className='dbc-summary'
        ),
        html.Div(id="page-content", className="dbc-content"),
    ]
)

@app.callback(
        [Output("page-content", "children"),
         Output("collapse", "children"),
         Output("page-summary", "children")], 
        [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/chart-1":
        return [dcc.Graph(figure=fig_area_1), table_1], explanation_1, summary_1
    elif pathname == "/table":
        return table_2, explanation_2, summary_2(dept)
    elif pathname == '/chart-2':
        return dcc.Graph(figure=fig_area_3), explanation_3, summary_3

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True, port=8800)