# Generate parameter files for the Vashistha inter-atomic potential
This package generates parameter files for the Vashishta inter-atomic potential to be used in LAMMPS. The Vashishta potential has successfully been applied on silica systems and other systems.

The package is based on a set of default parameters. For silica, the default parameters are taken from Vashishta, 1990. Default parameters for silica and water are provided in ```genpot.substance```. 

## Installation
First download the contents:
``` bash
$ git clone https://github.com/evenmn/generate-potential-files
```
and then install genpot:
``` bash
$ cd genpot
$ pip install .
```

## Usage
``` python
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
```

Here, the default parameters for water are taken from ```genpot.substance```. Then, the parameters ```Z_O``` and ```Z_H``` are changed using the ```set_parameters``` method. To generate the parameter file, the object can be called directly with a given filename.
