"""tmc provides tools for working with test and measurement equipment through go-hcit."""
import io

import requests

import numpy as np

from retry import retry

from golab_common import raise_err


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

    @retry(max_retries=2, interval=1)
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

    @retry(max_retries=2, interval=1)
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

        resp = requests.post(url, json={'f64': float(volts)})
        raise_err(resp)
        return

    @retry(max_retries=2, interval=1)
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

        resp = requests.post(url, json={'f64': float(hertz)})
        raise_err(resp)
        return

    @retry(max_retries=2, interval=1)
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

        resp = requests.post(url, json={'f64': float(volts)})
        raise_err(resp)
        return

    @retry(max_retries=2, interval=1)
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

    @retry(max_retries=2, interval=1)
    def upload_arb(self, ary):
        """Upload an arbitrary waveform to the the function generator.

        While the data is 16 bit, it must not be too large for the DAC on
        the hardware.  For 12-bit data, this means not exceeding 4095

        Parameters
        ----------
        ary : `numpy.ndarray`
            ndarray with ndim == 1, dtype == uint16
            for the Agilent 33250A, len < 65535 as well

        """
        if ary.ndim != 1:
            raise ValueError("array must be of dimension 1")
        if ary.dtype != np.uint16:
            raise ValueError("array must be of dtype uint16")

        url = f'{self.addr}/waveform'
        resp = requests.post(url, ary.tobytes())
        raise_err(resp)

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
        channel : `str`
            which channel to set the scale for
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

    def acq_waveform(self, channels=('1', '2', '3', '4')):
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

    @retry(max_retries=2, interval=1)
    def label(self, channel, label):
        """Set the label for a given channel.

        Parameters
        ----------
        channel : `int`
            which channel to set the label for
        label : `str`
            the label to use

        """
        url = f'{self.addr}/channel-label'
        payload = {'channel': int(channel), 'label': label}
        resp = requests.post(url, json=payload)
        raise_err(resp)
        return

    @retry(max_retries=2, interval=1)
    def configure(self, measurement, range_, resolution, channels, dc=True):
        """Configure the selected channel(s).

        Parameters
        ----------
        measurement : `str`, {'volt', 'curr'}
            voltage or current
        range_ : `float`
            symmetric range to digitize over
        resolution : `float`
            resolution to digitize with
        channels : `iterable` of `int`
            list of channels to configure.  Accepts single int, too.
        dc : `bool`
            if True, configure for DC coupling; else AC.

        """
        if isinstance(channels, int):
            channels = [channels]

        channels = ','.join((str(e) for e in channels))
        string = f'*CLS;:CONF:{measurement.upper()}:{"DC" if dc else "AC"} {range_},{resolution}, (@{channels});:SYST:ERROR?'  # NOQA
        resp = self.raw(string)
        if not resp[:2] == "+0":
            raise Exception(resp)

    @retry(max_retries=2, interval=1)
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
            return resp.json()['f64']
        else:
            payload = {'f64': float(samples_per_second)}
            resp = requests.post(url, json=payload)
            raise_err(resp)
            return

    @retry(max_retries=2, interval=1)
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
            return resp.json()['int']
        else:
            payload = {'int': int(channel)}
            resp = requests.post(url, json=payload)
            raise_err(resp)
            return

    @retry(max_retries=2, interval=1)
    def recording_length(self, samples=None):
        """Get or set the length of a recording in samples.

        Parameters
        ----------
        samples : `int`
            how many samples are in the record

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

    @retry(max_retries=2, interval=1)
    def record(self):
        """Capture a recording and return the data as a numpy array."""
        url = f'{self.addr}/record'
        resp = requests.get(url)
        raise_err(resp)
        src = io.BytesIO(resp.content)
        return np.loadtxt(src, delimiter=',', skiprows=1)

    @retry(max_retries=2, interval=1)
    def raw(self, cmd):
        """Raw sends text to the device and returns any response."""
        url = f'{self.addr}/raw'
        resp = requests.post(url, json={'str': cmd})
        raise_err(resp)
        return resp.json()['str']
