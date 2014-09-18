import requests


def send(connection, led_number, red, green, blue):
    message = "LED%02d%03d%03d%03d\n" % (led_number, red, green, blue)
    connection.write(message)
    connection.flushInput()


class Client(object):

    def __init__(self, connection, baseurl, projects, user=None, passwd=None):
        self.connection = connection
        self.baseurl = baseurl
        self.projects = projects
        self.user = user
        self.passwd = passwd

    def get_color_for_project(self, project):
        """Implement in concrete client."""
        raise NotImplementedError()

    def update(self):
        for project, led_number in self.projects.items():
            red, green, blue = self.get_color_for_project(project)
            print("{}: {} {} {} (LED {})".format(
                project, red, green, blue, led_number))
            send(self.connection, led_number, red, green, blue)


class JenkinsClient(Client):

    def get_color_for_project(self, project):
        url = "{}/job/{}/api/json".format(self.baseurl, project)
        if self.user and self.passwd:
            response = requests.get(url, auth=(self.user, self.passwd))
        else:
            response = requests.get(url)
        result = response.json()['color']

        if 'red' in result:
            return 128, 0, 0
        elif 'blue' in result:
            return 0, 128, 0
        elif 'yellow' in result:
            return 128, 128, 0
        else:
            return 0, 0, 128
