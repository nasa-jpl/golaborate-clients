"""tmc provides tools for working with test and measurement equipment through go-hcit."""
import io

import requests

import numpy as np


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

        resp = requests.post(url, json={'f64': float64(volts)})
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

        resp = requests.post(url, json={'f64': float64(hertz)})
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

        resp = requests.post(url, json={'f64': float64(volts)})
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
        url = f'{self.addr}/output'
        if on is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']

        resp = requests.post(url, json={'bool': on})
        raise_err(resp)
        return

    def raw(self, cmd):
        """Raw sends text to the device and returns any response."""
        url = f'{self.addr}/raw'
        resp = requests.post(url, json={'str': cmd})
        raise_err(resp)
        return resp.json()['str']


class Oscilloscope:
    """Oscilloscope is a class providing remote access to an oscilloscope through go-hcit."""

    def __init__(self, addr):
        """Create a new scope instance.

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

    def scale(self, channel='1', volts_full_scale=None):
        """Full vertical scale of the oscilloscope.

        Parameters
        ----------
        volts_full_scale : `float`
            number of volts full scale on the scope screen

        Returns
        -------
        `float`
            volts full scale, if input is None

        """
        url = f'{self.addr}/scale'
        if volts_full_scale is None:
            resp = requests.get(url, json={'channel': channel})
            raise_err(resp)
            return resp.json()['f64']

        resp = requests.post(url, json={'scale': float(volts_full_scale), 'channel': channel})
        raise_err(resp)
        return

    def timebase(self, seconds_full_width=None):
        """Full horizontal scale of the oscilloscope.

        Parameters
        ----------
        seconds_full_width : `float`
            number of seconds of data on the scope screen

        Returns
        -------
        `float`
            width of the scope window, if input is None

        """
        url = f'{self.addr}/timebase'
        if seconds_full_width is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']

        resp = requests.post(url, json={'f64': float(seconds_full_width)})
        raise_err(resp)
        return

    def bit_depth(self, bits=None):
        """Bit depth of the scope acquisition.

        Parameters
        ----------
        bits : `int`
            number of bits, 8 for 8 bit, 16 for 16-bit, etc

        Returns
        -------
        `int`
            bit depth, if input is None

        """
        url = f'{self.addr}/bit-depth'
        if bits is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['int']

        resp = requests.post(url, json={'int': int(bits)})
        raise_err(resp)
        return

    def sample_rate(self, samples_per_second=None):
        """Sample rate of the scope acquisition.

        Parameters
        ----------
        samples_per_second : `int`
            number of samples per second

        Returns
        -------
        `int`
            samples per second, if input is None

        """
        url = f'{self.addr}/sample-rate'
        if samples_per_second is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['int']

        resp = requests.post(url, json={'int': int(samples_per_second)})
        raise_err(resp)
        return

    def acq_length(self, samples=None):
        """Length of the scope acquisition.

        Parameters
        ----------
        samples : `int`
            number of samples of data

        Returns
        -------
        `int`
            samples, if input is None

        """
        url = f'{self.addr}/acq-length'
        if samples is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['int']

        resp = requests.post(url, json={'int': int(samples)})
        raise_err(resp)
        return

    def acq_mode(self, mode=None):
        """Acquisition mode of the scope.

        Parameters
        ----------
        mode : `str`
            acquisition mode, nominally "RTIME" for realtime

        Returns
        -------
        `str`
            acquisition mode if input is None

        """
        url = f'{self.addr}/acq-mode'
        if mode is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['str']

        resp = requests.post(url, json={'str': mode})
        raise_err(resp)
        return

    def acq_waveform(self, channels=['1', '2', '3', '4']):
        """Acquire a waveform from the scope.

        Parameters
        ----------
        channels : `iterable` of `str`
            which channels to acquire

        Returns
        -------
        `dict`
            with keys:
                - started -- datetime.datetime
                - time -- linear array of time in seconds
                - (each element of channels) -- linear array of waveform data, volts

        """
        url = f'{self.addr}/acq-waveform'
        resp = requests.get(url, json={'channels': channels})
        raise_err(resp)
        file = io.BytesIO(resp.content)
        ary = np.loadtxt(file, skiprows=1, delimiter=',')
        return ary

    def raw(self, cmd):
        """Raw sends text to the device and returns any response."""
        url = f'{self.addr}/raw'
        resp = requests.post(url, json={'str': cmd})
        raise_err(resp)
        return resp.json()['str']


class DAQ:
    """DAQ is an interface to Keysight DAQ970 series and 34000 series DAQs."""

    def __init__(self, addr):
        """Create a new DAQ instance.

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

    def label(self, channel, label):
        """Set the label for a given channel.

        Parameters
        ----------
        channel : `int`
            which channel to set the label for
        label : `str`
            the label to use

        """
        url = f'{self.addr}/label'
        payload = {'channel': int(channel), 'label': label}
        resp = requests.post(url, json=payload)
        raise_err(resp)
        return

    def configure(self, measurement, range_, resolution, channels, dc=True):
        """Configure the selected channel(s).

        Parameters
        ----------
        measurement : `str`, {'volt', 'curr'}
            voltage or current
        range : `float`
            symmetric range to digitize over
        channels : `iterable` of `int`
            list of channels to configure.  Accepts single int, too.
        dc : `bool`
            if True, configure for DC coupling; else AC.

        """
        if isinstance(channels, int):
            channels = [channels]

        url = f'{self.addr}/configure'
        payload = {
            'channels': channels,
            'measurement': measurement,
            'range': float(range_),
            'resolution': float(resolution),
            'dc': dc,
        }
        resp = requests.post(url, json=payload)
        raise_err(resp)
        return

    def sample_rate(self, samples_per_second=None):
        """Configure the sampling (scan) rate of the DAQ.

        Parameters
        ----------
        samples_per_second : `int`
            number of samples per second

        Returns
        -------
        `int`
            number of samples per second the DAQ makes

        """
        url = f'{self.addr}/sample-rate'
        if samples_per_second is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['int']
        else:
            payload = {'int': int(samples_per_second)}
            resp = requests.post(url, json=payload)
            raise_err(resp)
            return

    def recording_channel(self, channel=None):
        """Get or set the channel used in recording.

        Parameters
        ----------
        channel : `int`
            which channel to use

        Returns
        -------
        `int`
            the channel being used

        """
        url = f'{self.addr}/recording-channel'
        if channel is None:
            resp = requests.get(url)
            raise_err(resp)
            return reps.json()['int']
        else:
            payload = {'int': int(channel)}
            resp = requests.post(url, json=payload)
            raise_err(resp)
            return

    def recording_length(self, samples):
        """Get or set the length of a recording in samples.

        Parameters
        ----------
        channel : `int`
            which channel to use

        Returns
        -------
        `int`
            the channel being used

        """
        url = f'{self.addr}/recording-length'
        if samples is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['int']
        else:
            payload = {'int': int(samples)}
            resp = requests.post(url, json=payload)
            raise_err(resp)
            return

    def record(self):
        """Capture a recording and return the data as a numpy array."""
        url = f'{self.addr}/record'
        resp = requests.get(url)
        raise_err(resp)
        src = io.BytesIO(resp.content)
        return np.loadtxt(src, delimiter=',', skiprows=1)
