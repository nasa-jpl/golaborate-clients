"""DAC is the arm of DAQ that deals with D to A."""
import warnings

import requests

from golab_common import niceaddr, raise_err


class DAC:
    """D to A converter."""

    def __init__(self, addr):
        """Create a new DAC instance.

        Parameters
        ----------
        addr : str
            "root" address of the golab server, e.g. localhost:8000/my-dac

        """
        self.addr = niceaddr(addr)

    def output(self, channels, voltages=None):
        """Read the ideal output of a channel, or write voltages to a channel.

        Parameters
        ----------
        channels : int or Iterable of ints
            either a single channel, channels=1, or a sequence of channels
            channels=[1,2,3]
        voltages : float or Iterable of float
            either a single float, voltages=1.234 or a sequence of floats,
            voltage=[1.234, 2.345, 3.456]
            if None, reads the ideal output

        Returns
        -------
        None or float or Iterable of floats
            None if voltages != None
            single float if voltages=None and channels is an int,
            list of float otherwise

        """
        if isinstance(channels, int):
            url = f'{self.addr}/output'
        else:
            url = f'{self.addr}/output-multi'
            if voltages is not None:
                voltages = list(voltages)
            channels = list(channels)

        if voltages is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()
        else:
            resp = requests.post(url, json={
                'channel': channels,
                'voltage': voltages})
            raise_err(resp)

    def output_dn(self, channels, dns=None):
        """Read the ideal output of a channel, or write 16-bit DN to a channel.

        Parameters
        ----------
        channels : int or Iterable of ints
            either a single channel, channels=1, or a sequence of channels
            channels=[1,2,3]
        dns : int or Iterable of int
            either a single int, voltages=2**15 or a sequence of ints,
            voltage=[0, 2049, 4096]
            if None, reads the ideal output

        Returns
        -------
        None or int or Iterable of ints
            None if dns != None
            single int if dns=None and channels is an int,
            list of ints otherwise

        """
        if isinstance(channels, int):
            url = f'{self.addr}/output-dn-16'
        else:
            url = f'{self.addr}/output-multi-dn-16'
            if dns is not None:
                dns = list(dns)
            channels = list(channels)

        if dns is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()
        else:
            resp = requests.post(url, json={
                'channel': channels,
                'dn': dns})
            raise_err(resp)

    def range(self, channel, range_=None):
        """Configure the output range of a channel.

        Parameters
        ----------
        channel : int
            a channel identifier
        range : str, optional
            a CSV of lower and upper voltages; <low>,<high>.
            E.g., "0,10" or "-5,5" or "-2.5,7.5", etc.
            Voltages in volts.
            if None, returns the range which is active

        Returns
        -------
        str
            range of a channel, formatted as above.

        """
        url = f'{self.addr}/range'
        if range_ is None:
            resp = requests.get(url, json={'channel': channel})
            raise_err(resp)
            return resp.json()['str']
        else:
            resp = requests.post(url, json={'channel': channel, 'range': range_})
            raise_err(resp)

    def simultaneous(self, channel, boolean=None):
        """Configure a channel for simultaneous triggering (True).

        The DAC triggers all channels for which simultaneous is True in a ganged
        fashion.  All of the channels should be written to with .output and a
        list to observe the desired behavior, or used in one of the waveform
        triggering modes.

        e.g.,
        chans = [1,2,3]
        for chan in chans:
            dac.simultaneous(chan, True)

        dac.output_multi(chans, [0.001, 0.002, 0.003])

        Parameters
        ----------
        channel : int
            a channel identifier
        boolean : bool, optional
            True  -> simultaneous triggering
            False -> asynchronous triggering

        Returns
        -------
        bool
            True if the channel is triggered simultaneously with others

        """
        url = f'{self.addr}/simultaneous'
        if boolean is None:
            resp = requests.get(url, json={'channel': channel})
            raise_err(resp)
            return resp.json()['bool']
        else:
            resp = requests.post(url, json={'channel': channel, 'simultaneous': boolean})
            raise_err(resp)

    def operating_mode(self, channel, mode=None):
        """Configure the operating mode of a channel.

        Parameters
        ----------
        channel : int
            a channel identifier
        mode : str, {"single", "waveform"}
            which mode to use (single sample or waveform)

        Returns
        -------
        str
            the operating mode

        """
        url = f'{self.addr}/operating-mode'
        if mode is None:
            resp = requests.get(url, json={'channel': channel})
            raise_err(resp)
            return resp.json()['str']
        else:
            resp = requests.post(url, json={'channel': channel, 'operatingMode': mode})
            raise_err(resp)

    def trigger_mode(self, channel, mode=None):
        """Configure the triggering mode of a channel.

        Parameters
        ----------
        channel : int
            a channel identifier
        mode : str, {"software", "timer", "external"}
            how to trigger

        Returns
        -------
        str
            the triggering mode

        """
        url = f'{self.addr}/trigger-mode'
        if mode is None:
            resp = requests.get(url, json={'channel': channel})
            raise_err(resp)
            return resp.json()['str']
        else:
            resp = requests.post(url, json={'channel': channel, 'triggerMode': mode})
            raise_err(resp)

    def start(self):
        """Start playback."""
        url = f'{self.addr}/playback/start'
        resp = requests.post(url)
        raise_err(resp)
        return

    def stop(self):
        """Stop playback."""
        url = f'{self.addr}/playback/stop'
        resp = requests.post(url)
        raise_err(resp)
        return

    def timer_period_ns(self, nanoseconds=None):
        """Configure the on-board timer period, which is global to the DAC.

        Parameters
        ----------
        nanoseconds : int
            number of nanoseconds between samples at the output.
            For the Acromag AP235's internal timer, must be / will be rounded
            modulo 32.

        Returns
        -------
        int
            nanoseconds between timer ticks

        """
        url = f'{self.addr}/timer-period'
        if nanoseconds is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['uint']
        else:
            resp = requests.post(url, json={'uint': nanoseconds})
            raise_err(resp)

    def timer_period_s(self, seconds=None):
        """Timer_period_ns, except the argument is in seconds."""
        if seconds is None:
            return self.timer_period_ns(None) / 1e9
        else:
            return self.timer_period_ns(seconds*1e9)

    def load_waveform(self, filename, period_ns):
        """Load a waveform; compatible with Acromag AP235 and dacsrv only.

        Parameters
        ----------
        filename : str
            name of the file, **on the PC running dacsrv**
            either adjacent to the executable, or an absolute path
        period_ns : int
            inter-sample period in nanoseconds

        Notes
        -----
        call dac.start() after, to begin playable
        if playback is stopped, calling start again is undefined behavior;
        re-load the waveform first.

        """
        if not isinstance(period_ns, int):
            warnings.warn(f'{period_ns=} was not an int, casting...')
            period_ns = int(period_ns)

        url = f'{self.addr}/load-waveform'
        payload = {'filename': filename}
        resp = requests.post(url, json=payload)
        raise_err(resp)
