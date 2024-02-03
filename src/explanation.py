from dash_bootstrap_components import Card, CardBody
from dash import html


summary_1 = "수혜받은 장학금과 연구비를 유형과 함께 보여줍니다."

def summary_2(dept):
    return f"{dept}에서 가장 많은 학생이 받은 장학금입니다."

summary_3 = "납부한 등록금 대비 장학금 수혜내역을 표시합니다."

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
                    html.P("2020년 이후 동일 학과 학생들이 가장 많이 받은 상위 장학금 목록입니다.", className='mb-1'),
                    html.P("학생이 해당 장학금을 이미 받은 적이 있다면 '기수혜여부'에 ★ 표시됩니다."),
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
                    html.P("마지막으로 납부한 등록금(또는 수료연구 등록금) 대비 연구비 및 장학금 수혜내역을 표시합니다.", 
                           className='mb-1'
                    ),
                    html.P("빨간선은 해당 학기에 납부한 등록금액을 의미하며 수혜금액과 비교 파악할 수 있습니다",
                           className='mb-1'
                    ),
                    html.P("수혜내역의 색상은 하단 범례를 통해 어떤 유형인지 확인할 수 있습니다."),
                    ],
                    className='dbc-card-explanation'
                ),
                style={
                        'background-color': 'white', 
                        'border': 'none'
                }
)
