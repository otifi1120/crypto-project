from CoinMarketAPI import CoinMarketCapAPI
import pandas as pd

class DataTransformer:
    def __init__(self, api_client):
        self.api_client = api_client

    def transform_coinmarketcap_data(self):
        data = self.api_client.get_crypto_data()
        final_data = pd.DataFrame()

        for crypto in data:
            cryptos_df = pd.DataFrame()
            cryptos_dic = crypto['quote']
            cryptos_df = pd.DataFrame.from_dict(cryptos_dic, orient='index')
            cryptos_df.reset_index(inplace=True)
            final_data = final_data._append(cryptos_df, ignore_index=True)

        return final_data

    def save_to_csv(self, dataframe, filename):
        dataframe.to_csv(filename, index=False)
        print(f"DataFrame saved to {filename}")

api_client = CoinMarketCapAPI('BNB')
data_transformer = DataTransformer(api_client)
transformed_data = data_transformer.transform_coinmarketcap_data()
data_transformer.save_to_csv(transformed_data, "../datasets/coinmarketcap_bnb_data.csv")
