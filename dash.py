import plotly.express as px
import streamlit as st
from data_e import *


Names , Symbol_map = sympol_list()
name = st.sidebar.selectbox('Select Ticker', Names)
symbol = Symbol_map.get(name)
end_date = st.sidebar.date_input('End Date')

input_dict = {'symbol': symbol, 'currency': 'USD', 'limit_value': 2000, 'exchange_name': 'CCCAGG', 'end_date': end_date}

crypto_compare, crypto_messari = st.tabs(['Crypto Comaper', 'Messari'])

price_list, features = [], []
prices = ['open', 'close', 'high', 'low']
price_list.append(st.sidebar.checkbox(prices[0]))
price_list.append(st.sidebar.checkbox(prices[1]))
price_list.append(st.sidebar.checkbox(prices[2]))
price_list.append(st.sidebar.checkbox(prices[3]))
for i, p in enumerate (price_list, 0):
    if p:
        features.append(prices[i])

with crypto_compare:
    st.title('Crypto Comaper')
    df_c = crypto_c(input_dict)
    df_c = df_c[features]
    try:
        fig = px.line(df_c, x = df_c.index, y = df_c.columns, title = name)
        st.plotly_chart(fig)
    except:
        pass
    st.write(df_c[features])

with crypto_messari:
    st.title('Messari')
    df_m = crypto_m(input_dict)
    df_m = df_m[features]
    try:
        fig = px.line(df_m, x = df_m.index, y = df_m.columns, title = name)
        st.plotly_chart(fig)
    except:
        pass
    st.write(df_m[features])