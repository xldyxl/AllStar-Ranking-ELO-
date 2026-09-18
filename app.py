import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(
    page_title="올스타리그 ELO 랭킹",
    page_icon="🏆",
    layout="centered"
)

st.title("🏆 올스타리그 랭킹")
st.write("최신 경기 결과가 반영된 실시간 ELO 랭킹입니다.")

EXCEL_FILE_PATH = "Ranking_Data.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE_PATH)

    # 1) '진행된 경기 수' 컬럼까지만 데이터 자르기 (뒤쪽 Unnamed 빈 열들 자동 제거)
    if '진행된 경기 수' in df.columns:
        col_limit = df.columns.get_loc('진행된 경기 수') + 1
        df = df.iloc[:, :col_limit]

    # 2) 모든 컬럼 가운데 정렬 및 소수점 정리 (소수점 1자리로 깔끔하게)
    column_config = {}
    for col in df.columns:
        if df[col].dtype in ['float64', 'float32']:
            column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%.1f")
        elif df[col].dtype in ['int64', 'int32']:
            column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%d")
        else:
            column_config[col] = st.column_config.TextColumn(col, alignment="center")

    # 3) 위아래 스크롤바를 없애기 위해 전체 행 높이 자동 계산
    table_height = (len(df) + 1) * 36 + 15

    # 4) 표 출력
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=table_height,  # 높이를 행 개수에 맞추어 스크롤바 제거
        column_config=column_config
    )

except Exception as e:
    st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
