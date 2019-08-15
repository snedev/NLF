import csv, time, datetime, os
import pandas as pd

from sys import argv  # Specify the .csv file to be used for conversion

script, filename = argv


# Open the original .csv file and convert the date into a timestamp

with open(filename, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('formatted.csv', 'w') as new_file:
        fieldnames = ['Date', 'Symbol', 'Price']

        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        csv_writer.writeheader()  # Write the headers for the columns in the new .csv file

        for line in csv_reader:
            d = line['Date']
            date_formatted = time.mktime(datetime.datetime.strptime(d, "%Y-%m-%d %I-%p").timetuple())
            line['Date'] = int(date_formatted)
            print(line['Date'])
            csv_writer.writerow(line)

# Take the new csv file and create a line protocol .txt file for importing into influxDB

file = pd.read_csv("formatted.csv")
lines = [str(file["Symbol"][d])
         + " " + "Price=" + str(file["Price"][d])
         + " " + str(file["Date"][d]) for d in range(len(file))]
output = open('import.txt', 'w')
output.write("""# DDL
CREATE DATABASE NLF

# DML
# CONTEXT-DATABASE: NLF

""")
for item in lines:
    output.write("%s\n" % item)


os.remove("formatted.csv")  # Delete the temp .csv file
