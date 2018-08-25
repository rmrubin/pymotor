
class Direct:
    def __init__(self, j=0.0, d=0.0):
        self.type = 'direct'
        self.j = j
        self.d_in = d


class Coupler:
    def __init__(self, j=0.0, d_in=0.0, d_out=0.0):
        self.type = 'coupler'
        self.j = j
        self.d_in = d_in
        self.d_out = d_out


class Wheel:
    def __init__(self, diameter, j=0.0):
        self.type = 'wheel'
        self.diameter = diameter
        self.j = j
        self.d


class Screw:
    
    def __init__(self, pitch=None, lead=None, j=0.0):
        
        self.type = 'screw'
        
        if (pitch is None and lead is None) or (pitch is not None and lead is not None):
            raise ValueError("Either lead or pitch must be a float.")
        else:
            if pitch is not None:
                self.pitch = pitch
                self.lead = 1/pitch
            else: # lead is not None
                self.lead = lead
                self.pitch = 1/lead
        
        self.j = j


class Gear:
    def __init__(self, ratio, j_in=0.0, j_out=0.0, d_in=0.0, d_out=0.0):
        self.type = 'gear'
        self.ratio = ratio
        self.j_in = j_in
        self.j_out = j_out
        self.d_in = d_in
        self.d_out = d_out
