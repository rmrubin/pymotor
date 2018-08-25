
import numpy as np

# Pi Constants

TWO_PI = 2.0 * np.pi
ONE_OVR_TWO_PI = 1.0 / TWO_PI

# Time Conversion Constants

SEC_PER_MIN = 60.0
MIN_PER_SEC = 1.0 / SEC_PER_MIN

MIN_PER_HOUR = 60.0
HOUR_PER_MIN = 1.0 / MIN_PER_HOUR

SEC_PER_HOUR = SEC_PER_MIN * MIN_PER_HOUR
HOUR_PER_SEC = 1.0 / SEC_PER_HOUR  

# Length Conversion Constants

M_PER_INCH = 0.0254
INCH_PER_M = 1.0 / M_PER_INCH
 
MM_PER_M = 1000.0
M_PER_MM = 1.0 / MM_PER_M

CM_PER_M = 100.0
M_PER_CM = 1.0 / CM_PER_M

# Velocity Conversion Constants

MPS_PER_IPM = MIN_PER_SEC * M_PER_INCH
IPM_PER_MPS = SEC_PER_MIN * INCH_PER_M

# Area Conversion Constants

CM2_PER_M2 = CM_PER_M * CM_PER_M
M2_PER_CM2 = 1.0 / CM2_PER_M2

MM2_PER_M2 = MM_PER_M * MM_PER_M
M2_PER_MM2 = 1.0 / MM2_PER_M2

# Mass Conversion Constants

G_PER_KG = 1000.0
KG_PER_G = 1.0 / G_PER_KG

# Moment of Inertia Conversion Constants

KGM2_PER_GCM2 = KG_PER_G * M2_PER_CM2


def inch(x_inch: float) -> float:
    '''Converts from inch to meters.'''
    return x_inch * M_PER_INCH

def to_inch(x_m: float) -> float:
    '''Converts from meters to inch.'''
    return x_m * INCH_PER_M

def ipm(v_ipm: float) -> float:
    '''Converts from IPM to m/s.'''
    return v_ipm * MPS_PER_IPM

def to_ipm(v_mps: float) -> float:
    '''Converts from m/s to IPM'''
    return v_mps * IPM_PER_MPS

def radps(omega_radps: float) -> float:
    '''Converts from Rads/s to Hz.'''
    return omega_radps * ONE_OVR_TWO_PI

def to_radps(omega_hz: float) -> float:
    '''Converts from Hz to Rads/s.'''
    return omega_hz * TWO_PI

def rpm(omega_rpm: float) -> float:
    '''Converts from RPM to Hz.'''
    return omega_rpm * MIN_PER_SEC

def to_rpm(omega_hz: float) -> float:
    '''Converts from Hz to RPM.'''
    return omega_hz * SEC_PER_MIN

def radps2(alpha_radps2: float) -> float:
    '''Converts from Rads/s^2 to Hz/s.'''
    return alpha_radps2 * ONE_OVR_TWO_PI

def to_radps2(alpha_hzps: float) -> float:
    '''Converts from Hz/s to Rads/s^2.'''
    return alpha_hzps * TWO_PI

def rpmps(alpha_rpmps: float) -> float:
    '''Converts from RPM/s to Hz/s.'''
    return alpha_rpmps * MIN_PER_SEC

def to_rpmps(alpha_hzps: float) -> float:
    '''Converts from Hz/s to RPM/s.'''
    return alpha_hzps * SEC_PER_MIN

def gcm2(j_gcm2: float) -> float:
    '''Converts from g*cm^2 to kg*m^2.'''
    return j_gcm2 * KGM2_PER_GCM2

def to_gcm2(j_kgm2: float) -> float:
    '''Converts from kg*m^2 to g*cm^2.'''
    return j_kgm2 * GCM2_PER_KGM2
