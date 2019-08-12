import json, time, datetime
from django.views.generic import TemplateView
from django.shortcuts import redirect
from influxdb import InfluxDBClient
from django.http import JsonResponse
import plotly.express as px
import pandas as pd


def influxdb_client():  # An instance of the InfluxDBClient that gets data from InfluxDB
    client = InfluxDBClient(host='127.0.0.1', port=8086, username='root', password='root', database='NLF')
    return client


class HomeView(TemplateView):
    template_name = 'index.html'


def select_currency(request):
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
            fig.show()
            return JsonResponse(json_query, safe=False)
        if currency == 'ETHUSD':
            query = influxdb_client().query(
                ('select Price from ETHUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            fig.show()
            return JsonResponse(json_query, safe=False)
        if currency == 'LTCUSD':
            query = influxdb_client().query(
                ('select Price from LTCUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            fig.show()
            return JsonResponse(json_query, safe=False)
        if currency == 'XRPUSD':
            query = influxdb_client().query(
                ('select Price from XRPUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            fig.show()
            return JsonResponse(json_query, safe=False)
        if currency == 'XMRUSD':
            query = influxdb_client().query(
                ('select Price from XMRUSD where time > {} AND time <= {}').format(date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])
            fig = px.line(df, x='Date', y='Price')
            fig.show()
            return JsonResponse(json_query, safe=False)
    else:
        return redirect('/')