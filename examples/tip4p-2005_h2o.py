from genpot import TIP4P
potential = TIP4P('tip4p-2005')
potential.update_params({"Z_O": -1.1})
potential('force-field.tip4p')
