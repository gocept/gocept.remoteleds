import gocept.remoteleds.client
import mock


def test_client_update_calls_sendstate():
    project = gocept.remoteleds.client.Project('backy', 0)
    client = gocept.remoteleds.client.JenkinsClient(
        None, 'https://builds.gocept.com', [project])
    with mock.patch('gocept.remoteleds.client.Client.send_state') as method:
        client.update()
        method.assert_called_once_with(None, project)
