"""thermocube provides tools for accessing thermocube chillers thanks to a go-hcit middleman."""
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
        if not addr.startswith('http://'):
            addr = 'http://' + addr

        if 'https' in addr:
            addr = addr.replace('https', 'http')

        self.addr = addr

    @property
    def temperature(self):
        """Temperature at the output of the cube."""
        resp = requests.get(f'{self.addr}/temperature')
        raise_err(resp)
        return resp.json()['f64']

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
        url = f'{self.addr}/setpoint'
        if celcius is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']
        else:
            payload = {'f64': float(celcius)}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @property
    def faults(self):
        resp = requests.get(f'{self.addr}/temperature')
        raise_err(resp)
        return resp.json()

    @property
    def tank_level_low(self):
        return self.faults['tankLevelLow']
