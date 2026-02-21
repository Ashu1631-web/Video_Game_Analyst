import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

st.title("📈 Sales Forecasting")

@st.cache_data
def load():
    sales = pd.read_csv("data/vgsales.csv")
    sales.rename(columns={"Name":"Title"}, inplace=True)
    return sales

df = load()

yearly = df.groupby("Year")["Global_Sales"].sum().reset_index()
yearly.columns = ["ds","y"]
yearly["ds"] = pd.to_datetime(yearly["ds"], format="%Y")

model = Prophet()
model.fit(yearly)

future = model.make_future_dataframe(periods=5, freq='Y')
forecast = model.predict(future)

fig = go.Figure()
fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"]))
st.plotly_chart(fig, use_container_width=True)
