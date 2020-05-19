# Fluke (http) clients

This repository contains clients for Fluke DewK thermo hydrometers in various progamming languages.  To adapt the examples to your own testbed, just know the IP or name of the server you have a multiserver from `go-hcit` running at.

Point of contact: [Brandon Dube (383D)](mailto:brandon.dube@jpl.nasa.gov)

## Python example

To install:
```sh
pip install git+https://github.jpl.nasa.gov/HCIT/client-fluke
```

To use:

```python
import fluke

dk = fluke.DewK("malady:8002")

# get the temperature and humidity data, updated with each call to this function
dk.reading
>>> {
    'temp': 22.51, # Celcius
    'rh': 10.6     # relative humidity
}
```


## Matlab example

```matlab
% begin by making a struct for the axis, with two fields:
s = struct();
s.ControllerURL = 'http://malady:8002'
dewkGetTH(s)
>>>   struct with fields:

    temp: 22.2400
      rh: 30.2000
```
