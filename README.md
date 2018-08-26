# PyMotor

## Overview

This is about the app.

## Development Status

PyMotor is being developed with Python 3.7 using packages described in requirements.txt.

**This is Alpha phase software.** This means that features and usage are not fixed, the documentation is most likely incomplete, and there may be bugs.

Some versions of this package are uploaded to pypi.org and can be installed, at your own risk, like this:

``` python
$ pip install pymotor
```

## Physics Equations

The math used to calculate force, inertia and torque is shown below. Note that angular velocity and angular acceleration in the equations below are in rad/s and rad/s<sup>2</sup>, respectively. Internally, the software stores these values as Hz and Hz/s. 

## Physical Units

The native physical units used by the package are shown in the table below. Functions in the module conversions.py are provided so parameters can be entered in other units.

Parameter | Internal Symbol | Unit
--|--|--
Time | t | s
Length | x | m
Linear Velocity | v | m/s
Linear Acceleration | a | m/s<sup>2</sup>
Force | f | N
Rotations | revs | Revolutions
Angular Velocity | hz | Hz
Angular Acceleration | hzps | Hz/s
Torque | tau | N*m
Moment of Inertia | j | kg*m<sup>2</sup>

## Usage

### Creating a Linear Motion Profile

``` python
import pymotor as pm

lm_settings = {
    'fs': 100000.0,
    'max_velocity': pm.ipm(90),
    'acc_mode': 'X',
    'acc_value': pm.inch(.1), 
    'acc_smooth': True,
    'con_mode': 'X',
    'con_value': pm.inch(.05),
    'dec_mode': 'X',
    'dec_value': pm.inch(.1),
    'dec_smooth': True,
}

lm = pm.LinearMotion(lm_settings)
lm.plot()
```

### Converting to a Linear Force Profile

``` python
lf_settings = {
    'safety_factor': 2,
    'moving_mass': 10,
    'preload_force': 0.1,
    'efficiency': 0.9,
    'incline_angle': 0,
    'friction_coef': 0.1,
    'gravity': 9.8,
}

lf = pm.LinearForce(lf_settings, lm)
lf.plot()
```

### Defining a Motor Object

Motor objects contain torque curve and moment of inertia data. The method Motor.tau(hz) returns an interpolated torque value for a given angular velocity, which is used by AngularTorque objects to plot available motor torque vs required torque. Motor.plot() generates a plot of the torque curve which can be used for verification.

The curve_hz list defines the X axis values of the curve. The values must be positive, unique, and ascending.

The curve_tau list defines the Y axis values of the curve. The values must be positive. 

``` python
curve_hz = [
    0, 
    pm.rpm(300), 
    pm.rpm(600),
    pm.rpm(900),
    pm.rpm(1200),
    pm.rpm(1500),
    pm.rpm(1800)
]

curve_tau = [
    2.5,
    2.2,
    1.3,
    0.9,
    0.7,
    0.6,
    0.5
]

j = pm.gcm2(460)

motor = pm.Motor(curve_hz=curve_hz, curve_tau=curve_tau, j=j)
motor.plot()
```

### Defining Other Drivetrain Objects

``` python
coupler = pm.Coupler(j=pm.gcm2(460))
gear = pm.Gear(ratio=0.25, j_in=pm.gcm2(460), j_out=pm.gcm2(460))
screw = pm.Screw(lead=pm.inch(.05), j=pm.gcm2(460))
```

### Generating a Torque Profile

``` python
at = pm.AngularTorque(lf, motor=motor, coupler=coupler, gear=gear, drivetrain=screw)
at.plot()
```
