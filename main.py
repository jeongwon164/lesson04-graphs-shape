import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", page_icon="🎬", layout="wide")
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 10위권에 든 영화 216편의 요약 데이터를 살펴봅니다.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    df["openDt"] = pd.to_datetime(df["openDt"].astype(str), format="%Y%m%d", errors="coerce")
    df["genre"] = df["genre"].fillna("미상").astype(str).str.split("|").str[0].str.strip()
    for col in ["first_scrn", "first_show", "first_week_audi", "total_audi", "days_in_top10"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()

st.header("그래프 1. 장르별 영화 편수")
genre_counts = df["genre"].replace("", "미상").value_counts().rename_axis("genre").reset_index(name="count")

fig1 = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수",
)
fig1.update_traces(
    textinfo="percent",
    hovertemplate="장르: %{label}<br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>",
)
fig1.update_layout(legend_title_text="장르", margin=dict(l=20, r=20, t=70, b=20))
st.plotly_chart(fig1, use_container_width=True)
st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 통해 알 수 있는 내용을 한 문장으로 적어 주세요.")

st.divider()
st.header("그래프 2")
st.caption("다음 그래프를 이 구역에 추가하세요.")
st.divider()
st.header("그래프 3")
st.caption("다음 그래프를 이 구역에 추가하세요.")
st.divider()
st.header("그래프 4")
st.caption("다음 그래프를 이 구역에 추가하세요.")

# 그래프 2
st.divider()
st.header("그래프 2. 장르별 영화 총 관객 트리맵")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna(subset=["genre", "movieNm", "total_audi"]).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객",
)

fig2.update_traces(
    hovertemplate=(
        "장르: %{parent}<br>"
        "영화명: %{label}<br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(l=20, r=20, t=70, b=20),
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 통해 알 수 있는 내용을 한 문장으로 적어 주세요.")


# 그래프 3
st.divider()
st.header("그래프 3. 총 관객 분포")

hist_df = df.dropna(subset=["total_audi", "movieNm"]).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객",
        "count": "영화 편수",
    },
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    margin=dict(l=20, r=20, t=70, b=20),
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 영화가 많이 몰린 구간 계산
counts, edges = __import__("numpy").histogram(
    hist_df["total_audi"],
    bins=20,
)
peak_bin = int(counts.argmax())
peak_low = edges[peak_bin]
peak_high = edges[peak_bin + 1]

most_watched = hist_df.loc[hist_df["total_audi"].idxmax()]

peak_low_text = f"{peak_low:,.0f}명"
peak_high_text = f"{peak_high:,.0f}명"

st.markdown("**이 그래프로 알 수 있는 것**")
st.info(
    f"대부분의 영화가 몰려 있는 구간은 약 **{peak_low_text}~{peak_high_text}**이고, "
    f"총 관객이 가장 많은 영화는 **{most_watched['movieNm']}**로 "
    f"총 **{most_watched['total_audi']:,.0f}명**의 관객을 기록했습니다."
)


# 앞으로 추가할 그래프 공간
st.divider()
st.header("그래프 4")
st.caption("다음 그래프를 이 구역에 추가하세요.")
