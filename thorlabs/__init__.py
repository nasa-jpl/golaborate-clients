"""Thorlabs provides HTTP clients for Thorlabs hardware enabled by go-hcit."""
import requests

try:
    from astropy import units as u
except ImportError:
    pass


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


class ITC4000:
    """ITC4000 represents an ITC4000 laser diode / TEC controller."""

    def __init__(self, addr, convention='float'):
        """Create a new ITC4000 instance.

        Parameters
        ----------
        addr : `str`
            a network address, with port added.  "host:port".
            HTTP prefix not needed.
        convention : `str`, {'float', 'units'}
            if float, uses floats for current and temperature.
            Else uses astropy quantities.

        """
        if not addr.startswith('http://'):
            addr = 'http://' + addr

        if 'https' in addr:
            addr = addr.replace('https', 'http')

        self.addr = addr
        self.convention = convention

    def current(self, value=None):
        """Get or set the current setpoint.

        Parameters
        ----------
        value : `float` or `astropy.units.Quantity`
            current.  If float, units of mA.

        Returns
        -------
        `float`
            value in mA
        `astropy.units.Quantity`
            value

        """
        url = f'{self.addr}/current'
        if value is None:
            resp = requests.get(url)
            raise_err(resp)
            val = resp.json()['f64']
            if self.convention == 'float':
                return val
            else:
                return u.mA * val

        if isinstance(value, u.Quantity):
            value = value.to(u.mA)
            payload = {'f64': value}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    def emission(self, value=None):
        """Get or set the emission status.

        Parameters
        ----------
        value : `bool`
            if True, turns emission off.  If false, turns emission off.  Gets on None.

        Returns
        -------
        `bool`
            emission state (true=on)

        """
        url = f'{self.addr}/emission'
        if value is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            payload = {'bool': value}
            resp = requests.post(url, json=payload)
            raise_err(resp)
