import plotly.express as px
import plotly.graph_objects as go

def fig_area_2(df):

    # plot bubble chart
    fig_area_2 = px.scatter(df,
                    x= 'x', 
                    y='y', 
                    size= 'Size',
                    size_max=215,
                    color='기수혜', 
                    color_discrete_map={
                        'Y':'#7052EF',
                        'N':'#F15C6A'
                    },
                    hover_data={'x': False,'y':False, 'Size':False,'기수혜':False,'장학금명':False},
                    hover_name='장학금명'
                    #,width=300
                    , height=850
    )


    #update bubble chart- for Y labelling 🎓
    fig_area_2.add_trace(
        go.Scatter(
            x=df.loc[df['기수혜'] == 'Y', 'x'], 
            y=df.loc[df['기수혜'] == 'Y', 'y'], 
            mode='text', 
            text='🎓', 
            textfont=dict(size=45),
            textposition='middle center',
            showlegend=False
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


    #update bubble chart- for N labelling scholarship name
    fig_area_2.add_trace(
        go.Scatter(
            x=df.loc[df['기수혜'] == 'N', 'x'], 
            y=df.loc[df['기수혜'] == 'N', 'y'], 
            mode='text', 
            text=df.loc[df['기수혜'] == 'N', 'wrapped_labels'],
            textposition='middle center',
            textfont=dict(size=20),
            showlegend=False
            ))



    fig_area_2.update_xaxes(visible= False)
    fig_area_2.update_yaxes(visible= False,)
    fig_area_2.update_legends(visible=False)
    fig_area_2.update_legends(visible=False)
    fig_area_2.update_layout(
                legend=dict(
                    orientation="v",
                    yanchor='top',
                    xanchor='right',
                    y=1,
                    x=1,
                    title_font_family="NanumSquare",
                    font=dict(
                        family="NanumSquare",size=16,color="#919191")
                ),
                hoverlabel=dict(font=dict(size=30, family="NanumSquare",color='white'),
                                    align="left"),
                plot_bgcolor='#fff',
                paper_bgcolor='#fff',
                xaxis_fixedrange=True, 
                yaxis_fixedrange=True
            )

    return fig_area_2