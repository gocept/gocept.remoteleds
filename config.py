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
USER = "user"
PASSWORD = "password"
JENKINS = "jenkins"


class Config(object):
    """docstring for Config"""
    def __init__(self, SNR, led_count, clients):
        super(Config, self).__init__()
        self.SNR = SNR
        self.led_count = led_count
        self.clients = clients

    @staticmethod
    def load_config(connection, path='config.ini'):
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

        clients = []
        for client_name in client_names:
            typ = config.get(client_name, TYPE)
            user = None
            password = None
            if (config.has_option(client_name, USER)
                    and config.has_option(client_name, PASSWORD)):
                user = config.get(client_name, USER)
                password = config.get(client_name, PASSWORD)
            baseurl = config.get(client_name, BASEURL)
            projects = []
            for led_nr in led_numbers:
                led_name = "led{}".format(led_nr)
                if config.has_option(client_name, led_name):
                    project = config.get(client_name, led_name)
                    projects.append(client.Project(name=project, led=led_nr))
            if typ == JENKINS:
                clients.append(client.JenkinsClient(connection, baseurl, projects, user, password))
        return Config(snr, led_count, clients)

    def __str__(self):
        return "Config(SNR={},led_count={},clients={})".format(self.SNR, self.led_count, self.clients)


if __name__ == '__main__':
    config = Config.load_config(CONFIG_FILE)
    print config
