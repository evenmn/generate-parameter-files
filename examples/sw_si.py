from genpot import StillingerWeber
potential = StillingerWeber('si_stillinger_1985')
potential.update_params({'SiSiSi': {'p': 5.0}})
potential("../Si.sw")
