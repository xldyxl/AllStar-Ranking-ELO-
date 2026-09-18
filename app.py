import streamlit as st
import pandas as pd

# 1. 페이지 설정 (화면을 약간 넓게 쓰려면 layout="centered" 유지 혹은 "wide"로 변경 가능)
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

    # 1) '진행된 경기 수' 컬럼까지만 데이터 자르기 (뒤쪽 빈 열들 자동 제거)
    if '진행된 경기 수' in df.columns:
        col_limit = df.columns.get_loc('진행된 경기 수') + 1
        df = df.iloc[:, :col_limit]

    # 2) '참가자고유ID' 컬럼 삭제 (표시하지 않음)
    if '참가자고유ID' in df.columns:
        df = df.drop(columns=['참가자고유ID'])

    # 3) 맨 왼쪽에 '순위' 열 추가 (1등부터 순차적으로 부여)
    df.insert(0, '순위', range(1, len(df) + 1))

    # 4) 컬럼별 정렬 및 폭, 데이터 포맷 세밀한 설정 (닉네임 짤림 방지)
    # width 속성을 통해 닉네임과 팀명에는 넓은 공간을 주고, 숫자 데이터는 좁게 설정해 한눈에 들어오게 합니다.
    column_config = {
        "순위": st.column_config.NumberColumn("순위", alignment="center", format="%d", width="small"),
        "닉네임": st.column_config.TextColumn("닉네임", alignment="center", width="large"),
        "팀명": st.column_config.TextColumn("팀명", alignment="center", width="medium"),
        "16시즌 소프트리셋": st.column_config.NumberColumn("16시즌 소프트리셋", alignment="center", format="%.1f", width="small"),
        "17시즌 ELO": st.column_config.NumberColumn("17시즌 ELO", alignment="center", format="%.1f", width="small"),
        "+-": st.column_config.NumberColumn("+-", alignment="center", format="%.1f", width="small"),
        "진행된 경기 수": st.column_config.NumberColumn("진행된 경기 수", alignment="center", format="%d", width="small"),
    }

    # (선택 사항) 만약 엑셀에 예상치 못한 다른 컬럼이 추가될 경우를 대비한 기본 가운데 정렬 처리
    for col in df.columns:
        if col not in column_config:
            if df[col].dtype in ['float64', 'float32']:
                column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%.1f")
            elif df[col].dtype in ['int64', 'int32']:
                column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%d")
            else:
                column_config[col] = st.column_config.TextColumn(col, alignment="center")

    # 5) 위아래 스크롤바를 없애기 위해 전체 행 높이 자동 계산
    table_height = (len(df) + 1) * 36 + 15

    # 6) 표 출력
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=table_height,  # 높이를 행 개수에 맞추어 스크롤바 제거
        column_config=column_config
    )

except Exception as e:
    st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
