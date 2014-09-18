#!/usr/bin/python
# coding: utf-8


import ConfigParser
import client


CONFIG_FILE = "example.ini"
CONFIG = "config"
SNR = "SNR"
LEDCOUNT = "ledcount"
BASEURL = "baseurl"
TYPE = "type"
JENKINS = "jenkins"


class Config(object):
    """docstring for Config"""
    def __init__(self, SNR, led_count, clients):
        super(Config, self).__init__()
        self.SNR = SNR
        self.led_count = led_count
        self.clients = clients

    @staticmethod
    def load_config(path, connection=None):
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        sections = config.sections()
        client_names = [s for s in sections if s != CONFIG]
        print "Sections: %s" % sections
        print "Clients:  %s" % client_names
        snr = config.get(CONFIG, SNR)
        led_count = int(config.get(CONFIG, LEDCOUNT))
        print "SNR: %s, led_count: %s" % (snr, led_count)

        led_numbers = range(0, led_count)

        clients = list()
        for client_name in client_names:
            typ = config.get(client_name, TYPE)
            baseurl = config.get(client_name, BASEURL)
            projects = dict()
            for led_nr in led_numbers:
                try:
                    project = config.get(client_name, "led{}".format(led_nr))
                    projects[project] = led_nr
                except ConfigParser.NoOptionError as e:
                    pass
            if typ == JENKINS:
                clients.append(client.JenkinsClient(connection, baseurl, projects))
            else:
                clients.append(client.Client(connection, baseurl, projects))
        return Config(snr, led_count, clients)

    def __str__(self):
        return "Config(SNR={},led_count={},clients={})".format(self.SNR, self.led_count, self.clients)


if __name__ == '__main__':
    config = Config.load_config(CONFIG_FILE)
    print config
