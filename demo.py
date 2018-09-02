#!/usr/bin/env python3

if __name__ == '__main__':

    import pymotor as pm

    lm_settings = {
        'fs': 10000.0,
        'max_velocity': pm.ipm(40),
        'acc_mode': 'time',
        'acc_value': 0.06, 
        'acc_smooth': True,
        'con_mode': 'distance',
        'con_value': pm.inch(0.02),
        'dec_mode': 'acceleration',
        'dec_value': 0.25,
        'dec_smooth': False,
    }

    lm = pm.LinearMotion(lm_settings)
    lm.plot()

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

    coupler = pm.Coupler(j=pm.gcm2(5))
    gear = pm.Gear(ratio=2, j_in=pm.gcm2(10), j_out=pm.gcm2(15))
    screw = pm.Screw(lead=pm.inch(.05), j=pm.gcm2(20))

    at = pm.AngularTorque(lf, motor=motor,
        coupler=coupler, gear=gear, drivetrain=screw)
    at.plot()
