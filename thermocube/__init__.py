"""thermocube provides tools for accessing thermocube chillers thanks to a go-hcit middleman."""
import requests

from golab_common.retry import retry

from golab_common import raise_err, niceaddr


class Chiller:
    """Chiller is a class enabling access to thermocube chillers."""

    def __init__(self, addr):
        """Create a new Chiller instance.

        Parameters
        ----------
        addr : `str`
            a network address, with port added.  "host:port".
            HTTP prefix not needed.

        """
        self.addr = niceaddr(addr)

    @property
    @retry(max_retries=2, interval=1)
    def temperature(self):
        """Temperature at the output of the cube."""
        resp = requests.get(f'{self.addr}/temperature')
        raise_err(resp)
        return resp.json()['f64']

    @retry(max_retries=2, interval=1)
    def temperature_setpoint(self, celcius=None):
        """Get (celcius=None) or set (celcius != None) the temperature setpoint.

        Parameters
        ----------
        celcius : `float`, optional
            temperature, in degrees celcius to set the setpoint to.  Gets if None.

        Returns
        -------
        `float`
            the current setpoint in degrees celcius

        """
        url = f'{self.addr}/temperature-setpoint'
        if celcius is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']
        else:
            payload = {'f64': float(celcius)}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @property
    @retry(max_retries=2, interval=1)
    def faults(self):
        """Faults displayed by the thermocube."""
        resp = requests.get(f'{self.addr}/faults')
        raise_err(resp)
        return resp.json()

    # no need to decorate this since the inner function is decorated
    @property
    def tank_level_low(self):
        """If True, the tank needs to be refilled."""
        return self.faults['tankLevelLow']
