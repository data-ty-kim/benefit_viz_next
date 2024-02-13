import dash
import dash_bootstrap_components as dbc
import pandas as pd
from numpy import arange
from dash import Input, Output, dcc, html, State
import plotly.graph_objects as go
from furl import furl
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from src.common.common_util import path_to_project_root
from src.fig_area_1 import fig_area_1
from src.table_1 import table_1
from src.table_2 import table_2
from src.fig_area_3 import fig_area_3
from src.explanation import summary_1, summary_2, summary_3, explanation_1, explanation_2, explanation_3


root_dir = path_to_project_root('benefit_viz_next')
cred = credentials.Certificate(
                f'{root_dir}/config/datahub-firebase-adminsdk.json'
)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True


app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        dcc.Location(id="url", refresh=False),
        html.Header(children=[
                html.A(html.Div(children=[
                            html.Img(src='./assets/images/stone_left.png',
                                     className='stone-img'
                            ),
                            html.P("설문 참가하기", className='survey-text'),
                            html.Img(src='./assets/images/stone_right.png',
                                     className='stone-img'
                            )
                        ],
                        className='survey-banner'
                    ),
                    href="https://digital.korea.ac.kr/",
                    className='survey-link'
                ),
                html.P('장학금 및 연구비 데이터 시각화 서비스', 
                       className='dbc-header-title'
                )
            ],
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
                                    # href="/chart-1",
                                    id='link-1',
                                    active="partial"
                        ),
                        dbc.NavLink(children=[
                                        "학과 내 최다",
                                        html.Br(),
                                        "수여 장학금",
                                    ],
                                    # href="/table",
                                    id='link-2',
                                    active="partial"
                        ),
                        dbc.NavLink(children=[
                                        "등록금 대비",
                                        html.Br(),
                                        "수혜금액",
                                    ],
                                    # href="/chart-2",
                                    id='link-3',
                                    active="partial"
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
    Output('store', 'data'),
    Output('link-1', 'href'),
    Output('link-2', 'href'),
    Output('link-3', 'href'),
    Input('url', 'href')
)
def _content(href: str):
    # URL 파싱하고 key랑 dept 추출
    f = furl(href)

    dict_error_message = { 
            "content-1-1": go.Figure(data=[]),
            "content-1-2": html.Div("잘못된 링크로 접속하셨습니다. 주소를 다시 확인해주세요."), 
            "content-2": html.Div("잘못된 링크로 접속하셨습니다. 주소를 다시 확인해주세요."), 
            "content-3": go.Figure(data=[])
    }

    if not f.args:
        return dict_error_message, 'chart-1', 'table', 'chart-2'


    param1 = f.args['key']
    param2 = f.args['dpt']
    # param3 = f.args['stdID']

    # doc_check_1 = db.collection('Student-Fund-Data').document(param1).get()
    doc_check_2 = db.collection(u'Top-7-Scholarship').document(param2).get()

    if not doc_check_2.exists:
        return dict_error_message, 'chart-1', 'table', 'chart-2'

    # 새로운 href 생성
    href_1 = f"/chart-1?key={param1}&dpt={param2}"
    href_2 = f"/table?key={param1}&dpt={param2}"
    href_3 = f"/chart-2?key={param1}&dpt={param2}"

    # content 1
    # df의 열 설정
    column_name = ['semester', 'KEDI_sch_div', 'sch_nm', 'amt']

    # 장학금 데이터
    scholarships = db.collection('Student-Scholarship-Data').document(param1).collection('Semester').stream()
    df_sch = pd.DataFrame(columns=column_name)
    for semester in scholarships:
        df = pd.DataFrame(semester.to_dict()['sch'])
        df['amt'] = df['tuition_fee'] + df['etc_fee'] + df['admission_fee']
        df_group_sum = (
            df[['KEDI_sch_div', 'sch_nm', 'amt']]
            .groupby(['KEDI_sch_div', 'sch_nm'], as_index=False)
            .sum(numeric_only=True)
        )
        df_group_sum['semester'] = semester.id
        df_sch = pd.concat([df_sch, df_group_sum])
    df_sch.replace({'KEDI_sch_div': {'국가': '국가장학'}}, inplace=True)

    # 연구비 데이터
    funds = db.collection('Student-Fund-Data').document(param1).collection('Semester').stream()
    df_fund = pd.DataFrame(columns=column_name)
    for semester in funds:
        df = (
            pd.DataFrame(semester.to_dict()['fund'])
              .groupby(['desc_div_nm', 'desc_div_cd'], as_index=False)
              .sum(numeric_only=True)
        )
        df['semester'] = semester.id
        df['sch_nm'] = '연구비'
        df = (
            df.drop('desc_div_cd', axis=1)
              .rename(columns={'desc_div_nm': 'KEDI_sch_div'})
        )
        df_fund = pd.concat([df_fund, df])

    # 장학금 & 연구비 dataframe 만들기
    df_chart = pd.concat([df_sch.fillna('기타'), df_fund.fillna(0)])
    df_chart = df_chart.sort_values(by='semester')
    df_chart.rename(columns={'semester': '학기', 'KEDI_sch_div': '유형',
                             'sch_nm': '명칭', 'amt': '수혜금액'}, inplace=True)

    # KEDI_sch_div 항목은 아래의 총 9개이다. 엑셀 파일의 내용과 차이가 존재
    # '국가장학' '저소득' '기타' '성적우수' '근로' '재난' '사설및기타' '교직원' '통계조사 미반영'
    # 연구비 항목까지 하면 총 11개이므로, '사설및기타' 항목을 '기타' 항목으로 같이 묶어서 총 10개로 만듦
    df_chart['유형'].replace('사설및기타', '기타', inplace=True)

    # 수혜금액 항목에 comma(,)와 ￦를 표시한 dataframe으로 대치
    # df['수혜금액'] 의 형식이 int32 -> object로 변하기 때문에 따로 copy()해서 처리하였다.
    df_chart_comma = df_chart.copy()
    df_chart_comma.loc[:, "수혜금액"] = df_chart_comma["수혜금액"].map('{:,.0f}'.format)

    # 차트와 표 생성
    show_part_1_1 = fig_area_1(df_chart)
    show_part_1_2 = table_1(df_chart_comma)

    # content 2
    # 소속학과의 장학금 top7 가져오기
    sch_top_7 = db.collection(u'Top-7-Scholarship').document(param2).get().to_dict()
    sorted_sch = sorted(sch_top_7.items(),
                        key=lambda x: x[1], reverse=True)

    df_already_got = pd.DataFrame(sorted_sch, columns=['장학금명', '수혜학생'])
    df_already_got['순위'] = arange(1, df_already_got.shape[0] + 1)
    df_already_got['기수혜'] = df_already_got['장학금명'].apply(
        lambda x: '★' if x in df_sch['sch_nm'].unique() else ''
    )
    df_already_got = df_already_got[['순위', '장학금명', '기수혜']]

    # 표 생성
    showpart_2 = table_2(df_already_got)

    # content 3
    # 학생의 등록금 고지 내역 가져오기
    list_std_reg = db.collection(u'Student-Registration-Record').document(param1).get().to_dict()['Registration']
    std_last_reg = list_std_reg[-1]

    # 차트 생성
    showpart_3 = fig_area_3(df_chart, std_last_reg)

    return {
                "content-1-1": show_part_1_1,
                "content-1-2": show_part_1_2, 
                "content-2": showpart_2, 
                "content-3": showpart_3,
                "key": param1,
                "dpt": param2
    }, href_1, href_2, href_3


@app.callback(
        [Output("page-content", "children"),
         Output("collapse", "children"),
         Output("page-summary", "children")], 
        [Input("url", "pathname"), 
         Input("store", "data")]
)
def render_page_content(pathname, data):
    if pathname == "/chart-1":
        return [
                    dcc.Graph(figure=data["content-1-1"]), 
                    dbc.Card(data["content-1-2"], className="card-table")
               ], explanation_1, summary_1

    elif pathname == "/table":
        return dbc.Card(data['content-2'], className="card-table"), explanation_2, summary_2

    elif pathname == "/chart-2":
        return dcc.Graph(figure=data['content-3']), explanation_3, summary_3

    # 사용자가 다른 주소로 접근시, 잘못된 경로임을 알려주기
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"입력하신 주소 {pathname} 는 잘못된 경로입니다."),
            html.P("이메일을 통해 전달받은 올바른 주소를 입력하시면 개인 맞춤형 페이지를 확인하실 수 있습니다."),
            html.P("감사합니다!"),
        ],
        className="p-3 bg-light rounded-3",
    ), "주소창에 잘못된 경로를 입력하였습니다.", "잘못된 경로"


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
    app.run_server(debug=True, port=8800) # 나중에 서버 올릴 때는 debug=False로 하기!
