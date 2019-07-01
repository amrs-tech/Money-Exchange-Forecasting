from django.shortcuts import render
from .forms import MyForm
import requests as r
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go
import datetime


def data_get(start, base, target):
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    start_ = (start - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
    url = 'https://api.exchangeratesapi.io/history?start_at='+str(start_)+'&end_at='+str((start- datetime.timedelta(days=1)).strftime('%Y-%m-%d'))+'&base='+str(base.upper())+'&symbols='+str(target.upper())
    res = r.get(url)
    d = res.json()
    df = pd.DataFrame()
    for i in sorted(d['rates']):
        df = df.append([[i, d['rates'][i][target.upper()]]], ignore_index=True)
    df.columns = ['Date', str('Rate(in '+target.upper()+')')]
    df.to_csv('data.csv', index=False)


def predict(request, amount, wait):
    # dataset
    df = pd.read_csv('data.csv')
    # fit model
    model = ARIMA(np.asarray(df[df.columns[1]], dtype='float'), order=(3, 1, 2))
    model_fit = model.fit(disp=False)
    # make prediction
    yhat = model_fit.predict(len(df[df.columns[1]]), len(df[df.columns[1]]) + wait, typ='levels')
    # print(yhat)

    datelist = pd.date_range(pd.datetime.strptime(df['Date'][len(df['Date'])-1], '%Y-%m-%d'), periods=wait+1).tolist()
    x_date = [i.strftime('%Y-%m-%d') for i in datelist]
    fin_amt = [amount * i for i in yhat]
    graph = go.Scatter(
        x=x_date,
        y=fin_amt,
        mode='lines+markers',
        name='value'
    )

    pyo.plot([graph], filename='graph.html', auto_open=False)
    d={}
    for i in range(len(yhat)):
        d[x_date[i]] = yhat[i]

    return d


def graph(request):
    return render(request, 'graph.html')


def data(request):
    if request.method == "POST":
        m = MyForm(request.POST)
        if m.is_valid():
            start = m.cleaned_data['start']
            wait = m.cleaned_data['wait']
            amount = m.cleaned_data['amount']
            base = m.cleaned_data['base']
            target = m.cleaned_data['target']

            data_get(start, base, target)
            d = predict(request, amount, wait)
            return render(request, 'app/res.html', {'d': d})

    else:
        m = MyForm()
    return render(request, 'app/index.html', {'form': m})



