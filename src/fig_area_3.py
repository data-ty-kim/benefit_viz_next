import plotly.express as px

def fig_area_3(df, std_last_reg):
    # 차트 유형 정렬을 위한 순서 지정
    dict_category_order = {
        '유형': ['(연구) 월인건비', '(연구) 연구수당',
                '(장학) 근로', '(장학) 국가장학', '(장학) 기타', '(장학) 성적우수', '(장학) 교직원',
                '(장학) 재난', '(장학) 저소득', '(장학) 통계조사 미반영',
                ],
        '학기': sorted(df['학기'].unique())}

    df.replace({
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
                }, 
                inplace=True
    )

    df = df.loc[df['학기'] == std_last_reg['semester'], :]

    # content1
    fig_area_3 = px.bar(df,
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

    fig_area_3.update_yaxes(
        tickangle=0,  # y 눈금명 각도
        title=None,
        ticksuffix="    ",
        tickfont=dict(color="rgba(37, 43, 65, 0.64)", family="NanumSquare")
    )

    fig_area_3.update_xaxes(
        tickangle=0,  # x 눈금명 각도
        title=dict(
            text="<b>수혜금액</b>",
            font={"size": 16, "family": "NanumSquare", "color": "#000"},
        ),
        tickfont=dict(color="rgba(37, 43, 65, 0.64)", family="NanumSquare"),
        gridcolor='rgba(53, 82, 151, 0.13)',
    )

    fig_area_3.update_layout(
        legend=dict(
            orientation="h",
            y=-0.3,
            x=-0.15,
            title_font_family="NanumSquare",
            font=dict(
                family="NanumSquare",
                size=14,
                color="#919191"
            )
        ),
        plot_bgcolor='#fff',
        paper_bgcolor='#fff',
    )

    fig_area_3.update_traces(
        width=0.35
    )

    fig_area_3.add_vline(x=std_last_reg['tuition_fee'], 
                        line_width=3, 
                        line_dash="dash", 
                        line_color="grey"
    )

    total_sum = df['수혜금액'].sum()
    tuition_fee = std_last_reg['tuition_fee']

    fig_area_3.add_annotation(
                x=total_sum,
                y=std_last_reg['semester'],
                text=f'총 수혜금액<br>{total_sum:,} 원',
                showarrow=False,
                # xshift=50,
                xshift=-35,
                yshift=63,
                font=dict(family="NanumSquareRound", 
                          size=14,
                          color="rgba(37, 43, 65, 0.64)"
                )
    )

    fig_area_3.add_annotation(
                text=f'직전 학기<br>등록금<br>{tuition_fee:,} 원',
                x=tuition_fee,
                xshift=0,
                y=0.07,
                yref="paper",
                showarrow=False,
                font=dict(family="NanumSquareRound",
                          size=14, 
                          color="rgba(37, 43, 65, 0.64)"
                )
    )

    # fig_area_3.add_annotation(
    #             text=f'({tuition_fee:,} 원)',
    #             x=tuition_fee,
    #             xshift=65,
    #             y=0.1,
    #             yref="paper",
    #             showarrow=False,
    #             font=dict(family="NanumSquareRound",
    #                       size=14, 
    #                       color="#AA52EF"
    #             )
    # )

    return fig_area_3
