#! /usr/bin/env python3
import json
import time
import urllib.request

# Run `pip install kafka-python` to install this package
from kafka import KafkaProducer

API_KEY = "your_api" # FIXME
url = "https://api.jcdecaux.com/vls/v1/stations?apiKey={}".format(API_KEY)

producer = KafkaProducer(bootstrap_servers="localhost:9092")
available_bikes = {}
i=0
while True:
    response = urllib.request.urlopen(url)
    stations = json.loads(response.read().decode())
    for station in stations:
        current_available = station['available_bikes']
        key = "{}-{}-{}".format(station["number"], station["name"], station["contract_name"])

        if key not in available_bikes:
            available_bikes[key] = current_available

        # Si devient vide ou n'est plus vide
        if ( current_available == 0 and available_bikes[key] > 0 ) or \
           ( current_available > 0 and available_bikes[key] == 0):
            payload = {'key': key,
                       'name': station["name"],
                       'address': station['address'],
                       'available_bikes': current_available,
                       'city': station['contract_name']
                      }
            producer.send("empty-stations",
                          json.dumps(payload).encode(),
                          key=str(key).encode())
            print('iteration={} name=({}) address=({}) city=({}) before={} now={}'.format(i, station["name"], station["address"],
                                                                                          station["contract_name"], available_bikes[key],
                                                                                          current_available))
            print()
        available_bikes[key] = current_available

    time.sleep(1)
    i += 1
