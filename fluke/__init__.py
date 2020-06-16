"""Fluke provides tools for accessing Fluke hardware thanks to a go-hcit middleman."""
import requests

from golab_common.retry import retry

from golab_common import raise_err, niceaddr


class DewK:
    """DewK is a class exposing access to DewK temp/humidity meters."""

    def __init__(self, addr):
        """Create a new ITC4000 instance.

        Parameters
        ----------
        addr : `str`
            a network address, with port added.  "host:port".
            HTTP prefix not needed.

        """
        self.addr = niceaddr(addr)

    @property
    @retry(max_retries=2, interval=1)
    def reading(self):
        """Instantaneous Temp/Humidity reading."""
        url = f'{self.addr}/read'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()
