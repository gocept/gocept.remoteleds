import requests


class Client(object):

    def __init__(self, connection, baseurl, projects, user=None, passwd=None):
        self.connection = connection
        self.baseurl = baseurl
        self.projects = projects
        self.user = user
        self.passwd = passwd

    def get_state_for_project(self, project):
        """Implement in concrete client."""
        raise NotImplementedError()

    def get_color_for_state(self, state):
        """Implement in concrete client."""
        raise NotImplementedError()

    def update(self):
        for project, led_number in self.projects.items():
            state = self.get_state_for_project(project)
            print("{}: {} (LED {})".format(project, state, led_number))
            self.send(self.connection, led_number, state)

    def send(self, connection, led_number, state):
        red, green, blue = self.get_color_for_state(state)
        message = "LED%02d%03d%03d%03d\n" % (led_number, red, green, blue)
        connection.write(message)
        connection.flushInput()


class JenkinsClient(Client):

    def get_state_for_project(self, project):
        url = "{}/job/{}/api/json".format(self.baseurl, project)
        if self.user and self.passwd:
            response = requests.get(url, auth=(self.user, self.passwd))
        else:
            response = requests.get(url)
        return response.json()['color']

    def get_color_for_state(self, state):
        if 'red' in state:
            return 128, 0, 0
        elif 'blue' in state:
            return 0, 128, 0
        elif 'yellow' in state:
            return 128, 128, 0
        else:
            return 0, 0, 128
