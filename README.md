# Thorlabs (http) clients

This repository contains clients for Thorlabs hardware, currently just the ITC4000 laser diode controller in various languages.

Point of contact: [Brandon Dube (383D)](mailto:brandon.dube@jpl.nasa.gov)

# Python example

This example shows how to manipulate the controller from python (3.6+).

To install:
```sh
pip install https://github.jpl.nasa.gov/HCIT/client-thorlabs
```

To use:

```python
import thorlabs

laser = thorlabs.ITC4000('malady.jpl.nasa.gov:8001')

# is the diode emitting light?
laser.emission()
>>> True

# turn it off
laser.emission(False)

# back on
laser.emission(True)

# set the electrical current setpoint in mA
laser.current(50)

# check that the value stuck
laser.current()
>>> 50

# using astropy
from astropy import units as u

laser.convention = 'units'
setpt = 100 * u.mA
laser.current(setpt)
```


# Matlab example

```matlab

% first create a struct with the controller URL
s = struct();
s.ControllerURL = 'http://malady.jpl.nasa.gov:8001'

% is the diode emitting light?
itcGetEmission(s)
>>> 1

% turn it off
itcSetEmission(s, false)

% set the current in mA
itcSetCurrent(s, 50)

% get it
itcGetCurrent(s)
>>> 50
```
