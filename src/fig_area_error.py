import plotly.graph_objects as go


def fig_area_error():
    fig = go.Figure(data=[])

    fig.update_layout(
                font={'family': 'NanumSquare'},
                annotations=[dict(
                    text="주소를 다시 확인하여주세요.",
                    x=2.5, y=1.5,
                    xanchor="center", yanchor="middle",
                    showarrow=False,
                    font=dict(color="#252930", size=32, family="NanumSquare")
                )],

                title=dict(
                    text="<b>잘못된 접근</b>",
                    font={
                            'family': "NanumSquare", 
                            'size': 18, 
                            'color': '#000'
                        },
                    y=0.93,
                    x=0.5
                ),
                margin=dict(l=100),
                plot_bgcolor='#fff',
                paper_bgcolor='#fff',
            )

    fig.update_xaxes(
        showticklabels=False
    )

    fig.update_yaxes(
        showticklabels=False
    )

    return fig