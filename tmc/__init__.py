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


class FunctionGenerator:
    """FunctionGenerator is a class exposing access to function generators over HC."""

    def __init__(self, addr):
        """Create a new function generator instance.

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

    def function(self, signal_type=None):
        """Get or set the function type used by the generator.

        Parameters
        ----------
        signal_type : `str`, {'sine', 'square', 'ramp', 'pulse', 'noise'}
            signal type to generate with the hardware
            if None, returns the value from the generator

        Returns
        -------
        `str`
            the signal type being generated

        """
        url = f'{self.addr}/function'
        if signal_type is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['str']

        resp = requests.post(url, json={'str': signal_type})
        raise_err(resp)
        return

    def voltage(self, volts=None):
        """Get or set the voltage used by the generator, Vpp.

        Parameters
        ----------
        volts : `float`
            voltage used, peak to peak
            if None, returns the value from the generator

        Returns
        -------
        `float`
            the voltage being generated

        """
        url = f'{self.addr}/voltage'
        if volts is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']

        resp = requests.post(url, json={'f64': volts})
        raise_err(resp)
        return

    def frequency(self, hertz=None):
        """Get or set the frequency used by the generator, Hz.

        Parameters
        ----------
        hertz : `float`
            frequency used
            if None, returns the value from the generator

        Returns
        -------
        `float`
            the frequency being generated

        """
        url = f'{self.addr}/frequency'
        if hertz is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']

        resp = requests.post(url, json={'f64': hertz})
        raise_err(resp)
        return

    def offset(self, volts=None):
        """Get or set the offset used by the generator, Volts.

        Parameters
        ----------
        volts : `float`
            volts used, peak to peak
            if None, returns the value from the generator

        Returns
        -------
        `float`
            the voltage offset used

        """
        url = f'{self.addr}/offset'
        if volts is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']

        resp = requests.post(url, json={'f64': volts})
        raise_err(resp)
        return

    def output(self, on=None):
        """Get or set the output state, on=True -> output on.

        Parameters
        ----------
        on : `bool`
            output state, on=True -> on
            if None, returns the value from the generator

        Returns
        -------
        `bool`
            if the generator is currently outputting

        """
        url = f'{self.addr}/on'
        if on is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']

        resp = requests.post(url, json={'bool': on})
        raise_err(resp)
        return

    def set_output_load(self, ohms):
        """Set the output load used to correct voltage and frequency error in the generator.

        Parameters
        ----------
        ohms : `float`
            the impedance of the load in ohms

        """
        url = f'{self.addr}/output-load'
        resp = requests.post(url, json={'f64': ohms})
        raise_err(resp)
        return
