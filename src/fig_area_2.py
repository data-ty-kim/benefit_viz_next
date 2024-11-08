import plotly.express as px
import plotly.graph_objects as go

def fig_area_2(df):

    fig_area_2 = go.Figure(data=[go.Scatter(
                    x= df['x'], 
                    y=df['y'], 
                    mode='markers',
                    marker=dict(
                    size= df['Size'],
                    sizemode='area',
                    sizeref=2.*max(df['Size'])/(160.**2),
                    color=df['color']), 
                    customdata=df[['Size', '장학금명', '기수혜']].values, 
                    hovertemplate="<br>".join([

                                                " %{customdata[1]}"
                                        ]),
                    name=""
    )])


    fig_area_2.add_trace(go.Scatter
                        (
                            x=df.loc[df['기수혜'] == 'Y', 'x'], 
                            y=df.loc[df['기수혜'] == 'Y', 'y'], 
                            mode='text', 
                            text='🎓', 
                            textfont=dict(size=45),
                            textposition='middle center',
                            name=""
                        ))
    
     #Preparing wrapped text for putting inside bubbles
    def wrap_text_to_fit_bubble(text, bubble_size):
        char_limit = max(5, bubble_size // 10)  
        words = text.split(" ")
        wrapped_text, line = "", ""
        
        for word in words:
            if len(line) + len(word) + 1 <= char_limit:
                line += (word + " ")
            else:
                wrapped_text += line.strip() + "<br>"
                line = word + " "
        wrapped_text += line.strip()
        
        return wrapped_text

    df['wrapped_labels'] = [wrap_text_to_fit_bubble(text, size) for text, size in zip(
        df['장학금명'], df['Size'])]


    fig_area_2.add_trace(go.Scatter
                        (
                            x=df.loc[df['기수혜'] == 'N', 'x'], 
                            y=df.loc[df['기수혜'] == 'N', 'y'], 
                            mode='text', 
                            text=df.loc[df['기수혜'] == 'N', 'wrapped_labels'],
                            textposition='middle center',
                            name=""
                        ))



    fig_area_2.update_xaxes(range=(-1,7.5),visible= False)
    fig_area_2.update_yaxes(range=(-3,11),visible= False,)
    fig_area_2.update_legends(visible=False)
    if df.empty:
        fig_area_2.update_layout(
            font={'family': 'NanumSquare'},
            annotations=[dict(
                text="<span style='font-size: 1.4rem'>장학금 및 연구비<br>수혜 내역이 없습니다.</span>",
                x=2.5, y=1.5,
                xanchor="center", yanchor="middle",
                showarrow=False,
                font=dict(color="#252930", size=32, family="NanumSquare")
            )])
    else:
        fig_area_2.update_layout(
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
                    margin=dict(t=0,b=0,r=0,l=0),
                    plot_bgcolor='#F9F9F9',
                    paper_bgcolor='#F9F9F9',
                    xaxis_fixedrange=True, 
                    yaxis_fixedrange=True,
                    width=325,
                    height=450
                )
    return fig_area_2