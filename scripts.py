import streamlit as st

import requests
import json
import time
from queries import *
import os
import pandas as pd 
from utils import trade_side_mapper

#from dotenv import load_dotenv
#load_dotenv()



class Flipsider:
    def __init__(self, API_KEY, TTL_MINUTES=60*24):
        self.API_KEY = API_KEY
        self.TTL_MINUTES = TTL_MINUTES

    def create_query(self, SQL_QUERY):
        r = requests.post(
            'https://node-api.flipsidecrypto.com/queries', 
            data=json.dumps({
                "sql": SQL_QUERY,
                "ttlMinutes": self.TTL_MINUTES
            }),
            headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": self.API_KEY},
        )
        if r.status_code != 200:
            raise Exception("Error creating query, got response: " + r.text + "with status code: " + str(r.status_code))

        return json.loads(r.text)    


    def get_query_results(self, token):
        r = requests.get(
            'https://node-api.flipsidecrypto.com/queries/' + token, 
            headers={"Accept": "application/json", "Content-Type": "application/json", "x-api-key": self.API_KEY}
        )
        if r.status_code != 200:
            raise Exception("Error getting query results, got response: " + r.text + "with status code: " + str(r.status_code))
        
        data = json.loads(r.text)
        if data['status'] == 'running':
            time.sleep(10)
            return self.get_query_results(token)

        return data


    def run(self, SQL_QUERY):
        query = self.create_query(SQL_QUERY)
        token = query.get('token')
        data = self.get_query_results(token)
        df = pd.DataFrame(data['results'],columns = data['columnLabels'])
        return df


def load_queries():
    df = pd.read_csv('query1.csv',index_col=0)
    df2 = pd.read_csv('query2.csv',index_col=0)
    return df,df2

st.cache()
def run_queries():
    # so sloooow
    bot = Flipsider(os.getenv('API_KEY'))
    df = bot.run(QUERY)
    #print('1 done')
    df2 = bot.run(QUERY2)
    #print('2 done')
    df3 = bot.run(QUERY3)
    return df,df2,df3


def modify_data(d):
    d = d.copy()
    d['SIZE'] = d['SIZE'].apply(short_changer)
    d['TRADESIZE'] = d['TRADESIZE'].apply(short_changer)
    # st.dataframe(d[d['TX_HASH']=='0x22343b8d3ed60a490690f2b7b91f01d5ce1a945808a486324468d8bae7aadd08'])

    d['BLOCK_TIMESTAMP'] = pd.to_datetime(d['BLOCK_TIMESTAMP'])
    d[['MARGIN','SIZE','TRADESIZE','LASTPRICE']] = d[['MARGIN','SIZE','TRADESIZE','LASTPRICE']].astype('float') / 1e18
    d['SIDE'] = d['TRADESIZE'].apply(trade_side_mapper)
    # st.dataframe(d[d['TX_HASH']=='0x22343b8d3ed60a490690f2b7b91f01d5ce1a945808a486324468d8bae7aadd08'])

    return d

def short_changer(val):
    if int(val) > 1e50:
        return int(val) - 115792089237316195423570985008687907853269984665640564039457584007913129639936
    else:
        return int(val)

st.cache()
def load_historical(df,datapath = 'data/kwenta_trades.csv'):
    d = pd.read_csv(datapath)
    d = modify_data(d)
    d = d[d['BLOCK_TIMESTAMP']<='2022-08-04']
    
    df = modify_data(df)
    d = pd.concat([d,df],axis=0)
    
    # 115792089237316195423570985008687907853269984665640564039457584007913129639936
    return d.sort_values('BLOCK_TIMESTAMP')