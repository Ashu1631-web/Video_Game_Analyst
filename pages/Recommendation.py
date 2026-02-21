import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

st.title("🎯 Game Recommendation Engine")

@st.cache_data
def load():
    games = pd.read_csv("data/games.csv")
    return games

df = load()

df = df[["Title","Rating","Wishlist","Genres"]].dropna()

le = LabelEncoder()
df["Genres"] = le.fit_transform(df["Genres"])

features = df[["Rating","Wishlist","Genres"]]

similarity = cosine_similarity(features)

game_list = df["Title"].values
selected_game = st.selectbox("Select a Game", game_list)

if st.button("Recommend"):
    idx = df[df["Title"]==selected_game].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    recommended = [df.iloc[i[0]]["Title"] for i in scores]
    
    st.subheader("Recommended Games:")
    for game in recommended:
        st.write(game)
