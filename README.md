# Generate potential files used in LAMMPS
genpot is a light-weight Python package for generating parameter files to be used in LAMMPS. Per 2020-09-26, the package supports the Stillinger-Weber force-field and the Vashishta force-field, with multiple base parameterizations. However, the framework is written in a general way that makes it easy to add other force-fields. The strength of the package is that the user can modify the parameter sets as they like. This is in particular useful when parameterizing a force-field.

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

## Basic Usage
The short script
``` python
from genpot import StillingerWeber
potential = StillingerWeber()
potential.set_params('si_stillinger_1985')
potential("Si.sw")
```
will generate the original parameterization by Stillinger and Weber from 1985:
``` bash
$ cat Si.sw

...

# element 1 element 2 element 3
#           epsilon, sigma, a, lambda, gamma, cos(theta)
#           A, B, p, q, tol

Si   Si   Si        2.1683     2.0951        1.8       21.0        1.2  -0.333333
                  7.049556   0.602225        4.0        0.0        0.0

```
### Modify parameters
Say, for instance, that you want to change the value of ```p``` from 4.0 to 5.0. This can easily be done by
``` python
potential.update_params({'SiSiSi': {'p': 5.0}})
```

### List available base parameterizations
Above, we used the base parameterization "si_stillinger_1985". How can we find other parameterizations? All available parameterizations can be found by the command ```potential.list_params()```. Example:
``` python
from genpot import Vashishta
potential = Vashishta()
potential.list_params()
```
``` bash
h2o_wang_2007, lnp_branicio_2009, sic_vashishta_2007, sio2_vashishta_1990
```

### Coupled parameters
For a substance of pure silicon, as in the example above, we will only have one interaction group (interactions between the silicon atoms). For more complex substances, like water, there are multiple interaction groups that we need to assign values to. All the values can be set manually as shown above:
``` python
potential.update_params({'OOO': {'Zi': -0.6, 'Zj': -0.6, 'r4s': 5.0},
                         'HHH': {'Zi': 0.3, 'Zj': 0.3, 'r4s': 5.0},
                         'OHH': {'Zi': -0.6, 'Zj': 0.3, 'r4s': 5.0, 'H': 1000.0},
                         'HOO': {'H': 1000.0}})
```
However, often the parameters are coupled. Here, the effective charge of H and O should be the same in all interaction groups, which makes it excessive to update all of them manually. Instead, the effective charges can be updated globally, using:
``` python
potential.update_params({'global': {'Z_H': 0.3}})
```
Also, we often want a parameter to be the same across of all groups. Especially for cutoff distances, this is convenient. Similar to the ```global``` group, there is a ```all``` group that simplifies this operation:
``` python
potential.update_params({'all': {'r4s': 5.0}})
```
Sometimes, we want to change a parameter of several groups, but not all. This can be done by specifying the different groups separated by a comma:
``` python
potential.update_params({'OHH,HOO': {'H': 1000.0}})
```
