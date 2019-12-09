# Andor (http) clients

This repository contains clients for Andor Neo and iXon cameras in various languages.  To adapt the examples to your own camera, just know the IP or name of the server you have an andor-http server from `go-hcit` running at.

Point of contact: [Brandon Dube (383D)](mailto:brandon.dube@jpl.nasa.gov)

## Python example

This example shows how to use the camera from python (3.6+).  All operations will
raise any exceptions encountered on the server.  Use try/catch to suppress this behavior.

To install:
```sh
pip install git+https://github.jpl.nasa.gov/HCIT/client-andor
```

### Basic Usage
```python
import andor

cam = andor.SDK3Cam('malady.jpl.nasa.gov:8000') # <- replace this URL stub for your own server

# poll the thermometer
cam.temperature
>>> 26.54  # Celcius

# get a frame as a uint16 array, for when you don't care about the metadata or saving the file
ary = cam.snap(fmt='fits', ret='array')
ary.shape, ary.dtype
>>> ((2160, 2560), dtype('uint16'))

# get it as an hdu, for when you care about both but don't want to touch the disk:
hdu = cam.snap(fmt='fits', ret='hdu')
hdu[0].header
>>>
SIMPLE  =                    T / primary HDU
BITPIX  =                   16 / number of bits per data pixel
NAXIS   =                    2 / number of data axes
NAXIS1  =                 2560 / length of data axis 1
NAXIS2  =                 2160 / length of data axis 2
HDRVER  = '2       '           / header version
WRAPVER =                    2 / server library code version
SDKVER  = '3.13.30034.0'       / sdk version
DRVVER  = ''                   / driver version
FIRMVER = '15.1.20.0'          / camera firmware version
METAERR = ''                   / error encountered gathering metadata
CAMMODL = 'NEO-5.5-CL3-F'      / camera model
CAMSN   = 'SCC-02529'          / camera serial number
DATE    = '2019-12-09T14:36:10' /
EXPTIME =             0.000200 / exposure time, seconds
FAN     =                    T / on (true) or off
TEMPSETP= '-30.00  '           / Temperature setpoint
TEMPSTAT= 'Stabilised'         / TEC status
TEMPER  =           -30.260000 / FPA temperature (Celcius)
AOIL    =                    1 / 1-based left pixel of the AOI
AOIT    =                    1 / 1-based top pixel of the AOI
AOIW    =                 2560 / AOI width, px
AOIH    =                 2160 / AOI height, px
BZERO   =                32768 /
BSCALE  =             1.000000 /

hdu[0].data.shape, hdu[0].data.dtype
>>> ((2160, 2560), dtype('uint16'))

# closing the HDU is your responsibility
hdu.close()

# cam.snap takes an exposure time as the first argument, if None it doesn't update texp.
cam.exposure_time()
>>> 2e-4 # seconds

cam.exposure_time(2e-1) # set as floating point seconds

from astropy import units as u
cam.exposure_time(20 * u.us)  # astropy quantity

cam.exposure_time('500us') # string, no space separating unit and value

```

### Advanced usage

#### Thermal monitoring and control:
```python
# get the FPA temperature - this updates each time you access it
cam.temperature
>>> -30.26

# what does the TEC think it's doing?
cam.cooling_status
>>> 'Stabilised'

# what is the setpoint?
cam.temperature_setpt()
>>> '-30.00'

# Setpoints are strings because there are discrete options in the SDK

# change it:
cam.temperature_setpt('-15.00')

# what were the options?
cam.temperature_setpt_options # these may change, updated whenever you access the property
>>> ['-15.00', '-20.00', '-25.00', '-30.00', '-35.00', '-40.00']

# you can feed these into each other:
cam.temperature_setpt(cam.temperature_setpt_options[-2])  # -30C, probably

# is the TEC on?
cam.sensor_cooling()
>>> True

# turn it off - at your own risk
cam.sensor_cooling(False)

# what about the fan?
cam.fan()
>>> True

# also at your own risk
cam.fan(False)
```

#### Low-level access to features:

```python
# see a list of features
cam.featured
>>> {'AOIBinning': 'enum',
 'AOIHBin': 'int',
 'AOIHeight': 'int',
 'AOILayout': 'enum',
 'AOILeft': 'int',
 'AOIStride': 'int',
 'AOITop': 'int',
 'AOIVBin': 'int',
 'AOIWidth': 'int',
 'AccumulatedCount': 'int',
 ...

# get a feature
cam.get_feature('FrameRate')
>>> 33.332

# set a feature
cam.set_feature('ExposureTime', 2e-3)

# get the options for a feature, enums
cam.get_feature_info('TemperatureControl')
>>> {'options': ['-15.00', '-20.00', '-25.00', '-30.00', '-35.00', '-40.00'], 'type': 'enum'}

# numerical
cam.get_feature_info('ExposureTime')
>>> {'max': 19841.549026929577, 'min': 9.23943661971831e-06, 'type': 'float'}
