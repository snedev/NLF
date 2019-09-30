import pandas as pd

from influxdb import DataFrameClient
from sys import argv


script, filename = argv

df = pd.read_pickle(filename)

client = DataFrameClient('localhost', port=8086, username='root', password='root', database='NLF2')

client.write_points(df, measurement='CHFSEK', time_precision='s', database='NLF2', protocol='line')

print("DataFrame imported")
