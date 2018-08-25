
import pymotor as pm

if __name__ == '__main__':

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

    lf_settings = {
        'safety_factor': 2,
        'moving_mass': 10,
        'preload_force': 0.1,
        'efficiency': 0.9,
        'incline_angle': 0,
        'friction_coef': 0.1,
        'gravity': 9.8,
    }

    lm = pm.LinearMotion(lm_settings)
    lf = pm.LinearForce(lf_settings, lm)
    lf.plot()
    
    motor = pm.Motor()
    motor.plot()

    coupler = pm.Coupler()
    gear = pm.Gear(ratio=1.0)
    screw = pm.Screw(lead=pm.inch(.05))

    at = pm.AngularTorque(lf, motor=motor,
        coupler=coupler, gear=gear, drivetrain=screw)
    at.plot()
