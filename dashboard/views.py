import json
from django.views.generic import TemplateView
from django.shortcuts import redirect
from influxdb import InfluxDBClient
from django.http import JsonResponse


def influxdb_client():  # An instance of the InfluxDBClient that gets data from InfluxDB
    client = InfluxDBClient(host='127.0.0.1', port=8086, username='root', password='root', database='NLF')
    return client


class HomeView(TemplateView):
    template_name = 'index.html'


def select_currency(request):
    if request.method == 'POST':
        currency = request.POST.get('Pairs')
        if currency == 'BTCUSD':
            query = influxdb_client().query('select time, Price from BTCUSD')
            json_query = json.dumps(query.raw)
            return JsonResponse(json_query, safe=False)
        if currency == 'ETHUSD':
            query = influxdb_client().query('select time, Price from ETHUSD')
            json_query = json.dumps(query.raw)
            return JsonResponse(json_query, safe=False)
        if currency == 'LTCUSD':
            query = influxdb_client().query('select time, Price from LTCUSD')
            json_query = json.dumps(query.raw)
            return JsonResponse(json_query, safe=False)
        if currency == 'XRPUSD':
            query = influxdb_client().query('select time, Price from XRPUSD')
            json_query = json.dumps(query.raw)
            return JsonResponse(json_query, safe=False)
        if currency == 'XMRUSD':
            query = influxdb_client().query('select time, Price from XMRUSD')
            json_query = json.dumps(query.raw)
            return JsonResponse(json_query, safe=False)
    else:
        return redirect('/')

