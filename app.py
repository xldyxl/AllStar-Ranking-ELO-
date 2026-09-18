import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="올스타리그 ELO 랭킹",
    page_icon="🏆",
    layout="centered"
)

st.title("🏆 올스타리그 랭킹")
st.caption("최신 경기 결과가 반영된 실시간 ELO 랭킹입니다.")

EXCEL_FILE_PATH = "Ranking_Data.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE_PATH)

    # '진행된 경기 수' 열까지만 자르기
    if '진행된 경기 수' in df.columns:
        col_limit = df.columns.get_loc('진행된 경기 수') + 1
        df = df.iloc[:, :col_limit]

    # 세로 스크롤 없이 전체 행이 나오도록 높이 계산
    table_height = (len(df) + 1) * 36 + 15

    # 컬럼별 폭(width) 및 가운데 정렬 개별 지정
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=table_height,
        column_config={
            "참가자고유ID": st.column_config.TextColumn("참가자고유ID", alignment="center", width="small"),
            "닉네임": st.column_config.TextColumn("닉네임", alignment="center", width="large"),
            "팀명": st.column_config.TextColumn("팀명", alignment="center", width="medium"),
            "16시즌 소프트리셋": st.column_config.NumberColumn("16시즌 소프트리셋", alignment="center", format="%.1f", width="small"),
            "17시즌 ELO": st.column_config.NumberColumn("17시즌 ELO", alignment="center", format="%.1f", width="small"),
            "+-": st.column_config.NumberColumn("+-", alignment="center", format="%.1f", width="small"),
            "진행된 경기 수": st.column_config.NumberColumn("진행된 경기 수", alignment="center", format="%d", width="small"),
        }
    )

except Exception as e:
    st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
