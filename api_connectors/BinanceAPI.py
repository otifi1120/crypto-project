import websocket
import json
import pandas as pd
import rel
from binance.client import Client

client = Client()
dict_ = client.get_exchange_info()
cryptos = [sym['symbol'] for sym in dict_['symbols'] if sym['symbol'].endswith('USDT')]
print(len(cryptos))

cryptos = [crypt.lower() + '@kline_1m' for crypt in cryptos]

endpoint = '/'.join(cryptos)

def transform(data):
    real_data = data['data']['k']['c']
    evt_time = pd.to_datatime([data['data']['E']], unit='ms')
    df = pd.DataFrame(real_data, columns=[data['data']['s']], index = [evt_time])
    df.index.name = 'timestamp'
    df = df.astype(float)
    df = df.reset_index()
    print(df)
    return df

stream_df = pd.DataFrame()

def on_message(ws, message):
    json_response = json.loads(message)
    print(json_response)
    with open("../datasets/binance_messages.txt", "a") as f:
        f.write(json.dumps(json_response) + "\n")

socket = "wss://stream.binance.com:9443/stream?streams="+endpoint

ws = websocket.WebSocketApp(socket, on_message=on_message)
ws.run_forever()
