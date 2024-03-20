import pandas as pd
import numpy as np
from datetime import timedelta
import requests
import cryptocompare


def sympol_list():
    raw_ticker_data = cryptocompare.get_coin_list()
    all_tickers = pd.DataFrame.from_dict(raw_ticker_data).T
    Symbols = list(all_tickers['Symbol'])
    Names = list(all_tickers['CoinName'])
    Symbol_map = {k: v for k, v in zip(Names, Symbols)}
    return Names , Symbol_map

def crypto_c(input_dict):
    raw_price_data = cryptocompare.get_historical_price_hour(input_dict['symbol'], input_dict['currency'],
                                            limit = input_dict['limit_value'], exchange=input_dict['exchange_name'],
                                            toTs = input_dict['end_date'])
    df = pd.DataFrame.from_dict(raw_price_data)
    df.set_index("time", inplace=True)
    df.index = pd.to_datetime(df.index, unit='s')
    df['datetimes'] = df.index
    df['datetimes'] = df['datetimes'].dt.strftime('%Y-%m-%d')
    return df

def crypto_m(input_dict):
    end_date = input_dict['end_date']
    start_date = end_date - timedelta(days = 6 * 30)
    symbol = input_dict['symbol']
    api_url = f'https://data.messari.io/api/v1/markets/binance-{symbol}-usdt/metrics/price/time-series?start={start_date}&end={end_date}&interval=1d'
    raw = requests.get(api_url).json()
    df = pd.DataFrame(raw['data']['values'])
    df = df.rename(columns = {0: 'date', 1: 'open', 2: 'high',3: 'low', 4: 'close', 5: 'volume'})
    df['date'] = pd.to_datetime(df['date'], unit = 'ms')
    df = df.set_index('date')
    return df
    
def set_date(df, date_col):
    df[date_col] = pd.to_datetime(df[date_col], format='%Y-%m-%dT%H:%M:%S.%f%z')
    df = df.set_index(date_col).drop(['index'], axis = 1)
    return df