
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", page_icon="🎬", layout="wide")
DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"
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
