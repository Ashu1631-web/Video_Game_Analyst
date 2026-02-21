import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

st.title("🤖 ML Sales Prediction")

@st.cache_data
def load():
    games = pd.read_csv("data/games.csv")
    sales = pd.read_csv("data/vgsales.csv")
    sales.rename(columns={"Name":"Title"}, inplace=True)
    df = pd.merge(games, sales, on="Title", how="inner")
    return df

df = load()

df = df[["Genre","Platform","Publisher","Rating","Wishlist","Global_Sales"]].dropna()

le = LabelEncoder()
df["Genre"] = le.fit_transform(df["Genre"])
df["Platform"] = le.fit_transform(df["Platform"])
df["Publisher"] = le.fit_transform(df["Publisher"])

X = df.drop("Global_Sales", axis=1)
y = df["Global_Sales"]

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model = RandomForestRegressor()
model.fit(X_train,y_train)

pred = model.predict(X_test)

score = r2_score(y_test,pred)

st.metric("Model R² Score", round(score,3))

st.subheader("Predict New Game Sales")

rating = st.slider("Rating", 0.0, 5.0, 4.0)
wishlist = st.number_input("Wishlist Count", 0, 1000000, 50000)

if st.button("Predict"):
    sample = X.iloc[0:1].copy()
    sample["Rating"] = rating
    sample["Wishlist"] = wishlist
    prediction = model.predict(sample)
    st.success(f"Predicted Global Sales (Millions): {round(prediction[0],2)}")
