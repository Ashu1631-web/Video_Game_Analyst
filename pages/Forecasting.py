import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

st.title("ML Sales Prediction")

@st.cache_data
def load():
    games = pd.read_csv("data/games.csv")
    sales = pd.read_csv("data/vgsales.csv")
    sales.rename(columns={"Name":"Title"}, inplace=True)
    df = pd.merge(games, sales, on="Title", how="inner")
    return df

df = load()

df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Encoding safely
le_genre = LabelEncoder()
le_platform = LabelEncoder()
le_publisher = LabelEncoder()

df["Genre"] = le_genre.fit_transform(df["Genre"].astype(str))
df["Platform"] = le_platform.fit_transform(df["Platform"].astype(str))
df["Publisher"] = le_publisher.fit_transform(df["Publisher"].astype(str))

df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Wishlist"] = pd.to_numeric(df["Wishlist"], errors="coerce")
df["Global_Sales"] = pd.to_numeric(df["Global_Sales"], errors="coerce")

df.dropna(inplace=True)

X = df[["Genre","Platform","Publisher","Rating","Wishlist"]]
y = df["Global_Sales"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestRegressor()
model.fit(X_train,y_train)

score = r2_score(y_test, model.predict(X_test))
st.metric("R² Score", round(score,3))
