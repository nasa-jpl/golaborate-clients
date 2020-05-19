"""cryocon expresses reading of Cryocon Model 12~18i+ monitors over HTTP."""
import requests

from golab_common import raise_err

from retry import retry

ABS_ZERO = -273.15


class TemperatureMonitor:
    """Client class for talking to a temperature monitor through a server."""

    def __init__(self, addr):
        """Create a new TemperatureMonitor instance.

        Parameters
        ----------
        addr : `str`
            "root" address of the go-hcit server, one level above the
            "/read" route.  Must incude port.  startswith http not needed.

        """
        if not addr.startswith('http://'):
            addr = 'http://' + addr

        if 'https' in addr:
            addr = addr.replace('https', 'http')

        self.addr = addr

    @property
    @retry(max_retries=2, interval=1)
    def version(self):
        """The model name and firmware version."""
        resp = requests.get(self.addr + "/version")
        raise_err(resp)
        return str(resp.content).rstrip()

    @retry(max_retries=2, interval=1)
    def read(self, ch='all'):
        """Read some or all of the channels.

        Parameters
        ----------
        ch : `str`, optional
            if all, reads all channels and returns a list of floats, else returns a single float.
            Channels without monitors on them are encoded as NaN.

        Returns
        -------
        `list` of float or `float`

        """
        ch = ch.upper()
        if ch == 'ALL':
            resp = requests.get(self.addr + "/read")
            raise_err(resp)
            ret = resp.json()  # ret is a list or something
            # NaN can't be JSON'd and is encoded as -274
            return [f if f < ABS_ZERO else float('nan') for f in ret]
        else:
            resp = requests.get(f'{self.addr}/read/{ch}')
            raise_err(resp)
            ret = resp.json()['f64']
            if ret < ABS_ZERO:
                ret = float('nan')

            return ret
