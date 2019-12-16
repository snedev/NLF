import time, datetime
import pandas as pd
import json

from django.shortcuts import redirect, render
from influxdb import InfluxDBClient
from django.http import JsonResponse
from snips_nlu import SnipsNLUEngine

from NLF import settings


def influxdb_client():  # An instance of the InfluxDBClient that gets data from InfluxDB
    client = InfluxDBClient(
        settings.INFLUXDB_HOST,
        settings.INFLUXDB_PORT,
        settings.INFLUXDB_USERNAME,
        settings.INFLUXDB_PASSWORD,
        settings.INFLUXDB_DATABASE,
        settings.INFLUXDB_HTTP_MAX_ROW_LIMIT
    )
    return client


def index(request):
    cpairs = {'Bitcoin': 'BTCUSD',
              'Ethereum': 'ETHUSD',
              'Litecoin': 'LTCUSD',
              'Ripple': 'XRPUSD',
              'Monero': 'XMRUSD'
              }
    context = {
        'data_selector': get_data,
        'cpairs': cpairs
    }
    return render(request, 'index.html', context=context)


def create_plot(currency_pairs, date_from, date_to):
    dataframes = []
    for currency in currency_pairs:
        q = ('select Price from {} where time > {} AND time <= {}').format(currency, date_from, date_to)
        query = influxdb_client().query(q, chunked=True, chunk_size=1000)
        query = list(query.get_points(measurement=currency))
        df = pd.DataFrame(query).set_index('time')
        df = df.rename(columns={'Price': currency})
        dataframes.append(df)
    df2 = pd.DataFrame(query, columns=['time']).set_index('time')
    df_joined = pd.DataFrame.join(df2, dataframes, how='inner')
    instruments = {'time': df_joined.index.tolist()}
    for i in currency_pairs:
        instruments[i] = df_joined[i].tolist()
    return JsonResponse(instruments, safe=False)


def create_plot_with_indicator(currency_pairs, date_from, date_to, data_analysis):
    dataframes = []
    for currency in currency_pairs:
        q = ('select Price from {} where time > {} AND time <= {}').format(currency, date_from, date_to)
        query = influxdb_client().query(q, chunked=True, chunk_size=1000)
        query = list(query.get_points(measurement=currency))
        df = pd.DataFrame(query).set_index('time')
        df = df.rename(columns={'Price': currency})
        dataframes.append(df)
    df2 = pd.DataFrame(query, columns=['time']).set_index('time')
    df_joined = pd.DataFrame.join(df2, dataframes, how='inner')
    instruments = {'time': df_joined.index.tolist()}
    for i in currency_pairs:
        instruments[i] = df_joined[i].tolist()
    if data_analysis == 'MA21' or data_analysis == 'ma21':
        df_joined['MA21'] = df_joined.rolling(min_periods=1, window=21).mean()
        instruments.update({'MA21': df_joined['MA21'].tolist()})
        return JsonResponse(instruments, safe=False)
    elif data_analysis == 'MA100' or data_analysis == 'ma100':
        df_joined['MA100'] = df_joined.rolling(min_periods=1, window=100).mean()
        instruments.update({'MA100': df_joined['MA100'].tolist()})
        return JsonResponse(instruments, safe=False)
    elif data_analysis == 'MACD' or data_analysis == 'macd':
        for i in currency_pairs:
            df_joined['26EMA'] = df_joined[i].rolling(min_periods=1, window=26).mean()
            df_joined['12EMA'] = df_joined[i].rolling(min_periods=1, window=12).mean()
            df_joined['MACD'] = df_joined['12EMA'] - df_joined['26EMA']
            instruments.update({'MACD': df_joined['MACD'].tolist()})
            return JsonResponse(instruments, safe=False)
    else:
        return JsonResponse(instruments, safe=False)


def get_data(request):
    if request.method == 'POST':
        currency_pairs = request.POST.getlist('currency_pairs')
        date_from_unformatted = request.POST.get('date_from')
        date_from = str(int(time.mktime(datetime.datetime.strptime(date_from_unformatted, "%Y-%m-%dT%H:%M").timetuple()))) + "000000000"
        date_to_unformatted = request.POST.get('date_to')
        date_to = str(int(time.mktime(datetime.datetime.strptime(date_to_unformatted, "%Y-%m-%dT%H:%M").timetuple()))) + "000000000"
        data_analysis = request.POST.get('data_analysis')
        if request.POST.get('data_analysis') is not None:
            return create_plot_with_indicator(currency_pairs, date_from, date_to, data_analysis)
        else:
            return create_plot(currency_pairs, date_from, date_to)


def get_nlu(request):
    if request.method == 'POST':
        nlu_selector = request.POST.get('nlu_text')
        nlu_engine = SnipsNLUEngine.from_path("./dashboard/trained_engine")
        parsing = nlu_engine.parse(nlu_selector)
        if parsing['intent']['intentName'] == 'createPlot':
            currency_pairs = [parsing['slots'][0]['value']['value']]
            date_from_unformatted = parsing['slots'][1]['value']['value']
            date_from = str(int(time.mktime(
                datetime.datetime.strptime(date_from_unformatted[:16], "%Y-%m-%d %H:%M").timetuple()))) + "000000000"
            date_to_unformatted = parsing['slots'][2]['value']['value']
            date_to = str(int(time.mktime(
                datetime.datetime.strptime(date_to_unformatted[:16], "%Y-%m-%d %H:%M").timetuple()))) + "000000000"
            return create_plot(currency_pairs, date_from, date_to)
        elif parsing['intent']['intentName'] == 'createPlotwithIndicator':
            currency_pairs = [parsing['slots'][0]['value']['value']]
            date_from_unformatted = parsing['slots'][1]['value']['value']
            date_from = str(int(time.mktime(
                datetime.datetime.strptime(date_from_unformatted[:16], "%Y-%m-%d %H:%M").timetuple()))) + "000000000"
            date_to_unformatted = parsing['slots'][2]['value']['value']
            date_to = str(int(time.mktime(
                datetime.datetime.strptime(date_to_unformatted[:16], "%Y-%m-%d %H:%M").timetuple()))) + "000000000"
            data_analysis = parsing['slots'][3]['value']['value']
            return create_plot_with_indicator(currency_pairs, date_from, date_to, data_analysis)
        elif parsing['intent']['intentName'] == 'addIndicator':
            data_analysis = parsing['slots'][0]['entity']
            data = request.POST.get('plot_data')
            data = json.loads(data)
            date_from_unformatted = data[0]['time'][0]
            date_from = str(int(time.mktime(
                datetime.datetime.strptime(date_from_unformatted, "%Y-%m-%dT%H:%M:%SZ").timetuple()))) + "000000000"
            date_to_unformatted = data[0]['time'][-1]
            date_to = str(int(time.mktime(
                datetime.datetime.strptime(date_to_unformatted, "%Y-%m-%dT%H:%M:%SZ").timetuple()))) + "000000000"
            currency_pairs = []
            for key, value in data:
                currency_pairs.append(value)
            return create_plot_with_indicator(currency_pairs, date_from, date_to, data_analysis)
