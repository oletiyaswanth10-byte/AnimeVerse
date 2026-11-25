import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from recommender import recommend_anime

st.set_page_config(page_title="AnimeVerse Dashboard", page_icon="🎌", layout="wide", initial_sidebar_state="expanded")
DATA = Path(__file__).parent / "data" / "anime.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

df = load_data()
genres = sorted({g.strip() for cell in df.genres for g in cell.split(",")})

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--bg:#10111d;--panel:#191a2b;--muted:#9294ad;--pink:#ed65b8;--cyan:#60d9e8;--purple:#9a7bff;}
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:radial-gradient(ellipse at 12% 0%,#302348 0%,#151525 38%,#0d0f19 100%);color:#f8f7ff}
.block-container{padding:1.35rem 2rem 2rem;max-width:1600px}
[data-testid="stSidebar"]{background:#151626;border-right:1px solid #303047}
[data-testid="stSidebar"] *{color:#d8d8eb}
.hero{border:1px solid #51466e;border-radius:22px;padding:22px 27px;background:linear-gradient(110deg,rgba(96,217,232,.13),rgba(154,123,255,.19),rgba(237,101,184,.13));box-shadow:0 0 28px #9a7bff18;margin-bottom:18px}
.hero h1{font-size:32px;font-weight:800;margin:0;color:#fff;letter-spacing:-1px}
.hero p{color:#b8bad0;margin:5px 0 0;font-size:13px}
.eyebrow{font-size:10px;letter-spacing:3px;color:#69dce8;font-weight:800;margin-bottom:7px}
.metric{background:linear-gradient(145deg,#202136,#171827);border:1px solid #35364e;border-radius:15px;padding:15px 17px;min-height:93px}
.metric small{color:#9c9eb8;font-size:10px;letter-spacing:1.4px;font-weight:700}
.metric strong{display:block;color:white;font-size:25px;margin-top:6px}
.panel{background:#191a2b;border:1px solid #303149;border-radius:16px;padding:16px 18px}
.anime{background:linear-gradient(145deg,#24233b,#171827);border:1px solid #373650;border-radius:15px;padding:15px;min-height:190px}
.anime h3{font-size:16px;color:#fff;margin:5px 0 7px}
.anime p{font-size:12px;color:#aeb0c7;line-height:1.5}
.tag{display:inline-block;background:#302b50;color:#d1c6ff;border:1px solid #514477;border-radius:30px;padding:3px 8px;font-size:10px;margin:2px}
.rating{color:#ffd37a;font-weight:800;font-size:12px}
.section{font-size:19px;font-weight:750;color:#fff;margin:12px 0}
div[data-testid="stTabs"] button{color:#c8c9dc}
.stButton>button{background:linear-gradient(90deg,#8066df,#d45fae);border:0;color:white;border-radius:10px;font-weight:700}
.stButton>button:hover{color:white;border:1px solid #65dce7}
input,textarea{background:#202136!important;color:white!important}
[data-testid="stDataFrame"]{border:1px solid #33344d;border-radius:12px;overflow:hidden}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎌 AnimeVerse")
    st.caption("YOUR PERSONAL ANIME HUB")
    st.markdown("---")
    page = st.radio("NAVIGATION", ["◈  Dashboard", "✦  Recommendations", "⌕  Anime Library", "▥  Analytics"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**QUICK FILTERS**")
    genre_filter = st.multiselect("Genres", genres)
    rating_filter = st.slider("Minimum rating", 0.0, 10.0, 7.0, 0.1)
    st.markdown("---")
    st.caption("✧ Discover your next favourite anime")

# Header bar
h1,h2,h3 = st.columns([5,1,1])
with h1:
    st.markdown('<div class="eyebrow">ANIME DISCOVERY PLATFORM</div>', unsafe_allow_html=True)
with h2:
    st.markdown('<div style="text-align:right;color:#aeb0c7;padding-top:8px">● Online</div>', unsafe_allow_html=True)
with h3:
    st.markdown('<div style="text-align:right;color:#aeb0c7;padding-top:8px">Profile ✿</div>', unsafe_allow_html=True)

st.markdown('<div class="hero"><div class="eyebrow">WELCOME TO YOUR UNIVERSE</div><h1>Anime Dashboard ✦</h1><p>Explore stories, discover hidden gems, and find your next favourite anime.</p></div>', unsafe_allow_html=True)

filtered = df[df.rating >= rating_filter].copy()
if genre_filter:
    filtered = filtered[filtered.genres.apply(lambda s: any(g in s for g in genre_filter))]

if page == "◈  Dashboard":
    a,b,c,d = st.columns(4)
    cards=[("ANIME IN LIBRARY",f"{len(df):,}"),("AVERAGE RATING",f"{df.rating.mean():.1f} / 10"),("COMMUNITY MEMBERS",f"{df.members.sum()/1e6:.1f}M"),("GENRES",str(len(genres)))]
    for col,(label,value) in zip([a,b,c,d],cards):
        col.markdown(f'<div class="metric"><small>{label}</small><strong>{value}</strong></div>',unsafe_allow_html=True)
    st.markdown('<div class="section">✧ Your anime overview</div>',unsafe_allow_html=True)
    left,right=st.columns([1.15,1])
    with left:
        counts=pd.Series([g.strip() for cell in df.genres for g in cell.split(",")]).value_counts().head(8).reset_index()
        counts.columns=["Genre","Anime"]
        fig=px.bar(counts,x="Genre",y="Anime",color="Anime",color_continuous_scale=["#6452b5","#5bd6e5"],template="plotly_dark")
        fig.update_layout(title="Genre popularity",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",coloraxis_showscale=False,height=300,margin=dict(t=45,b=10,l=5,r=5))
        st.plotly_chart(fig,use_container_width=True)
    with right:
        top=df.nlargest(6,"rating")[["title","rating"]]
        fig=px.line(top,x="title",y="rating",markers=True,template="plotly_dark")
        fig.update_traces(line_color="#ed65b8",marker_color="#60d9e8",line_width=3)
        fig.update_layout(title="Top anime ratings",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",height=300,margin=dict(t=45,b=10,l=5,r=5),yaxis_range=[7.5,10])
        st.plotly_chart(fig,use_container_width=True)
    st.markdown('<div class="section">✦ Featured anime</div>',unsafe_allow_html=True)
    featured=df.sort_values(["rating","members"],ascending=False).head(6)
    cols=st.columns(3)
    for i,(_,r) in enumerate(featured.iterrows()):
        tags="".join(f'<span class="tag">{g.strip()}</span>' for g in r.genres.split(",")[:3])
        cols[i%3].markdown(f'<div class="anime"><div class="rating">★ {r.rating:.1f} / 10</div><h3>{r.title}</h3>{tags}<p>{r.synopsis}</p><span style="color:#8588a4;font-size:10px">{int(r.episodes)} episodes · {r.members/1000:.0f}K members</span></div>',unsafe_allow_html=True)

elif page == "✦  Recommendations":
    st.markdown('<div class="section">✦ Find anime similar to your favourite</div>',unsafe_allow_html=True)
    st.markdown('<div class="panel">Choose a title and let the recommendation engine find anime with similar genres and story themes.</div>',unsafe_allow_html=True)
    selected=st.selectbox("Select your favourite anime",sorted(df.title))
    n=st.slider("How many recommendations?",3,10,5)
    if st.button("✧ Generate recommendations"):
        st.session_state.recs=recommend_anime(selected,df,n)
    if "recs" in st.session_state:
        st.success(f"Because you liked {selected}")
        for start in range(0,len(st.session_state.recs),2):
            cols=st.columns(2)
            for col,(_,r) in zip(cols,st.session_state.recs.iloc[start:start+2].iterrows()):
                tags="".join(f'<span class="tag">{g.strip()}</span>' for g in r.genres.split(",")[:3])
                col.markdown(f'<div class="anime"><div class="rating">{r.similarity:.1f}% MATCH</div><h3>{r.title}</h3>{tags}<p>{r.synopsis}</p><span class="rating">★ {r.rating:.1f}/10</span></div>',unsafe_allow_html=True)

elif page == "⌕  Anime Library":
    st.markdown('<div class="section">⌕ Explore the anime library</div>',unsafe_allow_html=True)
    query=st.text_input("Search anime, genre or story",placeholder="Try fantasy, ninja, romance...")
    view=filtered.copy()
    if query:
        mask=view.apply(lambda r: query.casefold() in (r.title+" "+r.genres+" "+r.synopsis).casefold(),axis=1)
        view=view[mask]
    sort=st.selectbox("Sort by",["Popularity","Highest rating","Title"])
    if sort=="Popularity": view=view.sort_values("members",ascending=False)
    elif sort=="Highest rating": view=view.sort_values("rating",ascending=False)
    else: view=view.sort_values("title")
    st.caption(f"{len(view)} titles found")
    st.dataframe(view[["title","genres","rating","episodes","members","synopsis"]],use_container_width=True,hide_index=True)

else:
    st.markdown('<div class="section">▥ Anime analytics studio</div>',unsafe_allow_html=True)
    left,right=st.columns(2)
    g=pd.Series([x.strip() for cell in df.genres for x in cell.split(",")]).value_counts().reset_index()
    g.columns=["Genre","Titles"]
    fig=px.pie(g,names="Genre",values="Titles",hole=.58,template="plotly_dark",title="Genre composition")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=360)
    left.plotly_chart(fig,use_container_width=True)
    fig=px.scatter(df,x="members",y="rating",size="episodes",color="rating",hover_name="title",template="plotly_dark",title="Popularity vs rating",color_continuous_scale=["#6555b8","#63dce8"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",height=360)
    right.plotly_chart(fig,use_container_width=True)
    st.markdown("#### Highest-rated anime")
    st.dataframe(df.nlargest(10,"rating")[["title","rating","members","episodes"]],use_container_width=True,hide_index=True)

st.markdown("---")
st.markdown('<div style="text-align:center;color:#777a96;font-size:11px;letter-spacing:1px">ANIMEVERSE · BUILT WITH PYTHON · STREAMLIT · SCIKIT-LEARN · PLOTLY</div>',unsafe_allow_html=True)
