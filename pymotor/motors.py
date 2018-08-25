
from typing import List
import pandas as pd

import pymotor.files as files
import pymotor.plots as plots
from pymotor.conversions import *


class Motor:
    '''Motor objects describe a physical motor. 

    Motor.j is the moment of interia in kg*m^2.

    Motor.curve is a pandas DataFrame containing points representing the
        torque versus speed curve. 

    Motor.curve['hz'] are the angular velocities in Hz.

    Motor.curve['tau'] are the torques in N*m.

    Motor.tau(hz) returns an interpolated torque value in N*m.

    Motor.hz_min and Motor.hz_max are created at init and define the range
        for the tau method's hz argument. 

    Motor.plot(filename) creates a PNG plot of the torque curve. If the
        filename argument is not included, the plot will attempt to display
        on screen.

    Motor.d is the spindle diameter in m. 

    The following descriptive attributes are provided:
        Motor.name
        Motor.manufacturer
        Motor.description
    '''
    def __init__(self,
        name: str ='PL23HSAP4150 60VDC 1.5A',
        manufacturer: str = 'Moons',
        description: str = 'Stepper NEMA23',
        curve_hz: List[float] = [0, rpm(300), rpm(600), rpm(900), rpm(1200), rpm(1500), rpm(1800)],
        curve_tau: List[float] = [2.5, 2.2, 1.3, 0.9, 0.7, 0.6, 0.5],
        j: float = gcm2(460),
        d_out: float = inch(0.25),
        ):

        self.name = str(name)
        self.manufacturer = str(manufacturer)
        self.description = str(description)

        if self._j_ok(j):
            self.j = j
        else:
            raise ValueError("j (kg*m^2) cannot be negative.")

        if self._d_out_ok(d_out):
            self.d_out = d_out
        else:
            raise ValueError("d_out (m) must be positive.")

        if self._curve_hz_ok(curve_hz) and self._curve_tau_ok(curve_tau):
            if len(curve_hz) == len(curve_tau):
                self.curve = pd.DataFrame(data={'hz': curve_hz, 'tau': curve_tau})
                self.hz_min = self.curve['hz'].min()
                self.hz_max = self.curve['hz'].max()
            else:
                raise ValueError("curve_hz and curve_tau lists must be the same length.")        
        else:
            raise ValueError("curve_hz (Hz) and curve_tau (N*m) values must be positive. curve_hz values must be ascending.")

            
    def tau(self, hz: float) -> float:
        '''Given speed (Hz) returns interpolated tau (N*m).'''
        if self._hz_range_ok(hz):
            for i in range(self.curve['hz'].size):
                if hz <= self.curve['hz'].iloc[i + 1]:
                    hz1 = self.curve['hz'].iloc[i]
                    hz2 = self.curve['hz'].iloc[i + 1]
                    tau1 = self.curve['tau'].iloc[i]
                    tau2 = self.curve['tau'].iloc[i + 1]
                    break
            return (((hz - hz1) * (tau2 - tau1)) / (hz2 - hz1)) + tau1
        else:
            raise ValueError("hz must be between Motor.hz_min and Motor.hz_max.")


    def plot(self, 
        filename: str = None,
        plot_title: str = 'Motor Torque Curve',
        hz_label: str = 'Angular Velocity (Hz)',
        tau_label: str = 'Torque (N*m)',
        ):
        '''Plots torque curve data to PNG image, or screen if filename is not specified.'''
        df = self.curve[['hz', 'tau']]
        df = df.rename(columns={'hz': hz_label, 'tau': tau_label})
        plots._plot_df(df, plot_title=plot_title, filename=filename, height=3, width=5)


    def save(self, filename: str):
        '''Save Motor object data to file.'''
        save_data = (
            self.j,
            self.curve,
            self.hz_min,
            self.hz_max,
            self.d_out,
            self.name,
            self.manufacturer,
            self.description,
        )        
        files._save(save_data, filename)


    def load(self, filename: str):
        '''Load Motor object data from file.'''
        load_data = files._load(filename)
        (
            self.j,
            self.curve,
            self.hz_min,
            self.hz_max,
            self.d_out,
            self.name,
            self.manufacturer,
            self.description,
        ) = load_data


    def _j_ok(self, j: float) -> bool:
        '''True if j positive.'''
        if j < 0.0:
            return False
        return True


    def _d_out_ok(self, d_out: float) -> bool:
        '''True if j positive.'''
        if d_out <= 0.0:
            return False
        return True


    def _curve_hz_ok(self, curve_hz: List[float]) -> bool:
        '''True if values are ascending and positive.'''
        for i in range(len(curve_hz)):
            if curve_hz[i] < 0.0:
                return False
            if i > 0:
                if curve_hz[i] <= curve_hz[i - 1]:
                    return False
        return True


    def _curve_tau_ok(self, curve_hz: List[float]) -> bool:
        '''True if values are positive.'''
        for i in range(len(curve_hz)):
            if curve_hz[i] < 0.0:
                return False
        return True


    def _hz_range_ok(self, hz: float) -> bool:
        '''True if hz between Motor.hz_min and Motor.hz_max.'''
        if hz < self.hz_min or hz > self.hz_max:
            return False
        return True
