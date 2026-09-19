# 컬럼 폭 최적화 및 정렬 (픽셀 단위로 세밀하게 조정)
column_config = {
    "순위": st.column_config.NumberColumn("순위", alignment="center", format="%d", width=50),
    "17th ELO": st.column_config.NumberColumn("17th ELO", alignment="center", format="%.1f", width=90),
    "닉네임": st.column_config.TextColumn("닉네임", alignment="center", width=160),
    "팀명": st.column_config.TextColumn("팀명", alignment="center", width=220), # 아틀레티코 마드리드 등 긴 팀명을 위해 넓게
    "17시즌 경기 수": st.column_config.NumberColumn("17시즌 경기 수", alignment="center", format="%d", width=110),
    "승": st.column_config.NumberColumn("승", alignment="center", format="%d", width=60),
    "무": st.column_config.NumberColumn("무", alignment="center", format="%d", width=60),
    "패": st.column_config.NumberColumn("패", alignment="center", format="%d", width=60),
}

# 예상치 못한 다른 컬럼 대비 기본 정렬 (안전 장치)
for col in df.columns:
    if col not in column_config:
        if df[col].dtype in ['float64', 'float32']:
            column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%.1f")
        elif df[col].dtype in ['int64', 'int32']:
            column_config[col] = st.column_config.NumberColumn(col, alignment="center", format="%d")
        else:
            column_config[col] = st.column_config.TextColumn(col, alignment="center")

# 위아래 스크롤바를 없애기 위해 전체 행 높이 자동 계산
table_height = (len(df) + 1) * 36 + 15

# 표 출력
st.dataframe(
    df,
    use_container_width=False,  # ★ 핵심: 화면 꽉 채우기 끄기 (지정해둔 너비만 딱 차지하게 됨)
    hide_index=True,
    height=table_height,
    column_config=column_config
)
