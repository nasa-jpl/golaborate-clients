"""nkt exposes control of the NKT superK Extreme sources."""

import requests


class SuperK:
    """SuperK enables programmatic control of NKT SuperK lasers."""

    def __init__(self, ip):
        """Create a new SuperK instance.

        Parameters
        ----------
        ip : `str`
            IP address (port included) that the HTTP adapter server is listening at

        """
        self.ip = "http://" + ip

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
        url = self.ip + "/wl-center-bandwidth"
        if center is None:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception(resp.content)
            json = resp.json()
            return json['center'], json['bandwidth']
        else:
            data = {'center': center, 'bandwidth': bw}
            resp = requests.post(url, json=data)
            if resp.status_code != 200:
                raise Exception(resp.content)

    def emission(self, on=None):
        """Get or set the emission.

        Notes
        -----
        If on is None, gets the state, returns bool.
        If on is True, turns the laser on.  No return, or error.
        If on is False, turns the laser off.  No return, or error.

        Parameters
        ----------
        on : `bool`, optional
            None => get.  True => laser on.  False => laser off.

        Returns
        -------
        `bool`
            laser on/off

        """
        if on is None:
            url = self.ip + "/emission"
        else:
            if on is False:
                url = self.ip + "/emission/off"
            elif on is True:
                url = self.ip + "/emission/on"

        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception(resp.content)
        else:
            if on is None:
                return resp.json()['bool']

    def ND(self, pct=None):
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
        url = self.ip + "/nd"
        if pct is None:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception(resp.content)
            else:
                return resp.json()['f64']
        else:
            payload = {'f64': pct}
            resp = requests.post(url, json=payload)
            if resp.status_code != 200:
                raise Exception(resp.content)

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
        url = self.ip + "/power"
        if pct is None:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception(resp.content)
            else:
                return resp.json()['f64']
        else:
            payload = {'f64': pct}
            resp = requests.post(url, json=payload)
            if resp.status_code != 200:
                raise Exception(resp.content)

    def status_main(self):
        """Get the status bitfield from the main module."""
        url = self.ip + "/main-module-status"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception(resp.content)
        else:
            return resp.json()

    def status_varia(self):
        """Get the status bitfield from the VARIA module."""
        url = self.ip + "/varia-status"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise Exception(resp.content)
        else:
            return resp.json()
