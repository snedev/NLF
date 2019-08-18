import json, time, datetime
import pandas as pd

from django.shortcuts import redirect, render
from influxdb import InfluxDBClient
from django.http import JsonResponse

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


def get_data(request):
    if request.method == 'POST':
        currency = request.POST.get('currency_pairs')
        date_from_unformatted = request.POST.get('date_from')
        date_from = str(int(time.mktime(datetime.datetime.strptime(date_from_unformatted, "%Y-%m-%dT%H:%M").timetuple()))) + "000000000"
        date_to_unformatted = request.POST.get('date_to')
        date_to = str(int(time.mktime(datetime.datetime.strptime(date_to_unformatted, "%Y-%m-%dT%H:%M").timetuple()))) + "000000000"

        if currency == currency:
            query = influxdb_client().query(
                ('select Price from {} where time > {} AND time <= {}').format(currency, date_from, date_to))
            json_query = json.dumps(query.raw)
            df = pd.read_json(json_query)  # Pandas read_json function to read the json data
            df = df['series'][0]['values']
            df = pd.DataFrame(df, columns=['Date', 'Price'])  # Create Pandas dataframe to be used by Plotly
            Date = df['Date'].tolist()
            Price = df['Price'].tolist()
            return JsonResponse({'Date': Date, 'Price': Price}, safe=False)
    else:
        return redirect('home')
