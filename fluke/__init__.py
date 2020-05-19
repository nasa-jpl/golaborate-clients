"""Fluke provides tools for accessing Fluke hardware thanks to a go-hcit middleman."""
import requests


def raise_err(resp):
    """Raise an exception if the response status code is not 200.

    Parameters
    ----------
    resp : `requests.Response`
        a response with a status code

    Raises
    ------
    Exception
    any errors encountered, whether they are in communciation with the
    server or between the server and the camera/SDK

    """
    if resp.status_code != 200:
        raise Exception(resp.content.decode('UTF-8').rstrip())


class DewK:
    """DewK is a class exposing access to DewK temp/humidity meters."""

    def __init__(self, addr):
        """Create a new ITC4000 instance.

        Parameters
        ----------
        addr : `str`
            a network address, with port added.  "host:port".
            HTTP prefix not needed.

        """
        if not addr.startswith('http://'):
            addr = 'http://' + addr

        if 'https' in addr:
            addr = addr.replace('https', 'http')

        self.addr = addr

    @property
    def reading(self):
        """Instantaneous Temp/Humidity reading."""
        url = f'{self.addr}/read'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()
