# Example of how the scale method may be used to generate parameters that may be used for i.e Thermodynamic Integration
from genpot import Vashishta
scalefactors = [1.0, 0.75, 0.50, 0.25, 0.0]
for s in scalefactors:
    potential = Vashishta("sio2_vashishta_wang")
    potential.scale(s)
    potential("SiO.%i.Vashishta" % round(s * 100))