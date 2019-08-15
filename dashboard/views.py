import plotly
import json, time, datetime
import plotly.express as px
import pandas as pd

from django.shortcuts import redirect, render
from influxdb import InfluxDBClient
from django.http import HttpResponseRedirect

from NLF import settings


def influxdb_client():  # An instance of the InfluxDBClient that gets data from InfluxDB
    client = InfluxDBClient(
        settings.INFLUXDB_HOST,
        settings.INFLUXDB_PORT,
        settings.INFLUXDB_USERNAME,
        settings.INFLUXDB_PASSWORD,
        settings.INFLUXDB_DATABASE
    )
    return client


def index(request):
    context = {
        'data_selector': get_data
    }
    return render(request, 'index.html', context=context)


def get_data(request):
    if request.method == 'POST':
        currency = request.POST.get('Pairs')
        date_from_unformatted = request.POST.get('date_from')
        date_from = time.mktime(datetime.datetime.strptime(date_from_unformatted, "%Y-%m-%dT%H:%M").timetuple())
        date_from = int(date_from)
        date_from = str(date_from) + "000000000"
        date_to_unformatted = request.POST.get('date_to')
        date_to = time.mktime(datetime.datetime.strptime(date_to_unformatted, "%Y-%m-%dT%H:%M").timetuple())
        date_to = int(date_to)
        date_to = str(date_to) + "000000000"

        if currency == 'BTCUSD':
            query = influxdb_client().query(
                ('select Price from BTCUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)  # Pandas read_json function to read the json data
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])  # Create Pandas dataframe to be used by Plotly
            fig = px.line(df, x='Date', y='Price')
            plotly.offline.plot(fig, filename='dashboard/templates/plot.html', auto_open=False)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if currency == 'ETHUSD':
            query = influxdb_client().query(
                ('select Price from ETHUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            plotly.offline.plot(fig, filename='dashboard/templates/plot.html', auto_open=False)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if currency == 'LTCUSD':
            query = influxdb_client().query(
                ('select Price from LTCUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            plotly.offline.plot(fig, filename='dashboard/templates/plot.html', auto_open=False)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if currency == 'XRPUSD':
            query = influxdb_client().query(
                ('select Price from XRPUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            plotly.offline.plot(fig, filename='dashboard/templates/plot.html', auto_open=False)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if currency == 'XMRUSD':
            query = influxdb_client().query(
                ('select Price from XMRUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            plotly.offline.plot(fig, filename='dashboard/templates/plot.html', auto_open=False)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')
