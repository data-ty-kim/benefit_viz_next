from dash_bootstrap_components import Card, CardBody
from dash import html


summary_1 = "수혜받은 장학금과 연구비를 유형과 함께 보여줍니다."

summary_2 = "재학 중인 전공(학과)를 기반으로 장학금을 추천합니다."
# def summary_2(dept):
#     return f"{dept}에서 가장 많은 학생이 받은 장학금입니다."

summary_3 = "교내 장학 공지 데이터(최근 3년)에 기반하여 장학금을 추천합니다."

summary_4 = "메뉴를 눌러서 장학금/연구비 정보를 확인해보세요."


explanation_1 = Card(
                CardBody(
                    children=[
                    html.P("누적막대그래프를 통해 학기별로 받은 수혜금액을 쉽게 비교할 수 있으며, 장학금과 연구비 중에서 어떤 요소를 어느 정도 받았는지를 시각적으로 파악할 수 있습니다.", 
                           className='mb-1'
                    ),
                    html.P("2017년 이후 수혜내역을 표시하며 학기 순서대로 나열되어 있습니다. 장학금과 연구비의 유형, 명칭, 금액을 확인할 수 있습니다."
                    )
                    ],
                    className='dbc-card-explanation'
                ),
                style={
                        'background-color': 'white', 
                        'border': 'none'
                }
)

explanation_2 = Card(
                CardBody(
                    children=[
                    html.P(
                        "1. 통계적으로 받기 유리한 장학금을 추천드립니다! (2020년 이후 데이터)",
                        className='mb-1'
                    ),
                    html.P(
                        "해당 장학금을 이미 받은 적이 있다면 '기수혜여부'에 ★ 표시됩니다.", 
                        style={'margin-left': '0.9rem'},
                        className='mb-1'
                    ),
                    html.P("2. 재학 중인 학과와 관련된 장학금을 추천드립니다!"),
                    ],
                    className='dbc-card-explanation'
                ),
                style={
                        'background-color': 'white', 
                        'border': 'none'
                }
)

explanation_3 = Card(
                CardBody(
                    children=[
                    html.P("첫 번째 표에서는 교내 장학 공지 데이터를 기반으로 학생 맞춤형 장학금을 추천합니다.", 
                           className='mb-1'
                    ),
                    html.P("두 번째 표에서는 최근에 올라온 장학 공지 게시물을 확인하실 수 있습니다.", 
                           className='mb-1'
                    ),
                    html.P("세 번째 표에서는 시기별 맞춤형 장학금을 추천합니다."),
                    ],
                    className='dbc-card-explanation'
                ),
                style={
                        'background-color': 'white', 
                        'border': 'none'
                }
)

explanation_4 = Card(
                CardBody(
                    children=[
                    html.P("각 차트 화면에서도 '더 보기'를 누르시면 각 차트별 자세한 설명을 볼 수 있습니다.", 
                           className='mb-1'
                    )],
                    className='dbc-card-explanation'
                ),
                style={
                        'background-color': 'white', 
                        'border': 'none'
                }
)
