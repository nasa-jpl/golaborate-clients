"""andor expresses control of Andor cameras over HTTP."""

# note that the name SDK3Cam may become Camera in the future
# if the SDK2 operation can be made api compatible.
# in that circumstance, Camera will be re-exported
# as SDK3Cam to maintain backwards compatible.

import numbers
from io import BytesIO

from astropy import units as u
from astropy.io import fits

try:
    from imageio import imread
except ImportError:
    pass  # non-fits formats are optional

import requests


def raise_err(resp):
    """Raises an exception if the response status code is not 200.

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
        raise Exception(str(resp.content).strip())


def proces_exposure_time(t):
    """Convert an exposure time to the server's format.

    Parameters
    ----------
    t : `numbers.Number`, `str`, or `astropy.units.Quantity`
        a time-like object.  If a number (int, float) units of seconds

    Returns
    -------
    `str`
        a string looking like "30s" or "1h30m", or "10.5us" and so on.

    Raises
    ------
    ValueError
        wrong input type

    """
    if isinstance(t, u.Quantity):
        # user wants to manage their own units
        t = str(t).replace(" ", "")
    elif isinstance(t, numbers.Number):
        # float or int, seconds
        t = str(t) + "s"
    elif isinstance(t, str):
        pass  # str is a no-op, but we don't want to trigger the default clause (raises exception)
    else:
        raise ValueError('t must be of type astropy.units.Quantity, int, float, or string')

    return t


class SDK3Cam:
    def __init__(self, addr, time_convention='float'):
        """Create a new SDK3Cam instance.

        Parameters
        ----------
        addr : `str`
            "root" address of the go-hcit andor server, one level above the
            "/image" route.  Must incude port.  startswith http not needed.
        time_convention : `str`, {'float', 'astropy'}
            either float (exposure time returns as floating point seconds) or
            astropy (exposure time returns as astropy quantity)

        """
        if not addr.startswith('http://'):
            addr = 'http://' + addr

        if 'https' in addr:
            addr = addr.replace('https', 'http')

        self.addr = addr
        self.time_convention = time_convention

    # generics
    @property
    def features(self):
        """A dictionary mapping feature names to strings representing their types."""
        resp = requests.get(self.addr + "/feature")
        raise_err(resp)
        return resp.json()

    def set_feature(self, feature, value):
        """Set the value of a feature on the camera.

        Parameters
        ----------
        feature : `str`
            a feature that is a valid key to self.features
        value : `str`, `float`, `int`, or `bool`
            the value of the feature

        """
        url = f'{self.addr}/feature/{feature}'
        # andor-http server requires us to properly tag the datatype
        if isinstance(value, str):
            key = 'str'
        elif isinstance(value, float):
            key = 'f64'
        elif isinstance(value, int):
            key = 'int'
        elif isinstance(value, bool):
            key = 'bool'

        payload = {key: value}
        resp = requests.post(url, data=payload)
        raise_err(resp)
        return

    def get_feature(self, feature):
        """Get the value of a feature on the camera.

        Parameters
        ----------
        feature : `str`
            a feature that is a valid key to self.features

        Returns
        -------
        `str`, `float`, `int`, or `bool`
            varies with the feature, see the values in the self.features dict
        """
        url = f'{self.addr}/feature/{feature}'
        resp = requests.get(url)
        raise_err(resp)
        d = resp.json()
        keys = list(d.keys())
        k = keys[0]
        return d[k]

    def exposure_time(self, t=None):
        """Get or set the exposure time.  If t=None, gets.  If t!=None, sets.

        Parameters
        ----------
        t : `str`, `numbers.Number`, or `astropy.units.Quantity`
            something process_exposure_time can turn into the format expected
            by the server.  See help(andor.process_exposure_time).


        Returns
        -------
        `float` or `astropy.units.Quantity`
            if float, seconds.  Return type depends on self.time_convention

        """
        url = f'{self.addr}/exposure-time'
        if t is None:
            resp = requests.get(url)
            raise_err(resp)
            tsec = resp.json()['f64']
            if self.time_convention == 'float':
                return tsec
            else:
                return tsec * u.s
        else:
            t = proces_exposure_time(t)
            resp = requests.post(url, params={'exposureTime': t})
            raise_err(resp)
            return

    # thermal
    def fan(self, on=None):
        """Turns the fan on or off (on != None), or checks if it's on (true).

        Parameters
        ----------
        on : `bool`, optional
            whether the fan should be on (true) or off (false)

        Returns
        `bool`
            if the fan is on (true) or off (false)

        """
        url = f'{self.addr}/fan'
        if on is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            resp = requests.get(url, data={'bool': on})
            raise_err(resp)
            return

    def sensor_cooling(self, on=False):
        """Turns the TEC cooler on or off (on != None), or checks if it's on (true).

        Parameters
        ----------
        on : `bool`, optional
            whether the TEC cooler should be on (true) or off (false)

        Returns
        `bool`
            if the TEC cooler is on (true) or off (false)

        """
        # the body of this is identical to self.fan() but with a different URL
        url = f'{self.addr}/sensor-cooling'
        if on is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            resp = requests.get(url, data={'bool': on})
            raise_err(resp)
            return

    @property
    def temperature(self):
        """The current sensor temperature in Celcius."""
        resp = requests.get(self.addr + "/temperature")
        raise_err(resp)
        return resp.json()['f64']

    def temperature_setpt(self, valueS=None):
        """Get (valueS=None) or set the current temperature setpoint.

        Notes
        -----
        Calling self.temperature_setpt(self.temperature_setpt_options[-1]) is
        a good macro for setting the detector as cold as possible, and likewise
        ...options[0] as warm as possible without disabling the TEC.

        Parameters
        ----------
        valueS : `str`, optional
            a string representing a temperature.  Must be in self.temperature_setpt_options.

        Returns
        -------
        `str`
            the current temperature setpoint, in Celcius

        """
        # the body of this is identical to self.fan() but with a different URL and typecode for json
        url = f'{self.addr}/temperature-setpoint'
        if valueS is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['str']
        else:
            resp = requests.get(url, data={'str': valueS})
            raise_err(resp)
            return

    @property
    def temperature_setpt_options(self):
        """The currently allowed temperature setpoint options."""
        resp = requests.get(self.addr + '/temperature-setpoint-options')
        raise_err(resp)
        return resp.json()

    @property
    def cooling_status(self):
        """The current cooling status."""
        resp = requests.get(self.addr + "/temperature-status")
        raise_err(resp)
        return resp.json()['str']

    # imaging
    def snap(self, exposure_time=None, fmt='fits', ret='array'):
        """Take an image and return something that depends on the arguments

        Parameters
        ----------
        exposure_time : `str`, `numbers.Number`, or `astropy.units.Quantity`
            something process_exposure_time can turn into the format expected
            by the server.  See help(andor.process_exposure_time).
        fmt : `str`, {'fits', 'jpg', 'png'}, optional
            the format to retrieve the image as.
            If fits, the ret parameter is used, otherwise it is ignored.
            Fit images are captured with 16-bit precision, other options are 8-bit.
        ret : `str`, {'array', 'hdu', 'file'}, optional
            Only used if fmt='fits'.
            If array, returns a numpy array
            If hdu, returns an astropy.io.fits.HDU object.  The user is
            responsible for closing it when finished.

        Returns
        -------
        `numpy.ndarray` or `astropy.io.fits.HDU`
            either an array holding the image data as uint8 or uint16,
            or an HDU object. Users must close the HDU object.

        """
        if exposure_time is None:
            # not given, do not update
            exposure_time = ""

        exposure_time = proces_exposure_time(exposure_time)

        fmt = fmt.lower()
        params = {'exposureTime': exposure_time, 'fmt': fmt}
        resp = requests.get(self.addr + "/image", params=params)
        raise_err(resp)
        if fmt == 'fits':
            if ret == 'file':
                return resp.content

            hdu = fits.open(BytesIO(resp.content))
            if ret == 'array':
                ary = hdu[0].data
                hdu.close()
                return ary
            else:
                return hdu
        else:
            return imread(resp.content, format=fmt)
