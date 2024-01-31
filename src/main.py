from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.common_util import path_to_project_root

# Firebase init
root_dir = path_to_project_root('benefit_viz_next')
cred = credentials.Certificate(
    f'{root_dir}/config/datahub-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Dash init
dash_app = Dash(__name__)
dash_app.title = '장학금 및 연구비 데이터 시각화 서비스'
server = dash_app.server
dash_app.config.suppress_callback_exceptions = True

'''
# Plot 1 to test the Dash
# bring parameters
param1 = 'AAEXNEA8lKEv5dYsaLBzlX3'
param2 = 'AAEAdCf4UZeMuNMCKQckIel'
param3 = '2018010361'

# df의 열 설정
column_name = ['semester', 'KEDI_sch_div', 'sch_nm', 'amt']

# 장학금 데이터
scholarships = db.collection('Student-Scholarship-Data').document(param1).collection('Semester').stream()
df_sch = pd.DataFrame(columns=column_name)
for semester in scholarships:
    df_0 = pd.DataFrame(semester.to_dict()['sch'])
    df_0['amt'] = df_0['tuition_fee'] + df_0['etc_fee'] + df_0['admission_fee']
    df_1 = df_0[['KEDI_sch_div', 'sch_nm', 'amt']
    ].groupby(['KEDI_sch_div', 'sch_nm'], as_index=False).sum(numeric_only=True)
    df_1['semester'] = semester.id
    df_sch = pd.concat([df_sch, df_1])
df_sch.replace({'KEDI_sch_div': {'국가': '국가장학'}}, inplace=True)

# 연구비 데이터
funds = db.collection('Student-Fund-Data').document(param1).collection('Semester').stream()
df_fund = pd.DataFrame(columns=column_name)
for semester in funds:
    df = pd.DataFrame(semester.to_dict()['fund']
                        ).groupby(['desc_div_nm', 'desc_div_cd'], as_index=False).sum(numeric_only=True)
    df['semester'] = semester.id
    df['sch_nm'] = '연구비'
    df = df.drop('desc_div_cd', axis=1
                    ).rename(columns={'desc_div_nm': 'KEDI_sch_div'})
    df_fund = pd.concat([df_fund, df])

# 장학금 & 연구비 dataframe 만들기
df_chart = pd.concat([df_sch.fillna('기타'), df_fund.fillna(0)])
df_chart = df_chart.sort_values(by='semester')
df_chart.rename(columns={'semester': '학기', 'KEDI_sch_div': '유형',
                            'sch_nm': '명칭', 'amt': '수혜금액'}, inplace=True)

# ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
# KEDI_sch_div 항목은 아래의 총 9개이다. 엑셀 파일의 내용과 차이가 존재
# '국가장학' '저소득' '기타' '성적우수' '근로' '재난' '사설및기타' '교직원' '통계조사 미반영'
# 연구비 항목까지 하면 총 11개이므로, '사설및기타' 항목을 '기타' 항목으로 같이 묶어서 총 10개로 만듦
df_chart['유형'].replace('사설및기타', '기타', inplace=True)
'''

df_chart = pd.read_csv('./etc/df_test.csv', usecols=[1,2,3,4])

# 차트 유형 정렬을 위한 순서 지정
dict_category_order = {
    '유형': ['(연구) 월인건비', '(연구) 연구수당',
            '(장학) 근로', '(장학) 국가장학', '(장학) 기타', '(장학) 성적우수', '(장학) 교직원',
            '(장학) 재난', '(장학) 저소득', '(장학) 통계조사 미반영',
            ],
    '학기': sorted(df_chart['학기'].unique())}

# content1

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


# 수혜금액 항목에 comma(,)와 ￦를 표시한 dataframe으로 대치
# df['수혜금액'] 의 형식이 int32 -> object로 변하기 때문에 따로 copy()해서 처리하였다.
df_chart_comma = df_chart.copy()
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


# Dash Layout
dash_app.layout = html.Div(children=[

    html.Header(children=html.P('장학금 및 연구비 데이터 시각화 서비스', 
                                className='header-title'),
                className='header-container'
    ),

    html.Nav(children=html.Ul(children=[

        html.Li(children=html.A(html.Div([
                          html.Img(src='./assets/images/waterfall.png'), 
                          html.Br(), 
                          '장학금, 연구비',
                          html.Br(), 
                          '수혜내역']), href='#'), 
                className='nav-item'
        ),
        html.Li(children=html.A(html.Div([
                          html.Img(src='./assets/images/pyramid_chart.png'), 
                          html.Br(), 
                          '학과 내 최다',
                          html.Br(), 
                          '수여 장학금']), href='#'), 
                className='nav-item'
        ),
        html.Li(children=html.A(html.Div([
                          html.Img(src='./assets/images/pie_chart.png'), 
                          html.Br(), 
                          '등록금 대비',
                          html.Br(), 
                          '수혜금액']), href='#'), 
                className='nav-item'
        )
        ],
        className='nav-container')
    ),

    html.Main(children=[

        html.Article(children=[html.P('''
                                      수혜받은 장학금과 연구비를 유형과 함께 보여줍니다.
                                      ''', className='summary-text'),
                               html.Span('더 보기', className='info-more')
                               ],
                     className='summary-box'
        ),

        html.Figure(children=[
                        dcc.Graph(id='example-graph', figure=fig_area_1),
                        html.Br(),
                        html.Div(children=[table_1], className='table-area-1'),
                        html.Br()
                    ],
                    className='plot-area'
        )

        

        ],
        className='main-area'
    )

])






if __name__ == '__main__':
    dash_app.run(debug=True)
