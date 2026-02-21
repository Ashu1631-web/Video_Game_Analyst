import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

st.title("🎯 Smart Game Recommendation Engine")

games = pd.read_csv("data/games.csv")
games.dropna(inplace=True)

le = LabelEncoder()
games["Genres"] = le.fit_transform(games["Genres"].astype(str))

features = games[["Rating","Wishlist","Genres"]].values
similarity = cosine_similarity(features)

selected = st.selectbox("Select Game", games["Title"])

if st.button("Generate Recommendations"):
    idx = games[games["Title"]==selected].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores,key=lambda x:x[1],reverse=True)[1:6]

    st.subheader("Top Recommendations")
    for i in scores:
        st.write(f"{games.iloc[i[0]]['Title']}  (Score: {round(i[1],2)})")
