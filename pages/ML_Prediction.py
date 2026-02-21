import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

st.title("🤖 ML Sales Prediction Engine")

@st.cache_data
def load_data():
    games = pd.read_csv("data/games.csv")
    sales = pd.read_csv("data/vgsales.csv")
    sales.rename(columns={"Name":"Title"}, inplace=True)
    df = pd.merge(games,sales,on="Title")
    return df

df = load_data()
df.dropna(inplace=True)

le_g = LabelEncoder()
le_p = LabelEncoder()
le_pub = LabelEncoder()

df["Genre"] = le_g.fit_transform(df["Genre"].astype(str))
df["Platform"] = le_p.fit_transform(df["Platform"].astype(str))
df["Publisher"] = le_pub.fit_transform(df["Publisher"].astype(str))

X = df[["Genre","Platform","Publisher","Rating","Wishlist"]]
y = df["Global_Sales"]

with st.spinner("Training Model..."):
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    model = RandomForestRegressor()
    model.fit(X_train,y_train)
    score = r2_score(y_test,model.predict(X_test))

st.success("Model Trained Successfully")
st.metric("R² Score", round(score,3))

st.markdown("### Predict New Game")

rating = st.slider("Rating",0.0,5.0,4.0)
wishlist = st.number_input("Wishlist",0,100000,5000)

if st.button("Predict Sales"):
    sample = X.iloc[0:1].copy()
    sample["Rating"] = rating
    sample["Wishlist"] = wishlist
    pred = model.predict(sample)
    st.success(f"Predicted Sales (Millions): {round(pred[0],2)}")
