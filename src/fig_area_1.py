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
    fig_area_1 = px.bar(df.replace(
                            {
                                '유형': {
                                        '월인건비': '(연구) 월인건비',
                                        '연구수당': '(연구) 연구수당',
                                        '근로': '(장학) 근로',
                                        '국가장학': '(장학) 국가장학',
                                        '기타': '(장학) 기타',
                                        '성적우수': '(장학) 성적우수',
                                        '교직원': '(장학) 교직원',
                                        '재난': '(장학) 재난',
                                        '저소득': '(장학) 저소득',
                                        '통계조사 미반영': '(장학) 통계조사 미반영'
                                        }
                            }
                        ),
                        y="학기", x="수혜금액", color='유형', barmode="stack",
                        category_orders=dict_category_order,
                        hover_data={'유형': True, '학기': True, '수혜금액': ":,"},
                        orientation='h',
                        color_discrete_map={
                            '(연구) 월인건비': '#F15C6A', 
                            '(연구) 연구수당': '#7052EF', 
                            '(장학) 근로': '#FBD583', 
                            '(장학) 국가장학': '#559900',
                            '(장학) 기타': '#E756AD', 
                            '(장학) 성적우수': '#6C6365', 
                            '(장학) 교직원': '#F2A054', 
                            '(장학) 재난': '#AB58C8',
                            '(장학) 저소득': '#DC0418', 
                            '(장학) 통계조사 미반영': '#10C59A'
                        }
                        )

    fig_area_1.update_yaxes(
        tickangle=0,  # x 눈금명 각도
        # title_text="<b>학기</b>",
        # title_font={"color": "rgba(37, 43, 65, 0.64)"},
        title=None,
        ticksuffix="    ",
        tickfont=dict(color="rgba(37, 43, 65, 0.64)", family="NanumSquare")
        # title_standoff=21  # title 떨어져있는 정도
    )

    fig_area_1.update_xaxes(
        tickangle=0,  # y 눈금명 각도
        title=dict(
            text="<b>수혜금액</b>",
            font={"size": 16, "family": "NanumSquare", "color": "#000"},
        ),
        tickfont=dict(color="rgba(37, 43, 65, 0.64)", family="NanumSquare"),
        # title_standoff=15,  # title 떨어져있는 정도
        # tickformat=",",  # d3-format (파이썬 format이 아닌 듯)
        gridcolor='rgba(53, 82, 151, 0.13)',
        # showticklabels=False,
    )

    fig_area_1.update_layout(
        title=dict(
            text="<b>학기</b>",
            font={
                    'family': "NanumSquare", 
                    'size': 18, 
                    'color': '#000'
                 },
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
                color="#919191"
            )
        ),
        margin=dict(l=100),
        plot_bgcolor='#fff',
        paper_bgcolor='#fff',
        # bargap=0.35
    )

    fig_area_1.update_traces(
        width=0.68
    )

    df_sum_of_stack = df.groupby('학기')['수혜금액'].sum()
    df_sum_of_stack.sort_index(inplace=True)

    for semester, amount in zip(df_sum_of_stack.index, df_sum_of_stack.values):
        fig_area_1.add_annotation(
                x=amount,
                y=semester,
                text=f'{amount:,} 원',
                showarrow=False,
                xshift=50,
                font=dict(family="NanumSquareRound", 
                          color="rgba(37, 43, 65, 0.64)"
                )
        )

    return fig_area_1