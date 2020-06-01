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

from golab_common import raise_err, niceaddr


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


class Recorder:
    """Recoder is an interface to the autorecorder on the server, which saves every FITS file to disk."""

    def __init__(self, addr):
        """Create a new Recorder instance.

        Parameters
        ----------
        addr : `str`
            the URL the go-hcit server is running on, with any stem for the recorder.
            The route addr/autowrite should exist.

        """
        self.addr = addr

    def root(self, srvpath=None):
        """Get (srvpath=None) or set the root folder to backup to.

        Parameters
        ----------
        srvpath : `str`
            path *on the server* to store backups in

        Returns
        -------
        `str`
            the path that files are saved to

        """
        url = f'{self.addr}/autowrite/root'
        if srvpath is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['str']
        else:
            payload = {'str': srvpath}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    def prefix(self, string=None):
        """Get (string=None) or set the filename prefix to backup to.

        Parameters
        ----------
        string : `str`
            prefix to use when naming files, prefix00000x.fits

        Returns
        -------
        `str`
            the prefix that is currently in use

        """
        url = f'{self.addr}/autowrite/prefix'
        if string is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['str']
        else:
            payload = {'str': string}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    def enabled(self, boolean=None):
        """Enable/Disable the recorder, or check if it is enabled.

        Parameters
        ----------
        boolean : `bool`
            if None, get.  Else set.

        Returns
        -------
        `bool`
            whether the recorder is enabled

        """
        url = f'{self.addr}/autowrite/enabled'
        if boolean is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            payload = {'bool': boolean}
            resp = requests.post(url, json=payload)
            raise_err(resp)


class Camera:
    """Camera is a wrapper around a camera from andor SDK3 v3 through go-hcit."""

    def __init__(self, addr, time_convention='float'):
        """Create a new Camera instance.

        Parameters
        ----------
        addr : `str`
            "root" address of the go-hcit andor server, one level above the
            "/image" route.  Must incude port.  startswith http not needed.
        time_convention : `str`, {'float', 'astropy'}
            either float (exposure time returns as floating point seconds) or
            astropy (exposure time returns as astropy quantity)

        """
        self.addr = niceaddr(addr)
        self.time_convention = time_convention
        self.recorder = Recorder(addr)

    # generics
    @property
    def features(self):
        """Dictionary mapping feature names to strings representing their types."""
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
        elif isinstance(value, bool):
            key = 'bool'
        elif isinstance(value, float):
            key = 'f64'
        elif isinstance(value, int):
            key = 'int'

        payload = {key: value}
        resp = requests.post(url, json=payload)
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

    def get_feature_info(self, feature):
        """Get the type and allowable range for a feature on the camera.

        Parameters
        ----------
        feature : `str`
            a feature that is a valid key to self.features

        Returns
        -------
        `dict`
            with keys `type`.  May also include keys `min` and `max` for
            numerical features, or a key of "options" for enums, and "maxLength"
            for strings

        """
        url = f'{self.addr}/feature/{feature}/options'
        resp = requests.get(url)
        raise_err(resp)
        return resp.json()

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

    def aoi(self, dict_=None):
        """Get or set the area of interest (AoI).  If dict_=None, gets.  If dict_!=None, sets.

        Parameters
        ----------
        dict_ : `dict`
            dictionary with keys left, top, width, height.
            Not all keys are needed.  Partial updates are allowed.


        Returns
        -------
        dict_ : `dict`
            dictionary with keys left, top, width, height.

        """
        url = f'{self.addr}/aoi'
        if dict_ is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()
        else:
            resp = requests.post(url, json=dict_)
            raise_err(resp)

    def binning(self, fctr=None):
        """Get or set the on-camera binning.

        Parameters
        ----------
        fctr : `int`
            binning to apply, symmetric in H and V.

        Returns
        -------
        `int`
            the binning

        """
        url = f'{self.addr}/binning'
        if fctr is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['h']  # keys are h,v but we are explicitly symmetric

        else:
            payload = {'h': fctr, 'v': fctr}
            resp = requests.post(url, json=payload)
            raise_err(resp)

    # thermal
    def fan(self, on=None):
        """Turn the fan on or off (on != None), or checks if it's on (true).

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
            resp = requests.post(url, json={'bool': on})
            raise_err(resp)
            return

    def sensor_cooling(self, on=None):
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
            resp = requests.post(url, json={'bool': on})
            raise_err(resp)
            return

    @property
    def temperature(self):
        """Current sensor temperature in Celcius."""
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
            resp = requests.post(url, json={'str': valueS})
            raise_err(resp)
            return

    @property
    def temperature_setpt_options(self):
        """Currently allowed temperature setpoint options."""
        resp = requests.get(self.addr + '/temperature-setpoint-options')
        raise_err(resp)
        return resp.json()

    @property
    def cooling_status(self):
        """Current cooling status."""
        resp = requests.get(self.addr + "/temperature-status")
        raise_err(resp)
        return resp.json()['str']

    # imaging

    def snap(self, exposure_time=None, fmt='fits', ret='array'):
        """Take an image and return something that depends on the arguments.

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

    def burst(self, frames, fps, serverSpool=0):
        """Take a burst of images, returned as a generator of 2D arrays.

        Parameters
        ----------
        `frames` : `int`
            number of frames to take in the sequence
        `fps` : `float`
            framerate to use.  Ensure it is supported by the camera
        serverSpool : `int`
            size of the spool (in frames) to use on the server to buffer,
            if the client can't keep up.  If Zero, the spool size is set to
            frames*fps, which may cause out of memory errors.

        Returns
        -------
        `generator`
            a generator yielding 2D ndarrays.  An exception may be raised while
            iterating it if one is encountered on the server.

        """
        payload = {
            'fps': fps,
            'frames': frames,
            'spool': serverSpool
        }
        resp = requests.post(f'{self.addr}/burst/setup', json=payload)
        raise_err(resp)
        for _ in range(frames):
            resp = requests.get(f'{self.addr}/burst/frame')
            raise_err(resp)
            hdu = fits.open(BytesIO(resp.content))
            yield hdu[0].data

    # this is EMCCD stuff
    def em_gain(self, fctr=None):
        """Get or set the EM gain.  Get if fctr=None, else Set.

        Parameters
        ----------
        fctr : `int`
            gain factor, [0,300] if self.em_mode() != 'Advanced', else [0,1000].

        Returns
        -------
        `int`
            the EM gain

        """
        url = f'{self.addr}/em-gain'
        if fctr is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['int']
        else:
            resp = requests.post(url, json={'int': fctr})
            raise_err(resp)

    def em_gain_mode(self, mode=None):
        """Get or set the EM gain mode.  Get if mode=None, else Set.

        Parameters
        ----------
        mode : `str`, {'Advanced'}
            em gain mode

        Returns
        -------
        `str`
            the current EM gain mode

        """
        url = f'{self.addr}/em-gain-mode'
        if mode is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['str']
        else:
            resp = requests.post(url, json={'str': mode})
            raise_err(resp)

    @property
    def em_gain_range(self):
        """Min and max values for EM gain in the current configuration."""
        resp = requests.get(f'{self.addr}/em-gain-range')
        raise_err(resp)
        return resp.json()

    # this is shutter control
    def shutter(self, open=None):
        """Get or set the EM gain mode.  Get if mode=None, else Set.

        Parameters
        ----------
        mode : `str`, {'Advanced'}
            em gain mode

        Returns
        -------
        `str`
            the current EM gain mode

        """
        url = f'{self.addr}/shutter'
        if open is None:
            resp = requests.get(url)
            raise_err(resp)
            return resp.json()['bool']
        else:
            resp = requests.post(url, json={'bool': open})
            raise_err(resp)


SDK3Cam = Camera


class EMCCD(Camera):
    """Subclass of Camera that forbids excessively cold temperatures."""

    def temperature_setpt(self, valueS=None):
        """Get (valueS=None) or set the current temperature setpoint.

        Parameters
        ----------
        valueS : `str`, optional
            a string representing a temperature.  Must be in self.temperature_setpt_options.

        Returns
        -------
        `str`
            the current temperature setpoint, in Celcius

        """
        if valueS is not None:
            f = float(valueS)
            if f < -25:
                raise ValueError("it's forbidden to set the TEC cooler than this.")

        return super().temeprature_setpt(valueS)
