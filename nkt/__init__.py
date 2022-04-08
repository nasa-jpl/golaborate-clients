"""nkt exposes control of the NKT superK Extreme sources."""

import requests

from golab_common.retry import retry

from golab_common import raise_err, niceaddr


class SuperK:
    """SuperK enables programmatic control of NKT SuperK lasers."""

    def __init__(self, addr):
        """Create a new SuperK instance.

        Parameters
        ----------
        addr : `str`
            IP address (port included) that the HTTP adapter server is listening at

        """
        self.addr = niceaddr(addr)

    @retry(max_retries=2, interval=1)
    def center_bandwidth(self, center=None, bw=None):
        """Get or set the center wavelength and full bandwidth.

        Notes
        -----
        With center=None, bw=None, gets the current values.  If either is not None, sets.
        If center = 500 and bw = 100, the short wavelength will be 450 and the long wavelength 550.

        Parameters
        ----------
        center : `float`
            center wavelength, if `None` gets the current values
        bw : `float`
            full bandwidth

        Returns
        -------
        (center, bw) (float, float) if center is None.
        If a new value is programmed, returns nothing on success,
        or raises an error on failure.

        """
        url = f'{self.addr}/wvl/center-bandwidth'
        if center is None:
            resp = requests.get(url)
            raise_err(resp)
            json = resp.json()
            return json['center'], json['bandwidth']
        else:
            data = {'center': float(center), 'bandwidth': float(bw)}
            resp = requests.post(url, json=data)
            raise_err(resp)

    @retry(max_retries=2, interval=1)
    def short_wave(self, wvl_nm=None):
        """Get or set the short wavelength of the VARIA.

        Parameters
        ----------
        wvl_nm : `float`
            wavelength in nanometers, if None gets, else sets

        Returns
        -------
        `float`
            short wavelength, nm

        """
        url = f'{self.addr}/wvl/short'
        if wvl_nm is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']
        else:
            payload = {'f64': float(wvl_nm)}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @retry(max_retries=2, interval=1)
    def long_wave(self, wvl_nm=None):
        """Get or set the long wavelength of the VARIA.

        Parameters
        ----------
        wvl_nm : `float`
            wavelength in nanometers, if None gets, else sets

        Returns
        -------
        `float`
            short wavelength, nm

        """
        url = f'{self.addr}/wvl/long'
        if wvl_nm is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']
        else:
            payload = {'f64': float(wvl_nm)}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @retry(max_retries=2, interval=1)
    def emission(self, on=None):
        """Get or set the emission.

        Notes
        -----
        If on is None, gets the state, returns bool.  Otherwise manipulates emission state

        Parameters
        ----------
        on : `bool`, optional
            None => get.  True => laser on.  False => laser off.

        Returns
        -------
        `bool`
            laser on/off

        """
        url = f'{self.addr}/emission'
        if on is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            payload = {'bool': bool(on)}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @retry(max_retries=2, interval=1)
    def ND(self, pct=None):  # NOQA
        """Get or set the VARIA ND strength.

        Parameters
        ----------
        pct : `float`, optional
            0=ND inactive, 100=ND at full strength.  If None, gets the value and returns it.

        Returns
        -------
        `float`
            ND strength, percent

        """
        url = f'{self.addr}/nd'
        if pct is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']
        else:
            payload = {'f64': float(pct)}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @retry(max_retries=2, interval=1)
    def power(self, pct=None):
        """Get or set the main module power level.

        Parameters
        ----------
        pct : `float`, optional
            0= "off", 100= "full power".  If None, gets the value and returns it.

        Returns
        -------
        `float`
            power level, percent

        """
        url = f'{self.addr}/power'
        if pct is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['f64']
        else:
            payload = {'f64': float(pct)}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    @retry(max_retries=2, interval=1)
    def status_main(self):
        """Get the status bitfield from the main module."""
        url = f'{self.addr}/main-module-status'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()

    @retry(max_retries=2, interval=1)
    def status_varia(self):
        """Get the status bitfield from the VARIA module."""
        url = f'{self.addr}/varia-status'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()

    @property
    @retry(max_retries=2, interval=1)
    def emission_runtime(self):
        """Emission runtime of the laser in seconds."""
        url = f'{self.addr}/emission-runtime'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()['f64']
