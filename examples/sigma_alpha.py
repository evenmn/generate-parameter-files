from genpot import Vashishta

potential = Vashishta("h2o_20110114")
potential.update_params({'global': {'sigma_H': 2.0}})
potential.update_params({'global': {'alpha_H': 2.0}})
print(potential.params)


potential = Vashishta("h2o_wang_2007")
potential.update_params({'all': {'A': 0.0, 'sigmai': 0.0, 'sigmaj': 0.0}})
potential.update_params({'global': {'sigma_H': 3.0, 'sigma_O': 1.5}})
print(potential.params)

