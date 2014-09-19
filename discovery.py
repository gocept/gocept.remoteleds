#!/usr/bin/python
# coding: utf-8

import serial
import serial.tools.list_ports
import time
import client
import config


BAUD = 9600
SCAN_DELAY_IN_S = 1


def main():
    cfg = config.Config()
    cfg.load()

    dev = discover_loop(cfg.serial_number)

    if dev is not None:
        try:
            connection = serial.Serial(dev, BAUD)

            print("Waiting for Handshake")
            while (connection.readline().strip() != 'PING'):
                time.sleep(0.1)

            print("Answer Handshake")
            connection.write("14")
            connection.flushInput()

            while ("READY" not in connection.readline()):
                time.sleep(0.1)
            print("Connection ready")

            clients = []
            for client_cfg in cfg.clients:
                if config.JENKINS in client_cfg['type']:
                    clients.append(client.JenkinsClient(
                        connection=connection, baseurl=client_cfg['baseurl'],
                        user=client_cfg['user'], passwd=client_cfg['password'],
                        projects=client_cfg['projects']))

            while True:
                for cli in clients:
                    print("Update {}".format(cli.__class__.__name__))
                    cli.update()
                time.sleep(5)
            connection.close()
        except serial.serialutil.SerialException as e:
            print(e)


def discover_loop(snr):
    dev = None
    while dev is None:
        dev = discover(snr)
        time.sleep(SCAN_DELAY_IN_S)
    return dev

def discover(serial_number):
    comports = list(serial.tools.list_ports.comports())
    for port in comports:
        if "SNR={}".format(serial_number) in port[2]:
            return port[0]
    return None


if __name__ == '__main__':
    main()
