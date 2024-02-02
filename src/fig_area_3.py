import plotly.graph_objects as go
from itertools import accumulate


def fig_area_3(df, std_last_reg):
    dict_attribute = {'월인건비': 0, '연구수당': 0, '근로': 0, '국가장학': 0, '기타': 0, '성적우수': 0,
                      '교직원': 0, '재난': 0, '저소득': 0, '통계조사 미반영': 0, }

    df_last_sem = df[df['학기'] == std_last_reg['semester']][['유형', '수혜금액']]

    for row in range(len(df_last_sem)):
        if df_last_sem.iloc[row, 0] == '월인건비':
            dict_attribute['월인건비'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '연구수당':
            dict_attribute['연구수당'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '근로':
            dict_attribute['근로'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '국가장학':
            dict_attribute['국가장학'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '기타':
            dict_attribute['기타'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '성적우수':
            dict_attribute['성적우수'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '교직원':
            dict_attribute['교직원'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '재난':
            dict_attribute['재난'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '저소득':
            dict_attribute['저소득'] += df_last_sem.iloc[row, 1]
        elif df_last_sem.iloc[row, 0] == '통계조사 미반영':
            dict_attribute['통계조사 미반영'] += df_last_sem.iloc[row, 1]

    # 장학금과 연구비 누적합 리스트 만들기
    total_amt = list(accumulate(
        [value for value in dict_attribute.values()]))

    # indicator 그리기
    fig_area_3 = go.Figure()
    fig_area_3.add_trace(go.Indicator(
        mode="gauge+number",
        value=sum(dict_attribute.values()) // 10000,
        number={
                    "prefix": "￦ ", 
                    "suffix": "만원", 
                    "valueformat": ",.0f", 
                    "font": dict(
                        family="NanumSquare", 
                        size=25, 
                        color="#6C6365"
                    )
                },
        gauge={
            'axis': {'range': [None, sum(dict_attribute.values()) // 10000 + 300],
                     'showticklabels': False
                     },
            'steps': [
                {'range': [0, total_amt[0] // 10000],
                 'color': "#F15C6A"},
                {'range': [total_amt[0] // 10000, total_amt[1] // 10000],
                 'color': "#7052EF"},
                {'range': [total_amt[1] // 10000, total_amt[2] // 10000],
                 'color': "#FBD583"},
                {'range': [total_amt[2] // 10000, total_amt[3] // 10000],
                 'color': "#559900"},
                {'range': [total_amt[3] // 10000, total_amt[4] // 10000],
                 'color': "#E756AD"},
                {'range': [total_amt[4] // 10000, total_amt[5] // 10000],
                 'color': "#6C6365"},
                {'range': [total_amt[5] // 10000, total_amt[6] // 10000],
                 'color': "#F2A054"},
                {'range': [total_amt[6] // 10000, total_amt[7] // 10000],
                 'color': "#AB58C8"},
                {'range': [total_amt[7] // 10000, total_amt[8] // 10000],
                 'color': "#DC0418"},
                {'range': [total_amt[8] // 10000, total_amt[9] // 10000],
                 'color': "#10C59A"}
            ],

            'threshold': {'line': {'color': "#F4F4F4", 'width': 4},
                          'thickness': 0.75,
                          'value': std_last_reg['tuition_fee'] // 10000}
            , 'bar': {'color': "white"}
        },
        # title={'text': f"<b> {std_last_reg['semester']}</b> <br><sup>등록금 대비 수혜금액</sup>",
        #        'font': dict(family="NanumSquare", size=16)},
        domain={'x': [0, 1], 'y': [0, 1]},
    ))

    threshold_label = go.layout.Annotation(
        text="<b>등록금:</b> {:,.0f}원".format(std_last_reg['tuition_fee']),
        x=0.5,
        y=0.38,
        showarrow=False,
        font=dict(color="#DA4167", size=14, family="NanumSquare"))

    fig_area_3.update_layout(
        annotations=[threshold_label],
        title={
            'text': f"<b> {std_last_reg['semester']}</b><br><sup>등록금 대비 수혜금액</sup>",
            'font': dict(family="NanumSquareEB", size=16),
            # 'xanchor': 'center',
            # 'yanchor': 'top'
            'y':0.78,
            'x':0.5,
            },

    )

    return fig_area_3
