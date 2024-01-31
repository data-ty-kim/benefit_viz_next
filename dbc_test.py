import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import Input, Output, dcc, html
from src.fig_area_1 import fig_area_1
from src.table_1 import table_1

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df_chart = pd.read_csv('./etc/df_test.csv', usecols=[1,2,3,4])


# 차트 유형 정렬을 위한 순서 지정
dict_category_order = {
    '유형': ['(연구) 월인건비', '(연구) 연구수당',
            '(장학) 근로', '(장학) 국가장학', '(장학) 기타', '(장학) 성적우수', '(장학) 교직원',
            '(장학) 재난', '(장학) 저소득', '(장학) 통계조사 미반영',
            ],
    '학기': sorted(df_chart['학기'].unique())}

# content1
fig_area_1 = fig_area_1(df_chart)

df_chart_comma = df_chart.copy()
df_chart_comma['수혜금액'] = df_chart_comma['수혜금액'].astype('object')
df_chart_comma.loc[:, "수혜금액"] = '￦ ' + df_chart_comma["수혜금액"].map('{:,.0f}'.format)

# table-1
table_1 = table_1(df_chart)


app.layout = dbc.Container(
    [
        # dcc.Store(id="store"),
        dcc.Location(id="url"),
        html.Header(children=html.P('장학금 및 연구비 데이터 시각화 서비스', 
                                    className='header-title'),
                    className='header-container'
        ),
        html.H1("장학금 및 연구비 시각화 서비스"),
        html.Hr(),
        html.Nav(
            [
                dbc.Nav(
                    [
                        dbc.NavLink(
                            "장학금, 연구비 수혜내역", 
                            href="/chart-1",
                            active="exact",
                            className='nav-item'
                        ),
                        dbc.NavLink(
                            "학과 내 최다 수여 장학금", 
                            href="/table",
                            active="exact",
                            className='nav-item'
                        ),
                    ],
                    pills=True
                ),

            ],
        className='nav-container'
        ),
        html.Br(),
        html.P("수혜받은 장학금과 연구비를 유형과 함께 보여줍니다."),
        html.Div(id="page-content", className="p-4"),
    ]
)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/chart-1":
        return html.Div(dcc.Graph(figure=fig_area_1))
    elif pathname == "/table":
        return html.Div(table_1)
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )




if __name__ == "__main__":
    app.run_server(debug=True, port=8800)