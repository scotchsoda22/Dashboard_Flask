import pandas as pd
import numpy as np
import requests    
import time
import json


class exchange:
  def ex_bittrex(self):
    r = requests.get("https://api.bittrex.com/v3/markets/tickers")
    data = r.json()
    df = pd.DataFrame(data)
    df = df[['symbol', 'bidRate', 'askRate']]
    df = df[df['symbol'].str.endswith("USDT")==True]
    df['symbol'] = df['symbol'].str.replace('-USDT','')
    df.insert(0, 'exchange', 'bittrex')
    df['bidRate'] = pd.to_numeric(df['bidRate'])
    df['askRate'] = pd.to_numeric(df['askRate'])
    df = df[~(df == 0).any(axis=1)]



    return df

  def ex_gate(self):
    r = requests.get("https://api.gateio.ws/api/v4/spot/tickers")
    data = r.json()
    df = pd.DataFrame(data)
    df = df[['currency_pair', 'highest_bid', 'lowest_ask']]
    df.columns = ['symbol', 'bidRate', 'askRate']
    df = df[df['symbol'].str.endswith("_USDT")==True]
    df['symbol'] = df['symbol'].str.replace('_USDT','')
    df.insert(0, 'exchange', 'gate')
    df['bidRate'].replace('', np.nan, inplace=True)  
    df['askRate'].replace('', np.nan, inplace=True)  
    df = df[df["askRate"].str.contains("NaN") == False]
    df = df[df["bidRate"].str.contains("NaN") == False]
    df['bidRate'] = pd.to_numeric(df['bidRate'])
    df['askRate'] = pd.to_numeric(df['askRate'])

    return df

  def combine_dataframes(self):
    df_list = []
    for method in dir(self):
        if method.startswith("ex"):
            df = getattr(self, method)()
            if isinstance(df, pd.DataFrame):
                df_list.append(df)
    final_df = pd.concat(df_list)
    return final_df