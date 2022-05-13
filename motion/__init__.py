"""motion enables nice control of motion controllers (and stages) over HTTP via a go-hcit server."""
import time
import requests

from golab_common.retry import retry

from golab_common import niceaddr, raise_err


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
        self.addr = niceaddr(addr)
        self.name = name

    @retry(max_retries=2, interval=1)
    def home(self):
        """Home the axis."""
        url = f'{self.addr}/axis/{self.name}/home'
        resp = requests.post(url)
        raise_err(resp)

    @retry(max_retries=2, interval=1)
    def enable(self):
        """Enable the axis."""
        url = f'{self.addr}/axis/{self.name}/enabled'
        payload = {'bool': True}
        resp = requests.post(url, json=payload)
        raise_err(resp)

    @retry(max_retries=2, interval=1)
    def disable(self):
        """Disable the axis."""
        url = f'{self.addr}/axis/{self.name}/enabled'
        payload = {'bool': False}
        resp = requests.post(url, json=payload)
        raise_err(resp)

    @retry(max_retries=2, interval=1)
    def initialize(self):
        """Initialize the axis."""
        url = f'{self.addr}/axis/{self.name}/initialize'
        resp = requests.post(url)
        raise_err(resp)

    @property
    @retry(max_retries=2, interval=1)
    def enabled(self):
        """Boolean for if the axis is enabled."""
        url = f'{self.addr}/axis/{self.name}/enabled'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['bool']

    @property
    @retry(max_retries=2, interval=1)
    def pos(self):
        """Position of the axis."""
        url = f'{self.addr}/axis/{self.name}/pos'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['f64']

    @property
    @retry(max_retries=2, interval=1)
    def limits(self):
        """Limits of the axis."""
        resp = requests.get(f'{self.addr}/axis/{self.name}/limits')
        raise_err(resp)
        return resp.json()

    @retry(max_retries=2, interval=1)
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

    @retry(max_retries=2, interval=1)
    def move_abs(self, pos, async_max_checks=-1):
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

        try:
            sync = self.synchronous()
        except:
            # unknown, we are in sync mode
            sync = True

        if not sync:
            wait_inpos(self, async_max_checks)

    @retry(max_retries=2, interval=1)
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

    @retry(max_retries=2, interval=1)
    def synchronous(self, sync=None):
        url = f'{self.addr}/axis/{self.name}/synchronous'
        if sync is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            payload = {'bool': sync}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @property
    @retry(max_retries=2, interval=1)
    def inpos(self):
        """Position of the axis."""
        url = f'{self.addr}/axis/{self.name}/inposition'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['bool']


class Controller:
    """Controller represents a motion controller."""

    def __init__(self, addr, axes=['X', 'Y', 'Z']):
        """Create a new EnsembleController instance.

        Parameters
        ----------
        addr : `str`
            "root" address of the go-hcit motion server.

        """
        self.addr = niceaddr(addr)
        for axis in axes:
            ax = Axis(self.addr, axis)
            setattr(self, axis, ax)
            setattr(self, axis.lower(), ax)

    def raw(self, text):
        """Send a string to the controller and get back any response.

        Parameters
        ----------
        text : `str`
            the text to send, will have a newline added.

        Returns
        -------
        `str`
            any text returned

        """
        url = f'{self.addr}/raw'
        payload = {'str': text}
        resp = requests.post(url, json=payload)
        raise_err(resp)
        return resp.json().get('str', None)


def wait_inpos(axis, max_check=-1):
    # check the first time
    start = time.now()
    inpos = axis.inpos
    end = time.now()
    deltaT = end - start
    wait_t = deltaT * 4
    if inpos:
        return

    time.sleep(wait_t)

    if max_check >= 1:
        checks = 1
        while checks <= max_check:
            inpos = axis.inpos
            if inpos:
                return

            checks += 1
            time.sleep(wait_t)
