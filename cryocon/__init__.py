"""cryocon expresses reading of Cryocon Model 12~18i+ monitors over HTTP."""

import requests


def raise_err(resp):
    """Raises an exception if the response status code is not 200.

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
        raise Exception(str(resp.content).strip())


class TemperatureMonitor:
    def __init__(self, addr):
        """Create a new TemperatureMonitor instance.

        Parameters
        ----------
        addr : `str`
            "root" address of the go-hcit server, one level above the
            "/read" route.  Must incude port.  startswith http not needed.

        """
        if not addr.startswith('http://'):
            addr = 'http://' + addr

        if 'https' in addr:
            addr = addr.replace('https', 'http')

        self.addr = addr

    @property
    def version(self):
        """The model name and firmware version."""
        resp = requests.get(self.addr + "/version")
        raise_err(resp)
        return str(resp.content).rstrip()

    def read(self, ch='all'):
        """Read some or all of the channels.

        Parameters
        ----------
        ch : `str`, optional
            if all, reads all channels and returns a list of floats, else returns a single float.
            Channels without monitors on them are encoded as NaN.

        Returns
        -------
        `list` of float or `float`

        """
        ch = ch.upper()
        if ch == 'ALL':
            resp = requests.get(self.addr + "/read")
            raise_err(resp)
            return resp.json()
        else:
            resp = requests.get(f'{self.addr}/read/{ch}')
            raise_err(resp)
            return resp.json()['f64']
