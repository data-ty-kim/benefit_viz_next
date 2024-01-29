import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.common_util import path_to_project_root

# Firebase init
root_dir = path_to_project_root('benefit_viz_next')
cred = credentials.Certificate(
    f'{root_dir}/config/datahub-firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Plot 1 to test the Dash
# bring parameters
param1 = 'AAEXNEA8lKEv5dYsaLBzlX3'
param2 = 'AAEAdCf4UZeMuNMCKQckIel'
param3 = '2018010361'

# df의 열 설정
column_name = ['semester', 'KEDI_sch_div', 'sch_nm', 'amt']

# 장학금 데이터
scholarships = db.collection('Student-Scholarship-Data').document(param1).collection('Semester').stream()
df_sch = pd.DataFrame(columns=column_name)
for semester in scholarships:
    df_0 = pd.DataFrame(semester.to_dict()['sch'])
    df_0['amt'] = df_0['tuition_fee'] + df_0['etc_fee'] + df_0['admission_fee']
    df_1 = df_0[['KEDI_sch_div', 'sch_nm', 'amt']
    ].groupby(['KEDI_sch_div', 'sch_nm'], as_index=False).sum(numeric_only=True)
    df_1['semester'] = semester.id
    df_sch = pd.concat([df_sch, df_1])
df_sch.replace({'KEDI_sch_div': {'국가': '국가장학'}}, inplace=True)

# 연구비 데이터
funds = db.collection('Student-Fund-Data').document(param1).collection('Semester').stream()
df_fund = pd.DataFrame(columns=column_name)
for semester in funds:
    df = pd.DataFrame(semester.to_dict()['fund']
                        ).groupby(['desc_div_nm', 'desc_div_cd'], as_index=False).sum(numeric_only=True)
    df['semester'] = semester.id
    df['sch_nm'] = '연구비'
    df = df.drop('desc_div_cd', axis=1
                    ).rename(columns={'desc_div_nm': 'KEDI_sch_div'})
    df_fund = pd.concat([df_fund, df])

# 장학금 & 연구비 dataframe 만들기
df_chart = pd.concat([df_sch.fillna('기타'), df_fund.fillna(0)])
df_chart = df_chart.sort_values(by='semester')
df_chart.rename(columns={'semester': '학기', 'KEDI_sch_div': '유형',
                            'sch_nm': '명칭', 'amt': '수혜금액'}, inplace=True)

# ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
# KEDI_sch_div 항목은 아래의 총 9개이다. 엑셀 파일의 내용과 차이가 존재
# '국가장학' '저소득' '기타' '성적우수' '근로' '재난' '사설및기타' '교직원' '통계조사 미반영'
# 연구비 항목까지 하면 총 11개이므로, '사설및기타' 항목을 '기타' 항목으로 같이 묶어서 총 10개로 만듦
df_chart['유형'].replace('사설및기타', '기타', inplace=True)

# 차트 유형 정렬을 위한 순서 지정
dict_category_order = {
    '유형': ['(연구) 월인건비', '(연구) 연구수당',
            '(장학) 근로', '(장학) 국가장학', '(장학) 기타', '(장학) 성적우수', '(장학) 교직원',
            '(장학) 재난', '(장학) 저소득', '(장학) 통계조사 미반영',
            ],
    '학기': sorted(df_chart['학기'].unique())}

# content1
fig_area_1 = px.bar(df_chart.replace({'유형':
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
                                            }}),

                    x="학기", y="수혜금액", color='유형', barmode="stack"
                    , category_orders=dict_category_order
                    , hover_data={'유형': True, '학기': True, '수혜금액': True}
                    )

fig_area_1.update_xaxes(
    tickangle=0,  # x 눈금명 각도
    title_text="<b>학기</b>",
    title_font={"size": 18},
    title_standoff=21)  # title 떨어져있는 정도

fig_area_1.update_yaxes(
    tickangle=0,  # y 눈금명 각도
    title_text="<b>수혜금액</b>",
    title_font={"size": 18},
    title_standoff=21,  # title 떨어져있는 정도
    tickformat=","  # d3-format (파이썬 format이 아닌 듯)
)

if df_chart.empty:
    fig_area_1.update_layout(
        font={'family': 'NanumGothic'},
        annotations=[dict(
            text="장학금 및 연구비 수혜 내역이 없습니다.",
            x=2.5, y=1.5,
            xanchor="center", yanchor="middle",
            showarrow=False,
            font=dict(color="#252930", size=32, family="NanumGothic")
        )])
else:
    fig_area_1.update_layout(
        font={'family': 'NanumGothic'})
