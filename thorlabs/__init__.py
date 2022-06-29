"""Thorlabs provides HTTP clients for Thorlabs hardware enabled by go-hcit."""
import requests

try:
    from astropy import units as u
except ImportError:
    pass

from golab_common.retry import retry

from golab_common import raise_err, niceaddr


class ITC4000:
    """ITC4000 represents an ITC4000 laser diode / TEC controller."""

    def __init__(self, addr, convention='float'):
        """Create a new ITC4000 instance.

        Parameters
        ----------
        addr : str
            a network address, with port added.  "host:port".
            HTTP prefix not needed.
        convention : str, {'float', 'units'}
            if float, uses floats for current and temperature.
            Else uses astropy quantities.

        """
        self.addr = niceaddr(addr)
        self.convention = convention

    @retry(max_retries=2, interval=1)
    def current(self, value=None):
        """Get or set the current setpoint.

        Parameters
        ----------
        value : float or astropy.units.Quantity
            current.  If float, units of mA.

        Returns
        -------
        float
            value in mA
        astropy.units.Quantity
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
            value = float(value.to(u.mA))
        else:
            value = float(value)

        payload = {'f64': value}
        resp = requests.post(url, json=payload)
        raise_err(resp)

    @retry(max_retries=2, interval=1)
    def emission(self, value=None):
        """Get or set the emission status.

        Parameters
        ----------
        value : bool
            if True, turns emission off.  If false, turns emission off.  Gets on None.

        Returns
        -------
        bool
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
