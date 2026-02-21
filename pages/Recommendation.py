import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

st.title("Game Recommendation Engine")

games = pd.read_csv("data/games.csv")

games["Rating"] = pd.to_numeric(games["Rating"], errors="coerce")
games["Wishlist"] = pd.to_numeric(games["Wishlist"], errors="coerce")

games.dropna(subset=["Rating","Wishlist","Genres"], inplace=True)

le = LabelEncoder()
games["Genres"] = le.fit_transform(games["Genres"].astype(str))

features = games[["Rating","Wishlist","Genres"]].values

similarity = cosine_similarity(features)

selected = st.selectbox("Select Game", games["Title"])

if st.button("Recommend"):
    idx = games[games["Title"] == selected].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    for i in scores:
        st.write(games.iloc[i[0]]["Title"])
