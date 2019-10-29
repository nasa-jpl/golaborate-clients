# NKT clients

This repository contains clients for the NKT SuperK lasers in various languages.  To adapt the examples to your own SuperK, just know the IP or name of the server you have a SuperK-serving http server from `go-hcit` running at.  *We ask that you do not* run the examples as this would disturb a testbed.

Point of contact: [Brandon Dube (383D)](mailto:brandon.dube@jpl.nasa.gov).

## Python example

This example shows how to use the lasers from python.  All operations will raise any exceptions encountered on the server.  Use try/catch to suppress this behavior.

To install:

```bash
pip install git+https://github.jpl.nasa.gov/HCIT/client-nkt
```

To use:

```python
import nkt

# make a new SuperK object.  http:// will be prepended automatically.
sk = nkt.SuperK('misery.jpl.nasa.gov:8080/omc/nkt') # <- replace this URL stub for your own server.

# get the power level
print(sk.power)
>>> 40.0

# set the power level
sk.power(40)

# is the laser on?
sk.emission()
>>> True

# turn it off
sk.emission(False)

# on again
sk.emission(True)

# how is the VARIA configured?
sk.center_bandwidth()
>>> {'center': 575, 'bandwidth': 64}

# change the wavelength
sk.center_bandwidth(600, 20)


# adjust the VARIA ND if one is present
sk.ND(10)

# see the value of the ND
sk.ND()

# are there errors on the main module?
sk.status_main()
>>> {
  "CRC error on startup (possible module address conflict)": false,
  "Clock battery low voltage": false,
  "Emission on": false,
  "Inlet temperature out of range": false,
  "Interlock loop open": false,
  "Interlock relays off": false,
  "Interlock supply voltage low (possible short circuit)": false,
  "Log error code present": false,
  "Output control signal low": false,
  "Supply voltage low": false,
  "System error code present": false
}

# on the VARIA
sk.status_varia()
>>> {
  "Error code present": false,
  "Filter 1 moving": false,
  "Filter 2 moving": false,
  "Filter 3 moving": false,
  "Interlock loop in": false,
  "Interlock loop out": false,
  "Interlock off": false,
  "Shutter sensor 1": true,
  "Shutter sensor 2": false,
  "Supply voltage low": false
}

# get help
help(sk)
```

## Matlab example

To "install":

```matlab
addpath('../matlab/nkt')
```

```matlab
% yourStruct could be a testbed struct, config, whatever.
% We just look for this one field.
s = struct()
s.NKTSuperKRoot = "http://misery.jpl.nasa.gov:8080/omc/nkt"

# get the power level
nktPowerGet(s)
>>> ans = 40.0

# set the power level
nktPowerSet(s, 40)

# is the laser on?
nktGetEmission(s)
>>> ans = 1 % logicals are 1 or 0 in matlab

# turn it off
nktEmissionOff(s)

# on again
nktEmissionOn(s)

# how is the VARIA configured?
nktCenterBandwidthGet(s)
>>> ans =
    struct with fields:

           center: 575,
        bandwidth: 64

# change the wavelength
nktCenterBandwidthSet(s, 600, 20)


# adjust the VARIA ND if one is present
nktNDSet(s, 10)

# see the value of the ND
nktNDGet(s)
>>> ans = 10.0

# are there errors on the main module?
nktMainModuleStatus(s)
>>> ans =

  struct with fields:

    CRCErrorOnStartup_possibleModuleAddressConflict_: 0
                              ClockBatteryLowVoltage: 0
                                          EmissionOn: 1
                          InletTemperatureOutOfRange: 0
                                   InterlockLoopOpen: 0
                                  InterlockRelaysOff: 0
     InterlockSupplyVoltageLow_possibleShortCircuit_: 0
                                 LogErrorCodePresent: 0
                              OutputControlSignalLow: 0
                                    SupplyVoltageLow: 0
                              SystemErrorCodePresent: 0

# on the VARIA
nktVariaStatus(s)
>>> ans =

  struct with fields:

    ErrorCodePresent: 0
       Filter1Moving: 0
       Filter2Moving: 0
       Filter3Moving: 0
     InterlockLoopIn: 0
    InterlockLoopOut: 0
        InterlockOff: 0
      ShutterSensor1: 1
      ShutterSensor2: 0
    SupplyVoltageLow: 0
```
