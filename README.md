# Motion (http) clients

This repository contains clients for motion controllers in various languages.  To adapt the examples to your own testbed, just know the IP or name of the server you have a multiserver from `go-hcit` running at.  Aerotech Ensemble, Newport XPS, and newport ESP controllers are supported.

Point of contact: [Brandon Dube (383D)](mailto:brandon.dube@jpl.nasa.gov)

## Python example

To install:
```sh
pip install git+https://github.jpl.nasa.gov/HCIT/client-motion
```

To use:

```python
import motion

# ctl = "controller"
ctl = motion.Controller("malady:8002")

# some parameters are using defaults, this is equivalent:
ctl = motion.Controller("malady:8002", ['X', 'Y', 'Z'])

# ctl has a property for each axis,
x, y, z = ctl.X, ctl.Y, ctl.Z

# lowercase x, y, z are easy to overwrite/shadow,
# you probably shouldn't use these names.  Anyway...

# pos is the current position in millimeters.
# Each time you access it, it queries the controller and updates.
x.pos, y.pos, z.pos
>>> (3.9, 4.1, 5.2)

# you can move to an absolute position
x.move_abs(4.0563)
x.pos
>>> 4.0562567

# or make a relative adjustment
x.move_rel(1)
x.pos
>>> 5.0562552

# the velocity setpoint can be adjusted
x.velocity(10) # mm/s
x.velocity()
>>> 10 # and queried

# the software limits can be queried
x.limits
>>> {'min': 0, 'max': 210}

# the axis can be homed
x.home()

# there are also enable and disable functions,
# see the "there was an error section"
x.disable()
x.enable()
```


## Matlab example

```matlab
% begin by making a struct for the axis, with two fields:
s = struct();
s.ControllerURL = 'http://malady:8002'
s.Axis = 'X'

% get the position
motionGetPos(s)
>>> 3.9

% absolute move, mm
motionMoveAbs(s, 5)
motionGetPos(s)
>>> 5

% relative move, mm
motionMoveRel(s, 1)
motionGetPos(s)
>>> 6

% home
motionHome(s)
motionGetPos(s)
>>> 0

% enable/disable
motionGetEnabled(s)
>>> 1
motionSetEnabled(s, 0) % 0 == logical false == disable, 1 to enable

% velocity setpoints
motionSetVelocity(s, 10)
motionGetVelocity(s)
>>> 10

% limits
motionGetLimits
```

## There was an error

### bad response, OK returns %, got \#

The Ensemble controller uses the first byte in its response to indicate if things are OK or not.
The default is to use % for "OK", ! for "not understood", and "#" for error.
When you receive a # unexpectedly, it almost certainly is because the axis is disabled and you tried to interact with it.
The fix is simply:

```python
# ctl.X is the problem axis
ctl.X.enable()
ctl.X.home()
# ... go on with your day
```

You should never encounter this unless there was an << event >> on the testbed, for example a power cycle of the controller
or severe fault (such as torque limit reached, which almost certainly belies a collision).
