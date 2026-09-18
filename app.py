import streamlit as st
import pandas as pd

# 1. 페이지 설정 (코드 최상단에 위치해야 합니다)
st.set_page_config(
    page_title="올스타리그 ELO 랭킹",
    page_icon="🏆",
    layout="centered"  # 화면을 넓게 쓰고 싶다면 "wide" 로 변경 가능합니다
)

st.title("🏆 올스타리그 랭킹")
st.write("최신 경기 결과가 반영된 실시간 ELO 랭킹입니다.")

# 엑셀 파일 로드
EXCEL_FILE_PATH = "Ranking_Data.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE_PATH)

    # 2. 표 디자인 및 가운데 정렬 설정
    st.dataframe(
        df,
        use_container_width=True,  # 표 폭을 대시보드 너비에 딱 맞게 확장
        hide_index=True,           # 좌측 기본 인덱스(0, 1, 2...) 숨기기
        column_config={
            "순위": st.column_config.NumberColumn("순위", alignment="center"),
            "닉네임": st.column_config.TextColumn("닉네임", alignment="center"),
            "팀명": st.column_config.TextColumn("팀명", alignment="center"),
            "ELO": st.column_config.NumberColumn("ELO", alignment="center", format="%.1f"),
            "변동": st.column_config.TextColumn("변동", alignment="center"),
        }
    )

except Exception as e:
    st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
