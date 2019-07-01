import requests as r
import datetime
import pandas as pd


def data_get(start, base, target):
    start = datetime.datetime.strptime(start, '%y-%m-%d')
    start_ = (start - datetime.timedelta(days=60)).strftime('%y-%m-%d')
    url = 'https://api.exchangeratesapi.io/history?start_at='+str(start_)+'&end_at='+str((start- datetime.timedelta(days=1)).strftime('%y-%m-%d'))+'&base='+str(base.upper())+'&symbols='+str(target.upper())
    res = r.get(url)
    d = res.json()
    df = pd.DataFrame()
    for i in sorted(d['rates']):
        df = df.append([[i,d['rates'][i]]], ignore_index=True)
    df.columns = ['Date', str('Rate(in '+target.upper()+')')]
    df.to_csv('data.csv', 'a')
    temp = pd.read_csv('data.csv')
    temp.drop_duplicates(subset='Date', inplace=True)
    temp.to_csv('data.csv')

