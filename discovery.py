#!/usr/bin/python
# coding: utf-8

import serial
import serial.tools.list_ports
import time
import client
import config


SNR = "7523233343535130C120"
BAUD = 9600
SCAN_DELAY_IN_S = 1


def main():
    dev = None
    while dev is None:
        dev = discover()
        time.sleep(SCAN_DELAY_IN_S)

    if dev is not None:
        try:
            connection = serial.Serial(dev, BAUD)

            print("Waiting for Handshake")
            while (connection.readline().strip() != 'PING'):
                time.sleep(0.1)

            print("Answer Handshake")
            connection.write("1\n")
            connection.flushInput()

            while ("READY" not in connection.readline()):
                time.sleep(0.1)
            print("Connection ready")

            cfg = config.Config.load_config(connection)
            clients = cfg.clients

            while True:
                for cli in clients:
                    print("Update {}".format(cli.__class__.__name__))
                    cli.update()
                time.sleep(5)
            connection.close()
        except serial.serialutil.SerialException as e:
            print(e)


def discover():
    comports = list(serial.tools.list_ports.comports())
    for port in comports:
        if "SNR={}".format(SNR) in port[2]:
            return port[0]
    return None


if __name__ == '__main__':
    main()
