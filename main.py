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


# 그래프 4
st.divider()
st.header("그래프 4. 개봉일 스크린수와 총 관객의 관계")

scatter_df = df.dropna(
    subset=["first_scrn", "total_audi", "movieNm", "genre"]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르",
    },
)

fig4.update_traces(
    hovertemplate=(
        "영화: %{hovertext}<br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    margin=dict(l=20, r=20, t=70, b=20),
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수와 총 관객 사이의 관계를 영화별로 비교할 수 있습니다.")


# 그래프 5
st.divider()
st.header("그래프 5. 장르별 총 관객 분포")

box_df = df.dropna(
    subset=["genre", "total_audi", "movieNm"]
).copy()

# 영화가 10편 이상인 장르만 선택합니다.
genre_counts = box_df["genre"].value_counts()
eligible_genres = genre_counts[genre_counts >= 10].index.tolist()
box_df = box_df[box_df["genre"].isin(eligible_genres)].copy()

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객",
    },
)

fig5.update_traces(
    hovertemplate=(
        "영화: %{hovertext}<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    showlegend=False,
    margin=dict(l=20, r=20, t=70, b=20),
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("영화가 10편 이상인 장르별로 총 관객의 분포와 이상치를 비교할 수 있습니다.")


# 그래프 6
st.divider()
st.header("그래프 6. 개봉일 스크린수 × 총 관객 × 첫 주 관객")

bubble_df = df.dropna(
    subset=["first_scrn", "total_audi", "first_week_audi", "movieNm", "genre"]
).copy()

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=45,
    title="개봉일 스크린수와 총 관객의 관계 — 첫 주 관객 버블 크기",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "genre": "장르",
    },
)

fig6.update_traces(
    hovertemplate=(
        "영화: %{hovertext}<br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    margin=dict(l=20, r=20, t=70, b=20),
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("개봉일 스크린수와 총 관객의 관계를 살펴보면서 첫 주 관객이 많은 영화가 버블 크기로 크게 나타나는 것을 비교할 수 있습니다.")


# 그래프 7
st.divider()
st.header("그래프 7. 제작 국가 → 장르 영화 편수 선버스트")

sunburst_df = df[["nation", "genre"]].copy()

sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("미상")
    .astype(str)
    .str.strip()
    .replace("", "미상")
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .fillna("미상")
    .astype(str)
    .str.strip()
    .replace("", "미상")
)

# 같은 국가·장르 조합별 영화 편수를 집계합니다.
sunburst_counts = (
    sunburst_df.groupby(["nation", "genre"])
    .size()
    .reset_index(name="영화편수")
)

fig7 = px.sunburst(
    sunburst_counts,
    path=["nation", "genre"],
    values="영화편수",
    title="제작 국가 → 장르별 영화 편수",
)

fig7.update_traces(
    hovertemplate=(
        "항목: %{label}<br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    margin=dict(l=20, r=20, t=70, b=20),
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("제작 국가별로 어떤 장르의 영화가 많이 포함되어 있는지와 각 국가·장르의 영화 편수를 비교할 수 있습니다.")
