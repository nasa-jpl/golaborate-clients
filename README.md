# Thermocube (http) clients

This repository contains clients for SolidState ThermoCube chillersin various progamming languages.  To adapt the examples to your own testbed, just know the IP or name of the server you have a multiserver from `go-hcit` running at.

Point of contact: [Brandon Dube (383D)](mailto:brandon.dube@jpl.nasa.gov)

## Python example

To install:
```sh
pip install git+https://github.jpl.nasa.gov/HCIT/client-thermocube
```

To use:

```python
import thermocube

tc = thermocube.Chiller("malady:8002")

# get the temperature at the chiller output
tc.temperature
>>> 16 # Celcius

# get the temperature setpoint (C)
tc.temperature_setpoint()
>>> 16

# set the temperature setpoint (C)
tc.temperature_setpoint(15)  # going below 10 in air will probably condensation-kill what's on the cold side

tc.faults
>>> {

}
# check if the fluid is low
tc.tank_level_low
>>> False
```


## Matlab example

```matlab
% begin by making a struct for the axis, with two fields:
s = struct();
s.ControllerURL = 'http://malady:8002'
thermocubeTemp(s)
>>>   16

thermocubeGetSetpoint(s)
>>> 16

thermocubeSetSetpoint(s, 15)

thermocubeTankLevelLow(s)
>>> 0 % if 1, time to fill it back up
```
