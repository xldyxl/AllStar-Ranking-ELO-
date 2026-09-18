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

    # 1) '진행된 경기 수' 컬럼까지만 데이터 자르기
    if '진행된 경기 수' in df.columns:
        col_limit = df.columns.get_loc('진행된 경기 수') + 1
        df = df.iloc[:, :col_limit]

    # 2) '참가자고유ID' 컬럼 삭제
    if '참가자고유ID' in df.columns:
        df = df.drop(columns=['참가자고유ID'])

    # 3) '순위' 열 추가
    df.insert(0, '순위', range(1, len(df) + 1))

    # 4) 데이터 타입에 따른 소수점 포맷팅을 미리 적용
    # Pandas Styler를 사용하기 위해 미리 데이터 형식을 맞춤
    format_dict = {}
    for col in df.columns:
        if df[col].dtype in ['float64', 'float32']:
            format_dict[col] = "{:.1f}"
        elif df[col].dtype in ['int64', 'int32'] and col != '순위':
            format_dict[col] = "{:d}"

    # 5) Pandas Styler를 이용한 CSS 강제 적용 (헤더 및 셀 데이터 모두 가운데 정렬)
    # th: 헤더(열 제목), td: 셀 데이터
    styled_df = df.style.format(format_dict).set_properties(**{'text-align': 'center'}).set_table_styles(
        [dict(selector='th', props=[('text-align', 'center')])]
    )

    # 6) 위아래 스크롤바를 없애기 위해 전체 행 높이 계산
    table_height = (len(df) + 1) * 36 + 15

    # 7) 표 출력 (Styler 객체를 직접 넘김)
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=table_height,
        column_config={
            "닉네임": st.column_config.TextColumn("닉네임", width=140),
            "팀명": st.column_config.TextColumn("팀명", width=140),
        }
    )

except Exception as e:
    st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
