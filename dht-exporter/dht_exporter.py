#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import random
import time
import Adafruit_DHT
from prometheus_client import start_http_server, Gauge

# Create a metric to track time spent and requests made.
g_temperature = Gauge('dht_temperature', 'Temperature in celsius provided by dht sensor or similar', ['room'])
g_humidity = Gauge('dht_humidity', 'Humidity in percents provided by dht sensor or similar', ['room'])

def update_sensor_data(gpio_pin, room):
    """Get sensor data and sleep."""
    # get sensor data from gpio pin provided in the argument
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, gpio_pin)
    if humidity is not None and temperature is not None:
        if abs(temperature) < 100:     #If sensor returns veird value ignore it and wait for the next one 
            g_temperature.labels(room).set('{0:0.1f}'.format(temperature))
        if abs(humidity) < 100:        #If sensor returns veird value ignore it and wait for the next one 
           g_humidity.labels(room).set('{0:0.1f}'.format(humidity))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pull_time", type=int, default=5, help="Pull sensor data every X seconds.")
    parser.add_argument("-g", "--gpio", type=int, nargs='+', 
                        help="Set GPIO pin id to listen for DHT sensor data.", 
                        required=True)
    parser.add_argument("-r", "--room", type=str, nargs='+', 
                        help="Set room name.", 
                        required=True)
    cli_arguments = parser.parse_args()

    if len(cli_arguments.gpio) != len(cli_arguments.room):
        print("The number of gpio pins set needs to be the same as number of rooms set" \
              "\n Number of gpio pins: {g}\n Number of rooms: {r}".format(g=len(cli_arguments.gpio), r=len(cli_arguments.room)))
        exit(1)
    # Start up the server to expose the metrics.
    start_http_server(8001)

    # Update temperature and humidity
    while True:
        for id, gpio_pin in enumerate(cli_arguments.gpio):
            update_sensor_data(gpio_pin, cli_arguments.room[id])
        time.sleep(cli_arguments.pull_time)

