import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(layout="wide")

# 2. 엑셀 데이터 불러오기
df = pd.read_excel('Ranking_Data.xlsx')

# 3. '패' 열(G열)까지만 데이터 자르기
col_limit = df.columns.get_loc('패') + 1
df = df.iloc[:, :col_limit]

# 4. '참가자고유ID' 컬럼 삭제 (존재할 경우)
if '참가자고유ID' in df.columns:
    df = df.drop(columns=['참가자고유ID'])

# 5. 맨 왼쪽에 '순위' 열 추가 (1등부터 순차적으로 부여)
df.insert(0, '순위', range(1, len(df) + 1))

# 6. 컬럼 폭 최적화 및 정렬 (픽셀 단위로 세밀하게 조정)
column_config = {
    "순위": st.column_config.NumberColumn("순위", alignment="center", format="%d", width=50),
    "17th ELO": st.column_config.NumberColumn("17th ELO", alignment="center", format="%.1f", width=90),
    "닉네임": st.column_config.TextColumn("닉네임", alignment="center", width=160),
    "팀명": st.column_config.TextColumn("팀명", alignment="center", width=220), 
    "17시즌 경기 수": st.column_config.NumberColumn("17시즌 경기 수", alignment="center", format="%d", width=110),
    "승": st.column_config.NumberColumn("승", alignment="center", format="%d", width=60),
    "무": st.column_config.NumberColumn("무", alignment="center", format="%d", width=60),
    "패": st.column_config.NumberColumn("패", alignment="center", format="%d", width=60),
}

# 7. 예상치 못한 다른 컬럼 대비 기본 정렬 (안전 장치)
for col in df.columns:
    if col not in column_config:
        if df[col].dtype in ['float64', 'float32']:
            column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%.1f")
        elif df[col].dtype in ['int64', 'int32']:
            column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%d")
        else:
            column_config[col] = st.column_config.TextColumn(col, alignment="center")

# 8. 위아래 스크롤바를 없애기 위해 전체 행 높이 자동 계산
table_height = (len(df) + 1) * 36 + 15

# 9. 표 출력 (use_container_width=False 로 화면 꽉 채우기 해제)
st.dataframe(
    df,
    use_container_width=False, 
    hide_index=True,
    height=table_height,
    column_config=column_config
)
