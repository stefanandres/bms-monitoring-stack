import sys
import time

import sqlite3

import click

from prometheus_client import Gauge, start_http_server


class Metrics:
    def __init__(self, database):
        """
        (date time, ah_percent real, ah_remaining real, ah_full real, power real, voltage real, current real, temperature real, cycles numeric);
        """
        self.database = ''
        conn = sqlite3.connect(database)
        self.c = conn.cursor()
        self.ah_percent_gauge = Gauge('bms_ah_percent', 'Metrics of percent of capacity')
        self.ah_remaining_gauge = Gauge('bms_ah_remaining', 'Metrics of remaining capcity')
        self.ah_full_gauge = Gauge('bms_ah_full', 'Metrics of full capacity')
        self.power_gauge = Gauge('bms_power', 'Metrics of power')
        self.voltage_gauge = Gauge('bms_voltage', 'Metrics of voltage')
        self.current_gauge = Gauge('bms_current', 'Metrics of current')
        self.temperature_gauge = Gauge('bms_temperature', 'Metrics of temperature')
        self.cycles_gauge = Gauge('bms_cycles', 'Metrics of cycles')

    def build_metrics(self):
        data = self.c.execute('select * from readings  ORDER BY date DESC LIMIT 1').fetchone()
        ah_percent = data[1]
        ah_remaining = data[2]
        ah_full = data[3]
        power = data[4]
        voltage = data[5]
        current = data[6]
        temperature = data[7]
        cycles = data[8]
        self.ah_percent_gauge.set(ah_percent)
        self.ah_remaining_gauge.set(ah_remaining)
        self.ah_full_gauge.set(ah_remaining)
        self.power_gauge.set(power)
        self.current_gauge.set(current)
        self.voltage_gauge.set(voltage)
        self.temperature_gauge.set(temperature)
        self.cycles_gauge.set(cycles)

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
