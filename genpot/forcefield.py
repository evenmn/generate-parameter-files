import os
import re
import shutil
import datetime
import importlib
import copy
import warnings


class ForceField:
    def __init__(self, base=None, params=None, molecule=None, citation=None):
        self.base = base
        if params is not None:
            if base is not None:
                warnings.warn("Both base parameterization and parameters \
                              provided, ignoring base parameterization")
            if molecule is None:
                warnings.warn("Molecule has not been provided, cannot keep \
                               neutral (coupled charges)")
                molecule=""
            self.params = params
            self.citation = citation
            self._get_multiplicity(molecule)
            self.header = self._write_header(self.citation)
        if base is not None:
            self.params, molecule, self.citation = self._collect_params()
            self._get_multiplicity(molecule)
            self.header = self._write_header(self.citation)
        self.modified = False

    def __repr__(self):
        return ""

    @staticmethod
    def _write_header(citation):
        package_name = "genpot"
        url = "http://www.github.com/evenmn/generate-parameter-files"
        cont = "Even M. Nordhagen"
        email = "evenmn@fys.uio.no"
        today = datetime.datetime.today()

        string = f"# THIS PARAMETER FILE WAS GENERATED USING {package_name} \n#\n"
        string += f"# URL: {url}\n"
        string += f"# CONTRIBUTOR: {cont}, {email}\n#\n"
        string += f"# DATE: {today:%B %d, %Y}\n"
        string += f"# CITATION: {citation}\n#\n"
        return string

    def list_params(self):
        """List all available parameterizations.
        """
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, f"param/{self.__repr__()}")
        files = os.listdir(path)
        files = list(filter(lambda s: not s.startswith('__'), files))
        files = [os.path.splitext(file)[0] for file in files]
        print(', '.join(files))
        return files

    def set_params(self, base):
        """Set parameter set
        """
        self.base = base
        self.params, molecule, self.citation = self._collect_params()
        self._get_multiplicity(molecule)
        self.header = self._write_header(self.citation)

    def _get_multiplicity(self, molecule):
        """Find multiplicity of atoms in molecule
        """
        self.molecule = re.findall('[A-Z][^A-Z]*', molecule)
        self.multiplicity = {}
        for atom in self.molecule:
            cnt = self.molecule.count(atom)
            self.multiplicity[atom] = cnt

    def _collect_params(self):
        """collect information about base set
        """
        if self.base is None:
            raise TypeError("Base parameterization is not given!!")
        param_path = f"genpot.param.{self.__repr__()}.{self.base}"
        pm = importlib.import_module(param_path, package=None)
        return copy.deepcopy(pm.params), pm.molecule, pm.citation

    @staticmethod
    def _ordered_string(params, param_suffices, param_list):
        """Returning an ordered list of all the parameter values

        :type params: dict
        :param params: dictionary with all parameters
        :type param_suffices: list of str
        :param param_suffices: correctly ordered list of all parameter suffices
        :type param_list: list
        :param param_list: initial list to append parameters to
        """
        string = ""
        for atom in param_list:
            string += f"{atom:<5}"
        for param in param_suffices:
            number = round(params[param], 6)
            string += f" {number:>10}"
        return string + "\n"

    def append_type_to_file(self, group, params, filename):
        """Append the actual parameter values to the parameter file.

        :type group: str
        :param group: group (e.g. "SiSiSi")
        :type params: dict
        :param params: dictionary with all parameters
        :type filename: str
        :param filename: parameter filename
        """
        # Split group
        prefix_list = re.findall('[A-Z0-9][^A-Z0-9]*', group)
        with open(filename, 'a') as f:
            f.write("\n")
            for i, suffix_list in enumerate(self.suffices):
                if i == 0:
                    string = self._ordered_string(params, suffix_list, prefix_list)
                else:
                    string = self._ordered_string(params, suffix_list, 3 * [''])
                f.write(string)

    def update_params(self, params={}, mod_msg=True):
        """Updates the parameter dictionary
        """
        if mod_msg and not self.modified:
            self.header += "# NB: THE PARAMETERS HAVE BEEN MODIFIED\n#\n"
            self.modified = True
        for groups, parameters in params.items():
            groups = groups.split(",")
            for group in groups:
                if group == "global":
                    for key, value in parameters.items():
                        if key.startswith("Z_"):
                            this = key.split("_")[-1]
                            charge_this = value
                            for atom, multi in self.multiplicity.items():
                                if atom == this:
                                    multi_this = multi
                                else:
                                    other = atom
                                    multi_other = multi
                            charge_other = - charge_this * multi_this / multi_other
                            charge_map = {0: 'i', 1: 'j'}
                            for group in self.params.keys():
                                group_split = re.findall('[A-Z][^A-Z]*', group)
                                for i, atom in enumerate(group_split[:2]):
                                    n = charge_map[i]
                                    if atom == this:
                                        self.params[group][f"Z{n}"] = charge_this
                                    elif atom == other:
                                        self.params[group][f"Z{n}"] = charge_other
                elif group == "all":
                    for key, value in parameters.items():
                        for group in self.params.keys():
                            self.params[group][key] = value
                else:
                    for parameter, value in parameters.items():
                        self.params[group][parameter] = value

    def scale(self, scalefactor):
        """ Apply a multiplicative factor to the interaction potential: U -> U' = scalefactor * U by modifying
        the parameteters in the potential. Useful for i.e thermodynamic integration. 
        NOTE: Must be implemented differently for differet types of potentials.

        :param scalefactor: Factor to scale the potential by
        :type scalefactor: float
        """
        return NotImplementedError

    def write(self, filename="dest.vashishta", success_msg=True):
        """Generates input parameter file for the potential. The default
        parameters are the ones specified in Wang et al., so parameters
        that are not specified will fall back on these default parameters.

        :param substance: substance to simulate
        :type substance: str
        :param filename: filename of parameter file
        :type filename: str
        :param params: dictionary of parameters that should be changed
        :type params: dict
        """
        # Make new parameter file
        this_dir, this_filename = os.path.split(__file__)
        header_filename = os.path.join(this_dir, f"data/header.{self.__repr__()}")

        shutil.copyfile(header_filename, filename)
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(self.header.rstrip('\r\n') + '\n' + content)
            for suffix_list in self.suffices:
                f.write("#" + 11 * " " + ", ".join(suffix_list) + "\n")

        # Add parameters to file
        for group, params in self.params.items():
            self.append_type_to_file(group, params, filename)
        if success_msg:
            print(f"New parameter file '{filename}' successfully generated!")

    def __call__(self, filename="dest.vashishta", success_msg=True):
        """Generates input parameter file for the potential. The default
        parameters are the ones specified in Wang et al., so parameters
        that are not specified will fall back on these default parameters.

        :param substance: substance to simulate
        :type substance: str
        :param filename: filename of parameter file
        :type filename: str
        :param params: dictionary of parameters that should be changed
        :type params: dict
        """
        self.write(filename, success_msg=success_msg)
