from genpot import VashishtaGenerator
from genpot.substance import water

Z_H = 0.4
Z_O = - 2 * Z_H
params = {"HHH" : {"Zi" : Z_H, "Zj" : Z_H},
          "OOO" : {"Zi" : Z_O, "Zj" : Z_O},
          "HOO" : {"Zi" : Z_H, "Zj" : Z_O},
          "OHH" : {"Zi" : Z_O, "Zj" : Z_H}}

gen = VashishtaGenerator(water)
gen.set_parameters(params)
gen("H2O.vashishta")
