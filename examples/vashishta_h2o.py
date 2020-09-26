from genpot import Vashishta
potential = Vashishta()
potential.list_params()
potential.set_params('h2o_wang_2007')
potential.update_params({'global': {'Z_H': 0.42}})
potential("H2O.vashishta")
