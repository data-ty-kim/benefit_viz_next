import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import Input, Output, dcc, html

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
fig_area_1 = px.bar(df_chart.replace({'유형':
                                            {'월인건비': '(연구) 월인건비',
                                            '연구수당': '(연구) 연구수당',
                                            '근로': '(장학) 근로',
                                            '국가장학': '(장학) 국가장학',
                                            '기타': '(장학) 기타',
                                            '성적우수': '(장학) 성적우수',
                                            '교직원': '(장학) 교직원',
                                            '재난': '(장학) 재난',
                                            '저소득': '(장학) 저소득',
                                            '통계조사 미반영': '(장학) 통계조사 미반영'
                                            }})
                    , y="학기", x="수혜금액", color='유형', barmode="stack"
                    , category_orders=dict_category_order
                    , hover_data={'유형': True, '학기': True, '수혜금액': True}
                    , orientation='h'
                    )

fig_area_1.update_yaxes(
    tickangle=0,  # x 눈금명 각도
    # title_text="<b>학기</b>",
    # title_font={"size": 18},
    title=None,
    ticksuffix="    "
    # title_standoff=21  # title 떨어져있는 정도
)

fig_area_1.update_xaxes(
    tickangle=0,  # y 눈금명 각도
    title_text="<b>수혜금액</b>",
    title_font={"size": 16, 'family': "NanumSquare"},
    # title_standoff=21,  # title 떨어져있는 정도
    tickformat=","  # d3-format (파이썬 format이 아닌 듯)
)

fig_area_1.update_layout(
    title=dict(
        text="<b>학기</b>",
        font={'family': "NanumSquare", 'size': 18},
        y=0.93
    ),
    
    legend=dict(
        orientation="h",
        # yanchor="bottom",
        y=-0.3,
        # xanchor="right",
        x=-0.15,
        title_font_family="NanumSquare",
        font=dict(
            family="NanumSquare",
            size=14,
            color="black"
        )
    ),

    margin=dict(l=100)
)

df_chart_comma = df_chart.copy()
df_chart_comma['수혜금액'] = df_chart_comma['수혜금액'].astype('object')
df_chart_comma.loc[:, "수혜금액"] = '￦ ' + df_chart_comma["수혜금액"].map('{:,.0f}'.format)

# table-1
table_1 = dbc.Table.from_dataframe(df_chart_comma
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
    'color': 'white',  # You can adjust the text color as needed
    'text-align': 'center'
}

for header in table_1.children[0].children[0].children:
    header.style = header_style



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