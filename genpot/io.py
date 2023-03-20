import warnings
from .forcefield import ForceField
from .vashishta import Vashishta
from .stillingerweber import StillingerWeber


def read(filename, format=None, **kwargs):
    """
    Read parameter file, either a nbody-based file or input-based file

    """

    format_nbody = ["vashishta", "sw", "usc"]
    format_input = ["tip4p"]

    # try to detect whether file is nbody-based or input-based
    if format is None:
        if filename.endswith(".in"):
            # guess input-based
            read_func = read_input
            return read_input(filename, format=None, **kwargs)
        else:
            raise TypeError("Do not know how to read the file")
    elif isinstance(format, ForceField):
        if str(format) in format_nbody:
            read_func = read_nbody
        elif str(format) in format_input:
            read_func = read_input
    elif isinstance(format, str):
        if format in format_nbody:
            read_func = read_nbody
        elif format in format_input:
            read_func = read_input
    else:
        raise TypeError("'format' has wrong type. Expected str or ForceField object")

    nbody=3
    if format == "usc":
        nbody=4  # need to include parameter type
        format="vashishta"  # use vashishta object
    return read_func(filename, format=format, nbody=nbody, **kwargs)



def read_nbody(filename, format=None, sufficies=None, nbody=3, **kwargs):
    """
    Read nbody parameter file of the form

        X X X p1 p2 p3 p4 p5 ...
        X Y Z p1 p2 p3 p4 p5 ...

    :param filename: file to read
    :type filename: str
    :param format: file format (vashishta, sw, tersoff) or object
    :type format: str or ForceField obj
    :param sufficies: sufficies in correct order (nested if line shift)
    :type sufficies: list or list of list
    :param nbody: nbody-potential (3 by default)
    :type nbody: int
    :rtype: ForceField object
    """
    
    # create ForceField object if not given
    if format is None:
        if sufficies is None:
            warnings.warn("Not able to map parameters to labels as neither format nor sufficies is given")
        pot = ForceField()
    elif isinstance(format, ForceField):
        pot = format
    elif isinstance(format, str):
        format = format.lower()
        if format == "vashishta":
            pot = Vashishta()
        elif format == "sw":
            pot = StillingerWeber()
        else:
            raise NotImplementedError(f"Format '{format}' is not implemented!")
    else:
        raise TypeError("'format' has wrong type. Expected str or ForceField object")

    # ensure sufficies is flatten
    if sufficies is None:
        try:
            sufficies = pot.suffices
            #print(sufficies)
        except:
            pass
    if sufficies is not None and isinstance(sufficies[0], list):
        sufficies = [item for sublist in sufficies for item in sublist]

    # read file
    params = {}
    with open(filename, "r+") as f:
        for line in f:
            if line.startswith("#"):
                # skip hashed lines
                continue
            elif not line.strip():
                # skip empty lines
                continue
            elif line.split()[0].replace(".","").isnumeric():
                # append to previous line
                splitted = line.split()
                for i in range(len(splitted)):
                    if sufficies is None:
                        suffix = str(i+nvalues+1)
                    else:
                        suffix = sufficies[i+nvalues]
                    local[suffix] = float(splitted[i])
                params[label] = local
            elif isinstance(line.split()[0], str):
                splitted = line.split()
                nvalues = len(splitted)-nbody
                label = "".join(splitted[:nbody])
                local = {}
                for i in range(nvalues):
                    if sufficies is None:
                        suffix = str(i+1)
                    else:
                        suffix = sufficies[i]
                    local[suffix] = float(splitted[i+nbody])
                params[label] = local


    # create ForceField object if not given
    del pot
    if format is None:
        if sufficies is None:
            warnings.warn("Not able to map parameters to labels as neither format nor sufficies is given")
        pot = ForceField(params=params, **kwargs)
    elif isinstance(format, ForceField):
        pot = format
    elif isinstance(format, str):
        format = format.lower()
        if format == "vashishta":
            pot = Vashishta(params=params, **kwargs)
        elif format == "sw":
            pot = StillingerWeber(params=params, **kwargs)
        else:
            raise NotImplementedError(f"Format '{format}' is not implemented!")
    else:
        raise TypeError("'format' has wrong type. Expected str or ForceField object")

    return pot


def read_input(filename, format=None, **kwargs):
    """
    Read parameters from LAMMPS input script
    """
    raise NotImplemented


def write(filename, success_msg=True):
    pass


def write_nbody(self, filename, success_msg=True):
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
