# Cryocon (http) clients

This repository contains clients for Cryocon temperature monitors in various languages.  To adapt the examples to your own testbed, just know the IP or name of the server you have a multiserver from `go-hcit` running at.

Point of contact: [Brandon Dube (383D)](mailto:brandon.dube@jpl.nasa.gov)

## Python example

To install:
```sh
pip install git+https://github.jpl.nasa.gov/HCIT/client-cryocon
```

To use:

```python
import cryocon

tm = cryocon.TemperatureMonitor("malady:8002")

# read a single channel, must use alphanumeric identifier
tm.read('A')
>>> 22.5123 # Celcius

# read all channels
tm.read('all')
>>> [22.5123, ...]

# this is the same as the default
tm.read()
>>> [22.5123, ...]

```
