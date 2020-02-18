"""motion enables nice control of motion controllers (and stages) over HTTP via a go-hcit server."""

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


def _niceaddr(addr):
    if not addr.startswith('http://'):
        addr = 'http://' + addr

    if 'https' in addr:
        addr = addr.replace('https', 'http')

    return addr


class Axis:
    """Axis represents an axis of a stage."""

    def __init__(self, addr, name):
        """Create a new Axis instance.

        Parameters
        ----------
        addr : `str`
            "root" address of the go-hcit motion server.
        name : `str`
            name of the axis, as the controller knows it

        """
        self.addr = _niceaddr(addr)
        self.name = name

    def home(self):
        """Home the axis."""
        url = f'{self.addr}/axis/{self.name}/home'
        resp = requests.post(url)
        raise_err(resp)

    def enable(self):
        """Enable the axis."""
        url = f'{self.addr}/axis/{self.name}/enabled'
        payload = {'bool': True}
        resp = requests.post(url, json=payload)
        raise_err(resp)

    def disable(self):
        """Disable the axis."""
        url = f'{self.addr}/axis/{self.name}/enabled'
        payload = {'bool': False}
        resp = requests.post(url, json=payload)
        raise_err(resp)

    def initialize(self):
        """Initialize the axis."""
        url = f'{self.addr}/axis/{self.name}/initialize'
        resp = requests.post(url)
        raise_err(resp)

    @property
    def enabled(self):
        """Boolean for if the axis is enabled."""
        url = f'{self.addr}/axis/{self.name}/enabled'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['bool']

    @property
    def pos(self):
        """Position of the axis."""
        url = f'{self.addr}/axis/{self.name}/pos'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['f64']

    @property
    def limits(self):
        """Limits of the axis."""
        resp = requests.get(f'{self.addr}/axis/{self.name}/limits')
        raise_err(resp)
        return resp.json()

    def velocity(self, value=None):
        """Velocity setpoint of the axis.

        Parameters
        ----------
        value: `float`
            velocity of the axis, in mm/s

        Returns
        -------
        `float`
            velocity, if value=None

        """
        url = f'{self.addr}/axis/{self.name}/velocity'
        if value is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']
        else:
            payload = {'f64': value}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @property
    def limits(self):
        """Server/software imposed travel limits."""
        resp = requests.get(f'{self.addr}/axis/{self.name}/limits')
        return resp.json()

    def move_abs(self, pos):
        """Move the axis to an absolute position.

        Parameters
        ----------
        pos : `float`
            position to move to

        """
        url = f'{self.addr}/axis/{self.name}/pos'
        payload = {'f64': float(pos)}
        resp = requests.post(url, json=payload)
        raise_err(resp)

    def move_rel(self, pos):
        """Move the axis by a relative amount.

        Parameters
        ----------
        pos : `float`
            amount to move by

        """
        url = f'{self.addr}/axis/{self.name}/pos'
        payload = {'f64': float(pos)}
        resp = requests.post(url, json=payload, params={'relative': True})
        raise_err(resp)


class Controller:
    """Controller represents a motion controller."""

    def __init__(self, addr, axes=['X', 'Y', 'Z']):
        """Create a new EnsembleController instance.

        Parameters
        ----------
        addr : `str`
            "root" address of the go-hcit motion server.

        """
        self.addr = _niceaddr(addr)
        for axis in axes:
            ax = Axis(self.addr, axis)
            setattr(self, axis, ax)
            setattr(self, axis.lower(), ax)
