import streamlit as st
import pandas as pd
from prophet import Prophet

st.title("Sales Forecasting")

sales = pd.read_csv("data/vgsales.csv")

yearly = sales.groupby("Year")["Global_Sales"].sum().reset_index()
yearly.columns = ["ds","y"]
yearly["ds"] = pd.to_datetime(yearly["ds"], format="%Y")

model = Prophet()
model.fit(yearly)

future = model.make_future_dataframe(periods=5, freq="Y")
forecast = model.predict(future)

st.line_chart(forecast.set_index("ds")["yhat"])
