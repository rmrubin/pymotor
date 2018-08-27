# PyMotor

## Overview

PyMotor is a tool for electric motor selection. It generates force and torque plots from linear motion profiles and physical parameters describing motors, drivetrains, and loads.

## Development Status

PyMotor is being developed with Python 3.7 using packages described in requirements.txt.

**This is Alpha phase software.** This means that features and usage are not fixed, the documentation is most likely incomplete, and there may be bugs.

Some versions of this package are uploaded to pypi.org and can be installed, at your own risk, like this:

``` bash
$ pip install pymotor
```

## Physics Equations

The math used to calculate force, inertia and torque is shown below. Note that angular velocity and angular acceleration in the equations below are in rad/s and rad/s<sup>2</sup>, respectively. Internally, the software stores these values as Hz and Hz/s. 

![Equation Image](https://raw.githubusercontent.com/rmrubin/pymotor/master/readme/equations.png)

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
Angle | incline_angle | °

## Usage

### Creating a Linear Motion Profile

Code to import the pymotor package and configure the LinearMotion object is shown below. Linear motion profiles are created from three segments: acceleration from zero, constant velocity, and deceleration to zero.

fs is F<sub>sample</sub>, or the sample rate in Hz of the generated profiles.

Acceleration and deceleration segments can be defined by their time, distance, or acceleration. The constant velocity segment can be defined by time or distance. 

If the smoothing options are set True, the acceleration and deceleration segments use Hann windows to create smoothed velocity profiles. If set False, triangular windows are used to create a trapezoidal velocity profile with constant acceleration. 

The conversion functions ipm() and inch() have been used to convert from inches/min and inches, respectively, to native units.

``` python
import pymotor as pm

lm_settings = {
    'fs': 10000.0,
    'max_velocity': pm.ipm(40),
    'acc_mode': 'time',
    'acc_value': 0.06, 
    'acc_smooth': True,
    'con_mode': 'distance',
    'con_value': pm.inch(.01),
    'dec_mode': 'acceleration',
    'dec_value': 0.25,
    'dec_smooth': False,
}

lm = pm.LinearMotion(lm_settings)
lm.plot()
```
![Motion Profile Image](https://raw.githubusercontent.com/rmrubin/pymotor/master/readme/motion.png)

### Converting to a Linear Force Profile

LinearForce objects take a settings dictionary and LinearMotion object as arguments, and generates a plot of force and velocity versus time.

The safety factor defined here is also used in the AngularTorque objects. 

``` python
lf_settings = {
    'safety_factor': 2,
    'moving_mass': 100,
    'preload_force': 0.1,
    'efficiency': 0.9,
    'incline_angle': 45,
    'friction_coef': 0.1,
    'gravity': 9.8,
}

lf = pm.LinearForce(lf_settings, lm)
lf.plot()
```
![Force Profile Image](https://raw.githubusercontent.com/rmrubin/pymotor/master/readme/force.png)

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
    pm.rpm(1800),
]

curve_tau = [
    2.5,
    2.2,
    1.3,
    0.9,
    0.7,
    0.6,
    0.5,
]

motor = pm.Motor(curve_hz=curve_hz, curve_tau=curve_tau, j=pm.gcm2(460))
motor.plot()
```
![Motor Torque Curve Image](https://raw.githubusercontent.com/rmrubin/pymotor/master/readme/motor.png)

### Defining Other Drivetrain Objects

Other necessary drivetrain objects are created in the following code. Gear ratios, drive screw lead, and moments of inertia are used in the torque generation process. The conversion functions gcm2() and inch() have been used to convert from g*cm<sup>2</sup> and inches, respectively, to native units.

``` python
coupler = pm.Coupler(j=pm.gcm2(5))
gear = pm.Gear(ratio=0.5, j_in=pm.gcm2(10), j_out=pm.gcm2(15))
screw = pm.Screw(lead=pm.inch(.05), j=pm.gcm2(20))
```

### Generating a Torque Profile

AngularTorque objects take LinearForce, Motor, and drivetrain objects as arguments. The generated torque profile uses the safety factor defined in the LinearForce object.

The required torque plot includes an overlay of available motor torque. The velocity profile is also plotted.

``` python
at = pm.AngularTorque(lf, motor=motor, coupler=coupler, gear=gear, drivetrain=screw)
at.plot()
```
![Torque Profile Image](https://raw.githubusercontent.com/rmrubin/pymotor/master/readme/torque.png)

## Planned Changes
- [ ] More complete conversions.py module.
- [ ] Complete functions to output profile statistics. 
- [ ] Reduction of pandas DataFrame copy operations.
- [ ] Configurable plot units.
- [ ] Stepper motor table and three-phase motor signal generation. 
