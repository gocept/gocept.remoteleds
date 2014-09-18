#!/usr/bin/python
# coding: utf-8

import serial
import serial.tools.list_ports
import time


SNR = "7523233343535130C120"
BAUD = 9600
SCAN_DELAY_IN_S = 1


def main():
    dev = None
    while dev is None:
        dev = discover()
        time.sleep(SCAN_DELAY_IN_S)

    print dev
    if dev is not None:
        try:
            ser = serial.Serial(dev, BAUD)
            time.sleep(5)
            for y in range(0, 256):
                for i in range(0, 14):
                    if i - 1 > 0:
                        ser.write("LED%02d%03d%03d000\n" % (i - 1, 0, 0))
                    ser.write("LED%02d%03d%03d000\n" % (i, y, y))
            ser.flushInput()
            ser.close()
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
