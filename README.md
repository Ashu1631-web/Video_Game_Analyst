# 🎮 Enterprise Video Game Analytics Platform

An end-to-end Gaming Analytics System built using:

- Python
- Streamlit (Multi-page UI)
- SQL
- Machine Learning
- Prophet Forecasting
- Recommendation Engine

---

## 🚀 Features

### 📊 Interactive Dashboard
- Sales by Genre & Platform
- Regional Heatmaps
- Ratings vs Sales Analysis
- Engagement Metrics (Wishlist, Plays, Backlogs)

### 🤖 Machine Learning Sales Prediction
- Random Forest Regression
- R² Performance Metric
- Custom Sales Prediction Input

### 📈 Time Series Forecasting
- Facebook Prophet
- Future Sales Projection

### 🎯 Recommendation Engine
- Cosine Similarity
- Content-based Game Suggestions

---

## 📁 Project Structure

```
video-game-analytics-pro/
│
├── app.py
├── requirements.txt
├── README.md
│
├── pages/
│   ├── 1_📊_Dashboard.py
│   ├── 2_🤖_ML_Prediction.py
│   ├── 3_📈_Forecasting.py
│   ├── 4_🎯_Recommendation.py
│
├── data/
│   ├── games.csv
│   └── vgsales.csv
│
└── sql/
    └── schema.sql
```

---

## 🛠 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/video-game-analytics-pro.git
cd video-game-analytics-pro
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 🧠 Machine Learning Model

- Algorithm: Random Forest Regressor
- Target Variable: Global_Sales
- Features:
  - Genre
  - Platform
  - Publisher
  - Rating
  - Wishlist

---

## 📊 Forecasting Model

- Tool: Prophet
- Frequency: Yearly
- Output: 5-Year Future Sales Prediction

---

## 📌 Business Use Cases

- Game Marketing Strategy Optimization
- Sales Demand Forecasting
- Genre-Platform Profitability Analysis
- Engagement vs Revenue Insights
- Investment & Resource Allocation

---

## 🏆 Resume Highlight

Built a full-scale enterprise gaming analytics system integrating:
- Data Cleaning & SQL Modeling
- Interactive BI Dashboard
- Machine Learning Prediction
- Time Series Forecasting
- Recommendation Engine

---

## 📜 License

MIT License
