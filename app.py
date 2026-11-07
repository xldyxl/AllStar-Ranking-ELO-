import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(layout="wide")

# 2. 엑셀 데이터 불러오기
df = pd.read_excel('Ranking_Data.xlsx')

# 3. '순위 변동' 열까지 데이터 자르기 (지정된 열까지 자동으로 자름)
col_limit = df.columns.get_loc('순위 변동') + 1
df = df.iloc[:, :col_limit]

# 4. '참가자고유ID' 컬럼 삭제 (존재할 경우)
if '참가자고유ID' in df.columns:
    df = df.drop(columns=['참가자고유ID'])

# 5. (요청에 따라 코드로 순위 열을 추가하던 로직은 삭제되었습니다)

# 6. 컬럼 폭 최적화 및 정렬 (형식 지정)
column_config = {
    "순위": st.column_config.NumberColumn("순위", alignment="center", format="%d", width=60),
    "18th ELO": st.column_config.NumberColumn("18th ELO", alignment="center", format="%.2f", width=100), # 소수점 둘째 자리까지 표시
    "±": st.column_config.NumberColumn("±", alignment="center", format="%+.1f", width=70), # ★ 양수일 때 +가 붙도록 설정
    "닉네임": st.column_config.TextColumn("닉네임", alignment="center", width=160),
    "팀명": st.column_config.TextColumn("팀명", alignment="center", width=220), 
    "18시즌 경기 수": st.column_config.NumberColumn("18시즌 경기 수", alignment="center", format="%d", width=110),
    "승": st.column_config.NumberColumn("승", alignment="center", format="%d", width=60),
    "무": st.column_config.NumberColumn("무", alignment="center", format="%d", width=60),
    "패": st.column_config.NumberColumn("패", alignment="center", format="%d", width=60),
    "개막 순위": st.column_config.NumberColumn("개막 순위", alignment="center", format="%d", width=90),
    "순위 변동": st.column_config.TextColumn("순위 변동", alignment="center", width=90), # 상승/하강 기호 및 텍스트 표시
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

# 9. 표 출력
st.dataframe(
    df,
    use_container_width=False, 
    hide_index=True,
    height=table_height,
    column_config=column_config
)
