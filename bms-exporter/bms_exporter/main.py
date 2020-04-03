import datetime
import sys
import time

import sqlite3

import click

from prometheus_client import Gauge, start_http_server, Enum


class Metrics:
    def __init__(self, database):
        """
        (date time, ah_percent real, ah_remaining real, ah_full real, power real, voltage real, current real, temperature real, cycles numeric);
        """
        self.database = ''
        conn = sqlite3.connect(database)
        self.c = conn.cursor()
        self.last_update_gauge = Gauge('bms_last_update', 'Metrics of last update')
        self.ah_percent_gauge = Gauge('bms_ah_percent', 'Metrics of percent of capacity')
        self.ah_remaining_gauge = Gauge('bms_ah_remaining', 'Metrics of remaining capcity')
        self.ah_full_gauge = Gauge('bms_ah_full', 'Metrics of full capacity')
        self.power_gauge = Gauge('bms_power', 'Metrics of power')
        self.voltage_gauge = Gauge('bms_voltage', 'Metrics of voltage')
        self.current_gauge = Gauge('bms_current', 'Metrics of current')
        self.temperature_gauge = Gauge('bms_temperature', 'Metrics of temperature')
        self.cycles_gauge = Gauge('bms_cycles', 'Metrics of cycles')
        self.mode_enum = Enum('bms_mode', 'Metrics of mode', states=['discharging', 'charging'])
        self.time_left = Gauge('bms_time_left', 'Metrics of time to charge/discharge', ['mode'])

    def build_metrics(self):
        data = self.c.execute('select * from readings  ORDER BY date DESC LIMIT 1').fetchone()
        last_update = data[0]
        last_update = datetime.datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
        last_update = last_update.timestamp()
        self.last_update_gauge.set(last_update)
        self.ah_percent_gauge.set(data[1])
        ah_remaining_gauge = data[2]
        self.ah_remaining_gauge.set(ah_remaining_gauge)
        ah_full_gauge = data[3]
        self.ah_full_gauge.set(ah_full_gauge)
        self.power_gauge.set(data[4])
        self.voltage_gauge.set(data[5])
        self.current_gauge.set(data[6])
        self.temperature_gauge.set(data[7])
        self.cycles_gauge.set(data[8])

        if float(data[4]) >= 0:
            mode = 'charging'
        else:
            mode = 'discharging'

        self.mode_enum.state(mode)

        # Calculate mean value over 5m
        currents = []
        self.c.execute('select current from readings  ORDER BY date DESC LIMIT 30')
        for row in self.c:
            currents.append(row[0])

        mean_current = sum(currents) / len(currents)
        if mean_current == float(0):
          return
        to100 = (ah_full_gauge - ah_remaining_gauge) / mean_current
        to40 = (ah_remaining_gauge - (ah_full_gauge * 0.4)) / mean_current
        to0 = ah_remaining_gauge / mean_current
        if mode == 'discharging':
            smart = to40
        else:
            smart = to100

        self.time_left.labels(mode='smart').set(smart)
        self.time_left.labels(mode='to100').set(to100)
        self.time_left.labels(mode='to40').set(to40)
        self.time_left.labels(mode='to0').set(to0)


@click.command()
@click.option('--database', '-f', envvar='DATABASE', help='Path to sqlite db')
@click.option('--port', '-p', envvar='PORT', help='Exporter port', default=8000)
@click.option('--interval', '-i', envvar='INTERVAL', help='interval', default=5)
def main(database, port, interval):
    """
    """
    start_http_server(port)
    metrics = Metrics(database)

    while True:
        metrics.build_metrics()
        time.sleep(interval)
