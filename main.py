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
from src.fig_area_1 import fig_area_1
from src.table_1 import table_1
from src.table_2 import table_2
from src.table_3 import table_3
from src.fig_area_2 import fig_area_2
from src.fig_area_3 import fig_area_3
from src.fig_area_error import fig_area_error
from src.explanation import summary_1, summary_2, summary_3, summary_4
from src.explanation import explanation_1, explanation_2, explanation_3, explanation_4
import json


cred = credentials.Certificate('./config/smartku-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "장학금 및 연구비 시각화 서비스"
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
                            html.P(children=[
                                        "설문 참가하고",
                                        html.Br(),
                                        html.Span("스벅",
                                                  style={
                                                      "color": "#2E5300",
                                                      "font-family": "RixInooAriDuriR",
                                                      "font-size": "1.5rem",
                                                      "font-style": "normal",
                                                      "font-weight": "400",
                                                      "line-height": "1.875rem",
                                                      "letter-spacing": "-0.0255rem",
                                                      }
                                        ),
                                        " 쿠폰 받기!"
                                    ], 
                                   className='survey-text'
                            ),
                            html.Img(src='./assets/images/stone_right.png',
                                     className='stone-img'
                            )
                        ],
                        className='survey-banner'
                    ),
                    className='survey-link',
                    target='_blank',
                    rel='noreferrer noopener',
                    id='survey'
                ),
                html.P('장학금 및 연구비 시각화/추천서비스', 
                       className='dbc-header-title'
                )
            ],
        ),

        html.Nav(
            [
                dbc.Button(children=[
                                "장학금, 연구비",
                                html.Br(),
                                "수혜내역"
                            ], 
                            color="link",
                            id='link-1',
                            className='nav-link'

                ),
                dbc.Button(children=[
                                "전공(학과) 기반",
                                html.Br(),
                                "장학금 추천",
                            ],
                            color="link",
                            id='link-2',
                            className='nav-link'
                ),
                dbc.Button(children=[
                                "데이터 기반",
                                html.Br(),
                                "장학금 추천",
                            ],
                            color="link",
                            id='link-3',
                            className='nav-link'
                ),
            ]
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
    Output('survey', 'href'),
    Input('url', 'href')
)
def _content(href: str):
    # URL 파싱하고 key랑 dept 추출
    f = furl(href)

    dict_error_message = { 
            "content-1-1": fig_area_error(),
            "content-1-2": html.Div("잘못된 링크로 접속하셨습니다. 주소를 다시 확인해주세요."), 
            "content-2-1": html.Div("잘못된 링크로 접속하셨습니다. 주소를 다시 확인해주세요."), 
            "content-2-2": fig_area_error(),
            "content-2-3": html.Div("잘못된 링크로 접속하셨습니다. 주소를 다시 확인해주세요."), 
            "content-3": fig_area_error()
    }

    # 사용자가 다른 주소로 접근 시, 잘못된 경로임을 알려주기
    if not f.args:
        href_survey = f"https://docs.google.com/forms/d/e/1FAIpQLSfpyseDvfbfLOalGtslUBW-UD1xsTJ8A2aql0Ymm-rRrJZCMg/viewform?usp=sf_link"
        return dict_error_message, href_survey

    if not ('key' in f.args and 'dpt' in f.args and 'stdID' in f.args):
        href_survey = f"https://docs.google.com/forms/d/e/1FAIpQLSfpyseDvfbfLOalGtslUBW-UD1xsTJ8A2aql0Ymm-rRrJZCMg/viewform?usp=sf_link"
        return dict_error_message, href_survey

    param1 = f.args['key']
    param2 = f.args['dpt']
    param3 = f.args['stdID']

    try:
        doc_check_1 = (
            db.collection('Student-Fund-Data')
              .document(param1)
              .collection('Semester')
              .stream()
              .__next__()
        )
    except StopIteration:
        doc_check_1 = None
    doc_check_2 = db.collection(u'Top-7-Scholarship').document(param2).get()

    # 사용자가 key를 잘못 입력 시, 잘못된 경로임을 알려주기
    if not doc_check_1:
        href_survey = f"https://docs.google.com/forms/d/e/1FAIpQLSfpyseDvfbfLOalGtslUBW-UD1xsTJ8A2aql0Ymm-rRrJZCMg/viewform?usp=sf_link"
        return dict_error_message, href_survey

    # 사용자가 dept를 잘못 입력 시, 잘못된 경로임을 알려주기
    if not doc_check_2.exists:
        href_survey = f"https://docs.google.com/forms/d/e/1FAIpQLSfpyseDvfbfLOalGtslUBW-UD1xsTJ8A2aql0Ymm-rRrJZCMg/viewform?usp=sf_link"
        return dict_error_message, href_survey

    # href 생성
    href_survey = f"https://docs.google.com/forms/d/e/1FAIpQLSfpyseDvfbfLOalGtslUBW-UD1xsTJ8A2aql0Ymm-rRrJZCMg/viewform?usp=pp_url&entry.951904216={param3}"

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

    #df_already_got_with_count.iloc[np.random.permutation(len(df_already_got_with_count))]

    df_already_got_with_count= df_already_got.copy()
    df_already_got_with_count['기수혜'] = df_already_got_with_count['장학금명'].apply(
                            lambda x: 'Y' if x in df_sch['sch_nm'].unique() else 'N'
                            )

    # assigning coordination and size of bubbles according to scholarship ranking
    df_already_got_with_count['Size'] = [80, 65, 50, 40, 30, 23, 13]
    df_already_got_with_count['x'] = [1.5, 4.2, 1.2, 5,  4, 6.15, 6.5]
    df_already_got_with_count['y'] = [7.5, 0.95, 3.1, 8.1, 4.9, 3.6, 6]

    color_map = {'Y': '#7052EF', 'N': '#F15C6A'}
    df_already_got_with_count['color'] = df_already_got_with_count['기수혜'].map(color_map)

    #json file reading
    with open('./assets/json/dept_scholarships.json', encoding='utf-8') as f:
        scholarships_data = json.load(f)

    # 급해서 만들어둔 임시 설정
    dict_dept = {
        'dpt_sample_1': '보건안전융합과학과', 
        'dpt_sample_2': '산업경영공학과', 
        'dpt_sample_3': '역사학과', 
    }

    param4=dict_dept[param2]
    if param4 in scholarships_data:
        filtered_data = scholarships_data[param4]
        rows = [[param4] + scholarship for scholarship in filtered_data]
        df_must_know_scholarships = pd.DataFrame(rows, columns=["학과", "장학금명", "금액", "문의처"])
    else:
        df_must_know_scholarships = pd.DataFrame(columns=["학과", "장학금명", "금액", "문의처"])


    # 표 생성
    showpart_2_1 = table_2(df_already_got)
    showpart_2_2 = fig_area_2(df_already_got_with_count)
    showpart_2_3 = table_3(df_must_know_scholarships)

    # content 3
    # 학생의 등록금 고지 내역 가져오기
    list_std_reg = (
        db.collection(u'Student-Registration-Record')
          .document(param1).get().to_dict()['Registration'])

    std_last_reg = list_std_reg[-1]

    # 차트 생성
    showpart_3 = fig_area_3(df_chart, std_last_reg)

    return {
                "content-1-1": show_part_1_1,
                "content-1-2": show_part_1_2, 
                "content-2-1": showpart_2_1, 
                "content-2-2": showpart_2_2,
                "content-2-3": showpart_2_3,
                "content-3": showpart_3,
                # "key": param1,
                # "dpt": param2
    }, href_survey


@app.callback(
        [Output("page-content", "children"),
         Output("collapse", "children"),
         Output("page-summary", "children"),
         Output("link-1", "active"),
         Output("link-2", "active"),
         Output("link-3", "active")], 
        [Input("store", "data"),
         Input("link-1", "n_clicks"),
         Input("link-2", "n_clicks"),
         Input("link-3", "n_clicks")]
)
def render_page_content(data, link_1_click, link_2_click, link_3_click):
    ctx = dash.callback_context
    clicked_button_id = ctx.triggered_id.split('.')[0]

    if not clicked_button_id:
         return [
                    dcc.Graph(figure=data["content-1-1"]), 
                    dbc.Card(data["content-1-2"], className="card-table"), 
               ], explanation_1, summary_1, True, False, False

    elif clicked_button_id == "link-1":
        return [
                    dcc.Graph(figure=data["content-1-1"]), 
                    dbc.Card(data["content-1-2"], className="card-table")
               ], explanation_1, summary_1, True, False, False

    elif clicked_button_id == "link-2":
        return [
                    dbc.Card(data['content-2-1'], className="card-table"),
                    dbc.Card([
                                html.Div(
                                    dcc.Graph(figure=data["content-2-2"]),
                                    className='card-figure'
                                ),
                                html.Div(
                                    children=[
                                    "🎓", html.B("보라색 말풍선"), "🎓", 
                                    html.Br(),
                                    "기존에 수혜받은 장학금을 나타냅니다~!"
                                    ],
                                    className='card-legend'
                                )
                            ],
                            className="card-second"
                    ),
                    dbc.Card(
                        children=[
                            html.Div(
                                children=[
                                    html.Img(
                                        src='./assets/images/hoikui_original.svg',
                                        className='hoikui-left'
                                    ),
                                    html.P(
                                        "알아두면 좋은 학과 장학금", 
                                        className='content2-text'
                                    ),
                                    html.Img(
                                        src='./assets/images/hoikui_original.svg',
                                        className='hoikui-right'
                                    ) 
                                ],
                                className='content2-banner'
                            ),
                            html.Div(data['content-2-3'], className="card-table"),
                            html.Div(
                                html.P(
                                    children=[
                                        "※ 자세한 정보는 고려대학교 일반대학원 홈페이지",
                                        html.A(
                                            "(대학원생활-장학제도-대학/학과 장학금)",
                                            href="https://graduate.korea.ac.kr/scholarship/status.html",
                                            target='_blank',
                                            rel='noreferrer noopener',
                                        ),
                                        "을 참고하세요.",
                                    ],
                                    className='card-scholarship-info'
                                )
                            )
                        ] if data['content-2-3'] is not None else None,
                        className="card-second"
                    )
                        
                ], explanation_2, summary_2, False, True, False

    elif clicked_button_id == "link-3":
        return dcc.Graph(
                    figure=data['content-3']
                ), explanation_3, summary_3, False, False, True

    # 사용자가 다른 주소로 접근시, 잘못된 경로임을 알려주기
    return [html.Div(
        [
            html.H1("안녕하세요!✨💕", className="text-muted"),
            html.Hr(),
            html.P("서비스 테스터로 참여해주신 여러분을 환영합니다."),
            html.P(children=[
                    "장학금 및 연구비 데이터 시각화 서비스는 2023년의 ",
                    html.B('장학금/연구비 수혜내역 시각화 서비스'),
                    "를 고도화시킨 서비스입니다."
                   ]
            ),
            html.P(children=["찬찬히 서비스 이용해보신 후, 꼭 ",
                             html.Span("상단의 배너", 
                                       style={"color": "#F15C6A", "font-weight": "600"}
                             ),
                             "를 누르셔서 ",
                             html.Span("설문조사", 
                                       style={"color": "#2E5300", "font-weight": "600"}
                             ),
                             "에 응해주시길 부탁드립니다."]),
            html.P("감사합니다!"),
        ],
        className="p-3 bg-light rounded-3",
    ), explanation_4, 
       summary_4, 
       False, False, False
    ]


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
