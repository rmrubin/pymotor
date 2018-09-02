
class Direct:
    def __init__(self, j=0.0):
        self.type = 'direct'
        self.j = j


class Coupler:
    def __init__(self, j=0.0):
        self.type = 'coupler'
        self.j = j


class Wheel:
    def __init__(self, diameter, j=0.0):
        self.type = 'wheel'
        self.diameter = diameter
        self.j = j


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
    def __init__(self, ratio=1.0, j_in=0.0, j_out=0.0):
        self.type = 'gear'
        self.ratio = ratio
        self.j_in = j_in
        self.j_out = j_out
 