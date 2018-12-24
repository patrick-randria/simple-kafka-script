#! /usr/bin/env python3
"""This is the consumer script"""

import json
from kafka import KafkaConsumer

empty_stations_per_city = {}

consumer = KafkaConsumer("empty-stations", bootstrap_servers='localhost:9092',
                         group_id="velib-monitor-stations")
for message in consumer:
    station = json.loads(message.value.decode())
    station_id = station["key"]
    station_name = station["name"]
    station_address = station["address"]
    current_available = int(station["available_bikes"])
    station_city = station["city"]

    if station_city not in empty_stations_per_city:
        empty_stations_per_city[station_city] = 1 if current_available == 0 else 0

    if current_available == 0:
        empty_stations_per_city[station_city] += 1
        print("- address=({address}) - city=({city}) become empty. "
              " empty station(s) = {nb} ".format(address=station_address,
                                                 city=station_city,
                                                 nb=empty_stations_per_city[station_city]))
        print('')
    else:
        empty_stations_per_city[station_city] -= 1
