
import numpy as np
from scipy import signal
import pandas as pd

import pymotor.files as files
import pymotor.plots as plots
from pymotor.conversions import *

class Profile:

    def _gen_deriv(self, data, fs, init=0):

        tablen = len(data)
        deriv_tab = np.empty(tablen)
        last = np.float(init)

        i = 0
        for sample in data:
            deriv_tab[i] = np.float((sample - last) * fs)
            last = np.float(sample)
            i += 1

        return deriv_tab

    def _gen_intgrl(self, data, fs, init=0):

        tablen = len(data)
        intgrl_tab = np.empty(tablen)
        intgrl_val = np.float(init)

        i = 0
        for sample in data:
            intgrl_val += np.float(sample / fs)
            intgrl_tab[i] = intgrl_val
            i += 1

        return intgrl_tab

    def save(self, filename):
        files._save((self.settings, self.stats, self.profile), filename)    

    def load(self, filename):
        (self.settings, self.stats, self.profile) = files._load(filename)    

    def html(self, filename):
        files._html(self.profile, filename)

    def csv(self, filename):
        files._csv(self.profile, filename)

    def xlsx(self, filename):
        files._xlsx(self.profile, filename)

    def print(self, filename=None):

        profile_str = "\n[i] Profile Data Table\n\n"
        profile_str += self.profile.to_string() + '\n'     

        settings_str = "\n[i] Profile Settings\n\n"
        for key, value in self.settings.items():
            settings_str += key + ': ' + str(value) + '\n'
    
        stats_str = "\n[i] Profile Stats\n\n"
        for key, value in self.stats.items():
            stats_str += key + ': ' + str(value) + '\n'
                
        if filename:
            files._txt((settings_str + stats_str + profile_str), filename)
        else:
            print(profile_str + settings_str + stats_str)

    def drop_profile(self):
        del self.profile


class LinearMotion(Profile):

    def __init__(self,
        settings=None,
        fs = 1000,
        max_velocity = 1,
        acc_mode = 'time',
        acc_value = 1,
        acc_smooth = True,
        con_mode = 'time',
        con_value = 1,
        dec_mode = 'time',
        dec_value = 1,
        dec_smooth = True,
        ):

        if settings is None:
            self.settings = {
                'fs': fs,
                'max_velocity': max_velocity,
                'acc_mode': acc_mode,
                'acc_value': acc_value,
                'acc_smooth': acc_smooth,
                'con_mode': con_mode,
                'con_value': con_value,
                'dec_mode': dec_mode,
                'dec_value': dec_value,
                'dec_smooth': dec_smooth,
                }
        else:
            self.settings = settings

        self.generate()

    def generate(self):
        (self.profile, self.stats) = self._gen_linpro(self.settings)

    def plot(self, 
        filename=None,
        plot_title='Linear Motion Profile',
        t_label='Time (s)',
        x_label='Distance (m)',
        v_label='Velocity (m/s)',
        a_label='Acceleration (m/s^2)'
        ):

        df = self.profile[['t', 'a', 'v', 'x']]
        df = df.rename(columns={'t': t_label, 'a': a_label, 'v': v_label, 'x': x_label})
        plots._plot_df(df, plot_title=plot_title, filename=filename)

    def _gen_x_from_v(self, v, fs, x0=0):
        return self._gen_intgrl(v, fs, x0)

    def _gen_v_from_a(self, a, fs, v0=0):
        return self._gen_intgrl(a, fs, v0)

    def _gen_v_from_x(self, x, fs, x0=0):
        return self._gen_deriv(x, fs, x0)

    def _gen_a_from_v(self, v, fs, v0=0):
        return self._gen_deriv(v, fs, v0)

    def _gen_t_from_v(self, v, fs):
        t = np.arange(len(v), dtype='float')
        t = t / fs
        return t

    def _get_t_from_vmax_and_x(self, v, x):
        return (2 * x) / v

    def _get_t_from_vcon_and_x(self, v, x):
        return x / v

    def _get_t_from_vmax_and_a(self, v, a):
        return v / a

    def _gen_acc_from_v_and_t(self, v1, t1, fs, smooth):

        tablen = np.int(t1 * fs)

        if smooth is True:
            v = signal.get_window('hann', tablen * 2)
        else:
            v = signal.get_window('triang', tablen * 2)

        v = v[:tablen]
        v = v * v1
        x = self._gen_x_from_v(v, fs)
        a = self._gen_a_from_v(v, fs)
        t = self._gen_t_from_v(v, fs)

        profile = pd.DataFrame({'t': t, 'x': x, 'v': v, 'a': a})

        return profile

    def _gen_con_from_v_and_t(self, v1, t1, x0, fs):

        v1 = np.float(v1)
        t1 = np.float(t1)
        tablen = np.int(t1 * fs)

        v = np.empty(tablen, dtype='float')
        v.fill(v1)
        
        x = self._gen_x_from_v(v, fs=fs, x0=x0)
        a = np.zeros(tablen, dtype='float')
        t = self._gen_t_from_v(v, fs)
             
        profile = pd.DataFrame({'t': t, 'x': x, 'v': v, 'a': a})

        return profile

    def _gen_dec_from_v_and_t(self, v1, t1, v0, x0, fs, smooth):

        tablen = np.int(t1 * fs)

        if smooth is True:
            v = signal.get_window('hann', tablen * 2)
        else:
            v = signal.get_window('triang', tablen * 2)

        v = v[tablen:]
        v = v * v1

        x = self._gen_x_from_v(v, fs, x0)
        a = self._gen_a_from_v(v, fs, v0)
        t = self._gen_t_from_v(v, fs)
             
        profile = pd.DataFrame({'t': t, 'x': x, 'v': v, 'a': a})

        return profile

    def _gen_linpro(self, settings):

        fs = settings['fs']
        max_velocity = settings['max_velocity']
        acc_mode = settings['acc_mode']
        acc_value = settings['acc_value']
        con_mode = settings['con_mode']
        con_value = settings['con_value']
        dec_mode = settings['dec_mode']
        dec_value = settings['dec_value']

        if settings['acc_smooth'] is None or settings['acc_smooth'] is False:
            acc_smooth = False
        else:
            acc_smooth = True
        
        if settings['dec_smooth'] is None or settings['dec_smooth'] is False:
            dec_smooth = False
        else:
            dec_smooth = True

        if acc_mode == 'distance':
            acc_t1 = self._get_t_from_vmax_and_x(max_velocity, acc_value)
        elif acc_mode == 'acceleration':
            acc_t1 = self._get_t_from_vmax_and_a(max_velocity, acc_value)
        elif acc_mode == 'time':
            acc_t1 = acc_value
        else:
            raise ValueError("Acceptable input for acc_mode is 'distance', 'time', or 'acceleration'.")    

        if con_mode == 'distance':
            con_t1 = self._get_t_from_vcon_and_x(max_velocity, con_value)
        elif con_mode == 'time':
            con_t1 = con_value
        else:
            raise ValueError("Acceptable input for con_mode is 'distance' or 'time'.")

        if dec_mode == 'distance':
            dec_t1 = self._get_t_from_vmax_and_x(max_velocity, dec_value)
        elif dec_mode == 'acceleration':
            dec_t1 = self._get_t_from_vmax_and_a(max_velocity, dec_value)
        elif dec_mode == 'time':
            dec_t1 = dec_value
        else:
            raise ValueError("Acceptable input for dec_mode is 'distance', 'time', or 'acceleration'.")

        acc_profile = self._gen_acc_from_v_and_t(v1=max_velocity, t1=acc_t1, smooth=acc_smooth, fs=fs)
        con_profile = self._gen_con_from_v_and_t(v1=max_velocity, t1=con_t1, x0=acc_profile['x'].iloc[-1], fs=fs)
        dec_profile = self._gen_dec_from_v_and_t(v1=max_velocity, t1=dec_t1, v0=con_profile['v'].iloc[-1], x0=con_profile['x'].iloc[-1], smooth=dec_smooth, fs=fs)
        
        profile = pd.concat([acc_profile, con_profile, dec_profile], ignore_index=True)
        
        t = np.arange(profile['x'].size)
        t = t / fs
        t = pd.Series(t)
        profile['t'] = t

        stats = {
            'acc_size': acc_profile['x'].size,
            'acc_a_max': acc_profile['a'].max(),
            'acc_a_mean': acc_profile['a'].mean(),
            'acc_t': acc_profile['x'].size / fs,
            'acc_x': acc_profile['x'].ptp(),
            'con_size': con_profile['x'].size,
            'con_t': con_profile['x'].size / fs,
            'con_x': con_profile['x'].ptp(),
            'dec_size': dec_profile['x'].size,
            'dec_a_min': dec_profile['a'].min(),
            'dec_a_mean': dec_profile['a'].mean(),
            'dec_t': dec_profile['x'].size / fs,
            'dec_x': dec_profile['x'].ptp(),
            }

        return (profile, stats)


class LinearForce(Profile):

    def __init__(self, settings, linear_motion_object):

        self.settings = settings
        self.lm = linear_motion_object
        self.generate()

    def generate(self):

        self.profile = self.lm.profile
        self.lm.drop_profile()
        
        self.stats = {}
        self._calc_force_constants()

        f_series = self.profile['a'].copy()
        f_series = f_series.apply(self._get_force)
        self.profile['f'] = f_series

    def plot(self, 
        filename=None,
        plot_title='Required Force',
        t_label='Time (s)',
        v_label='Velocity (m/s)',
        f_label='Force (N)',
        ):

        df = self.profile[['t', 'f', 'v']]
        df = df.rename(columns={'t': t_label, 'f': f_label, 'v': v_label})
        plots._plot_df(df, plot_title=plot_title, filename=filename, height=6.0)

    def _calc_force_constants(self):

        moving_mass = self.settings['moving_mass']
        f_preload = self.settings['preload_force']
        incline = self.settings['incline_angle']
        friction_coef = self.settings['friction_coef']
        gravity = self.settings['gravity']
        sf_and_eff = self.settings['safety_factor'] / self.settings['efficiency']
        
        f_incline = moving_mass * gravity * np.sin(np.radians(incline))
        f_friction = friction_coef * moving_mass * gravity * np.cos(np.radians(incline))
        f_constant = f_preload + f_incline + f_friction

        self._f_scale = sf_and_eff * moving_mass 
        self._f_offset = sf_and_eff * f_constant

        self.stats['f_incline'] = f_incline
        self.stats['f_friction'] = f_friction
        self.stats['f_constant'] = f_constant

    def _get_force(self, a):
        return a * self._f_scale + self._f_offset


class AngularTorque(Profile):

    def __init__(self, linear_force_object, motor, coupler, gear, drivetrain):
        self.lf = linear_force_object
        self.motor = motor
        self.coupler = coupler
        self.gear = gear
        self.drivetrain = drivetrain
        self.generate()

    def generate(self):
        
        self.profile = self.lf.profile
        self.lf.drop_profile()
        
        self.settings = {}
        self.settings['safety_factor'] = self.lf.settings['safety_factor']

        self.stats = {}
        self._calc_torque_constants()

        revs_series = self.profile['x'].copy()
        self.profile['revs'] = revs_series.apply(self._get_revs_from_x)

        hz_series = self.profile['v'].copy()
        self.profile['hz'] = hz_series.apply(self._get_hz_from_v)
        
        hzps_series = self.profile['a'].copy()
        self.profile['hzps'] = hzps_series.apply(self._get_hzps_from_a)

        tau_rotating_series = self.profile['hzps'].copy()        
        self.profile['tau_rotating'] = tau_rotating_series.apply(self._get_tau_rotating_from_hzps)

        tau_linear_series = self.profile['f'].copy()        
        self.profile['tau_linear'] = tau_linear_series.apply(self._get_tau_linear_from_f)
        
        self.profile['tau'] = self.profile['tau_rotating'] + self.profile['tau_linear']

        tau_motor_series = self.profile['hz'].copy()
        self.profile['tau_motor'] = tau_motor_series.apply(self._get_tau_motor_from_hz)

    def plot(self, 
        filename=None,
        plot_title='Required (Black) and Available (Red) Torque',
        t_label='Time (s)',
        hz_label='Velocity (Hz)',
        tau_label='Torque (N*m)',
        ):

        df = self.profile[['t', 'tau', 'hz']]
        df = df.rename(columns={'t': t_label, 'tau': tau_label, 'hz': hz_label})
        series = self.profile['tau_motor']
        plots._plot_df_dual(df, series, plot_title=plot_title, filename=filename, height=6.0)

    def _calc_torque_constants(self):

        j_linear = self.lf.settings['moving_mass'] / (2 * np.pi * self.drivetrain.pitch)**2
        j_in = self.coupler.j + self.gear.j_in
        j_out = self.gear.j_out + self.drivetrain.j + j_linear
        j_load = j_in + j_out / self.gear.ratio**2
        j_ratio = j_load / self.motor.j
        j_rotating = self.motor.j + j_in + (self.gear.j_out + self.drivetrain.j) / self.gear.ratio**2

        self._tau_rotating_scale = 2.0 * np.pi * j_rotating * self.settings['safety_factor']
        self._tau_linear_scale = self.drivetrain.lead / (2.0 * np.pi * self.gear.ratio)
        self._xva_scale = self.drivetrain.pitch * self.gear.ratio

        self.stats['drivetrain_type'] = self.drivetrain.type
        self.stats['gear_ratio'] = self.gear.ratio
        self.stats['j_motor'] = self.motor.j
        self.stats['j_coupler'] = self.coupler.j
        self.stats['j_gear_in'] = self.gear.j_in
        self.stats['j_gear_out'] = self.gear.j_out
        self.stats['j_drivetrain'] = self.drivetrain.j
        self.stats['j_linear'] = j_linear
        self.stats['j_in'] = j_in
        self.stats['j_out'] = j_out
        self.stats['j_load'] = j_load
        self.stats['j_ratio'] = j_ratio
        self.stats['j_rotating'] = j_rotating

    def _get_revs_from_x(self, x):
        return x * self._xva_scale
    
    def _get_hz_from_v(self, v):
        return v * self._xva_scale

    def _get_hzps_from_a(self, a):
        return a * self._xva_scale

    def _get_tau_rotating_from_hzps(self, hzps):
        return hzps * self._tau_rotating_scale

    def _get_tau_linear_from_f(self, f):
        return f * self._tau_linear_scale

    def _get_tau_motor_from_hz(self, hz):
        return self.motor.tau(hz) 
