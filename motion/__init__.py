"""motion enables nice control of motion controllers (and stages) over HTTP via a go-hcit server."""
import time
import math
import warnings

import requests

from golab_common.retry import retry

from golab_common import niceaddr, raise_err


class Axis:
    """Axis represents an axis of a stage."""

    def __init__(self, addr, name):
        """Create a new Axis instance.

        Parameters
        ----------
        addr : str
            "root" address of the go-hcit motion server.
        name : str
            name of the axis, as the controller knows it

        """
        self.addr = niceaddr(addr)
        self.name = name

    def home(self):
        """Home the axis."""
        url = f'{self.addr}/axis/{self.name}/home'
        resp = requests.post(url)
        raise_err(resp)

    def stop(self):
        """Stop the axis."""
        url = f'{self.addr}/axis/{self.name}/stop'
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

    def enabled(self):
        """Boolean for if the axis is enabled."""
        url = f'{self.addr}/axis/{self.name}/enabled'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['bool']

    def homed(self):
        """Boolean for if the axis is homed."""
        url = f'{self.addr}/axis/{self.name}/home'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['bool']

    def pos(self):
        """Position of the axis."""
        url = f'{self.addr}/axis/{self.name}/pos'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['f64']

    def limits(self):
        """Limits of the axis."""
        resp = requests.get(f'{self.addr}/axis/{self.name}/limits')
        raise_err(resp)
        return resp.json()

    def velocity(self, value=None):
        """Velocity setpoint of the axis.

        Parameters
        ----------
        value: float
            velocity of the axis, in mm/s

        Returns
        -------
        float
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

    def move_abs(self, pos, sync=True, wait_inpos_kwargs=None):
        """Move the axis to an absolute position.

        Parameters
        ----------
        pos : float
            position to move to
        sync : bool, optional
            if True and the controller is configured in asynchronous mode, poll
            until it is in position using self.wait_inpos and associated kwargs
        wait_inpos_kwargs : dict, optional
            keyword arguments for self.wait_inpos


        """
        url = f'{self.addr}/axis/{self.name}/pos'
        payload = {'f64': float(pos)}
        resp = requests.post(url, json=payload)
        raise_err(resp)

        if not sync and wait_inpos_kwargs is not None:
            warnings.warn('move_abs: sync and wait_inpos_kwargs are deprecated and have no effect')

    def move_rel(self, pos, sync=True, wait_inpos_kwargs=None):
        """Move the axis by a relative amount.

        Parameters
        ----------
        pos : float
            amount to move by

        """
        url = f'{self.addr}/axis/{self.name}/pos'
        payload = {'f64': float(pos)}
        resp = requests.post(url, json=payload, params={'relative': True})
        raise_err(resp)

        if not sync and wait_inpos_kwargs is not None:
            warnings.warn('move_abs: sync and wait_inpos_kwargs are deprecated and have no effect')

    def synchronous(self, sync=None):
        """Synchronous mode for the axis.

        wait_inpos and the sync arguments to the two move functions provide
        comprehensive support for asynchronous styles

        Parameters
        ----------
        sync : bool
            True = controller replies after move ended
            False = controller replies after move starts

        Returns
        -------
        bool
            synchronous, if value=None

        """
        url = f'{self.addr}/axis/{self.name}/synchronous'
        if sync is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            payload = {'bool': sync}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    def inpos(self):
        """Position of the axis."""
        url = f'{self.addr}/axis/{self.name}/inposition'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['bool']

    def wait_inpos(self, max_check=None, max_time=None, min_interval=0.1, controller_latency_scale=4):
        """Return when an axis to be in position.

        Parameters
        ----------
        max_checks : int, optional
            the maximum number of checks to perform
            if None, unbounded
        max_time : float, optional
            the maximum duration (seconds) to wait for the axis to be in position
            if None, unbounded
        min_interval : float, optional
            the minimum checking interval, seconds
            if None, controller_latency_scale times a measurement of the latency
            is used
            i.e., time_to_check * controller_latency_scale is the polling interval

        """
        # check the first time, profile the time taken to check
        start = time.time()
        inpos = self.inpos()
        end = time.time()
        deltaT = end - start
        wait_t = deltaT * controller_latency_scale

        if min_interval is not None and wait_t < min_interval:
            wait_t = min_interval

        if max_time is None:
            max_time = math.inf

        if inpos:
            return

        time.sleep(wait_t)

        if max_check is not None:
            checks = 1
            while checks <= max_check and not self.inpos:
                end = time.time()
                dT = end - start
                if dT > max_time:
                    return

                checks += 1
                time.sleep(wait_t)
        else:
            while not self.inpos:
                end = time.time()
                dT = end - start
                if dT > max_time:
                    return
                time.sleep(wait_t)


class Controller:
    """Controller represents a motion controller."""

    def __init__(self, addr, axes=['X', 'Y', 'Z']):
        """Create a new EnsembleController instance.

        Parameters
        ----------
        addr : str
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
        text : str
            the text to send, will have a newline added.

        Returns
        -------
        str
            any text returned

        """
        url = f'{self.addr}/raw'
        payload = {'str': text}
        resp = requests.post(url, json=payload)
        raise_err(resp)
        return resp.json().get('str', None)
