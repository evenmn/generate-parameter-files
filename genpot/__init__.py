class VashishtaGenerator:
    def __init__(self, default):
        self.default = default

    def set_parameters(self, parameters):
        """ This function overwrites the default parameters.

        Parameters
        ----------
        parameters : dictionary
            nested dictionary with new parameters. Has to be in the form of:
            {"comb1": {"param1": value1, "param2": value2, ...},
             "comb2": {"param1": value1, "param2": value2, ...},
             ...}.
        """
        for comb, params in parameters.items():
            for param, value in params.items():
                self.default[comb][param] = value

    def ordered_parameter_string(self, params, param_suffices, param_list, string):
        """ Returning an ordered list of all the parameter values.

        Parameters
        ----------
        params : dictionary
            dictionary with all parameters.
        param_suffices : List of str
            list of all parameter suffices.
        param_list : list
            initial list to append parameter to.
        string : str
            initial string that will be extended.
        """
        for suffix in param_suffices:
            param_list.append(params[suffix])
        for param in param_list:
            string += str(param) + 2 * " "
        return string + "\n"

    def append_type_to_file(self, name, params, filename):
        """ Append the actual parameter values to the parameter file.

        Parameters
        ----------
        name : str
            name of element combo (e.g. "SiSiSi")
        params : dictionary
            dictonary with all parameters
        filename  : str
            filename
        """
        # Split name
        from re import findall
        prefix_list = findall('[A-Z][^A-Z]*', name)
        params_line1 = ["H", "eta", "Zi", "Zj", "r1s", "D", "r4s"] # correctly ordered
        params_line2 = ["W", "rc", "B", "xi", "r0", "C", "cos(theta)"]  # correctly ordered
        string_line1 = self.ordered_parameter_string(params, params_line1, prefix_list, "")
        string_line2 = self.ordered_parameter_string(params, params_line2, [], (len(name) + 6) * " ")

        with open(filename, 'a') as file:
            file.write("\n")
            file.write(string_line1)
            file.write(string_line2)

    def __call__(self, filename, header_filename="/data/header.vashishta"):
        """ Generates input parameter file for the potential. The default
        parameters are the ones specified in Wang et al., so parameters
        that are not specified will fall back on these default parameters.

        Parameters
        ----------
        filename : str
            filename
        header_filename : str
            header file name
        """
        # Find path to header file
        import os
        this_dir, this_filename = os.path.split(__file__)
        header_filename = this_dir + header_filename

        # Add header to file
        from shutil import copyfile
        copyfile(header_filename, filename)

        # Add parameters to file
        for name, params in self.default.items():
            self.append_type_to_file(name, params, filename)

if __name__ == "__main__":
    Z_H = 0.4
    Z_O = - 2 * Z_H
    params = {"HHH" : {"Zi" : Z_H, "Zj" : Z_H},
              "OOO" : {"Zi" : Z_O, "Zj" : Z_O},
              "HOO" : {"Zi" : Z_H, "Zj" : Z_O},
              "OHH" : {"Zi" : Z_O, "Zj" : Z_H}}

    from substance import water
    gen = VashishtaGenerator(water)
    gen.set_parameters(params)
    gen("H2O.vashishta")
