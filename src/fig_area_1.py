import plotly.express as px

def fig_area_1(df):

    # 차트 유형 정렬을 위한 순서 지정
    dict_category_order = {
        '유형': ['(연구) 월인건비', '(연구) 연구수당',
                '(장학) 근로', '(장학) 국가장학', '(장학) 기타', '(장학) 성적우수', '(장학) 교직원',
                '(장학) 재난', '(장학) 저소득', '(장학) 통계조사 미반영',
                ],
        '학기': sorted(df['학기'].unique())}

    # content1
    fig_area_1 = px.bar(df.replace({'유형':
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

    return fig_area_1