from genpot import StillingerWeber
potential = StillingerWeber()
potential.list_params()
potential.set_params('si_stillinger_1985')
potential.update_params({'p': 5.0})
potential("Si.sw")
