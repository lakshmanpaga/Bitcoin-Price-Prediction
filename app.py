import yfinance as yf
import streamlit as st
from forex_python.converter import CurrencyRates
from babel.numbers import format_currency
import datetime
import pandas as pd
from datetime import date
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
from dateutil.relativedelta import relativedelta


c = CurrencyRates()
dollar=c.get_rate('USD', 'INR')
crypto_mapping = {"Bitcoin": "BTC-USD"}

st.title("Bitcoin ₿ Price Prediction")
st.header('By ADITYA COLLEGE OF ENGINEERING AND TECHNOLOGY STUDENTS')
st.subheader("        -P.V.V.S.S LAKSHMAN ,P.DINESHKUMAR ,M.AJAY SAKTHI SHANKAR ,V.V.V DURGA PRASAD -    ")

st.write(
    "In simplistic terms, Cryptocurrency is a digitised asset spread through multiple computers in a shared network. The decentralised nature of this network shields them from any control from government regulatory bodies. The term “cryptocurrency” in itself is derived from the encryption techniques used to secure the network.What is Bitcoin? Bitcoin is a cryptocurrency built by using blockchain. Bitcoin value depends on various aspects. Predicting the price of bitcoin is the hardest job. We are building a machine model which will predict the price of bitcoin based on the previous history data from 2014 to today and analysis tools. Our problem is a regression problem predicting the value of bitcoin. We use various ml regression algorithms to predict the value and pick the best one.")
st.image("https://www.dropbox.com/t/D9GepdwveB02TLCt")
crypto_option = "Bitcoin"
symbol_crypto = crypto_mapping[crypto_option]
data_crypto = yf.Ticker(symbol_crypto)

start_date = st.sidebar.date_input("Start Date", date.today() - relativedelta(months=3))
end_date = st.sidebar.date_input("End Date", date.today())

data_interval = "1d"
value_selector =  "Close"

days = st.sidebar.selectbox(
    "Next", (7,10,30,50)
)


if st.sidebar.button("Visualize"):

    crypto_hist = data_crypto.history(
        start=start_date, end=end_date, interval=data_interval)
    model = ARIMA(crypto_hist.Close, order=(2, 1, 0))
    model_fit = model.fit()
    output = model_fit.forecast(days)
    predict = []
    for i in output:
        predict.append(i)
    dates1 =[]
    colour = []
    for i in crypto_hist.index:
        dates1.append(i.date())
        colour.append('Old')
    today = datetime.date.today()
    dates2 = []
    for i in range(days):
        dates2.append(today + datetime.timedelta(days=i))
        colour.append('predicted')


    df = pd.DataFrame()
    df["Date"] = dates1+dates2
    df["price"] = predict+crypto_hist.Close.tolist()
    df["Type"] = colour

    fig = px.line(df, x="Date", y="price", color="Type", title="Bitcoin Prediction")


    predict_inr = str(format_currency(int(int(predict[0]) * dollar), 'INR', locale='en_IN'))
    predict_inr1 = str(format_currency(int(int(predict[1]) * dollar), 'INR', locale='en_IN'))

    df = pd.DataFrame()
    df["Date"] = dates1 + dates2
    df["price"] = predict + crypto_hist.Close.tolist()
    df["Type"] = colour

    fig = px.line(df, x="Date", y="price", color="Type", title="Bitcoin Prediction")

    predict_inr = str(format_currency(int(int(predict[0]) * dollar), 'INR', locale='en_IN'))
    predict_inr1 = str(format_currency(int(int(predict[1]) * dollar), 'INR', locale='en_IN'))

    st.plotly_chart(fig)
    st.write("Inr Value For Tomorrow Prediction : ")
    st.success(predict_inr)
    st.write("Inr Value For Day After Tomorrow Prediction : ")
    st.success(predict_inr1)


