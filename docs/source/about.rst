About generate-parameter-files
===============================

:code:`generate-parameter-files` is a complete tool for handling LAMMPS parameter files directly in Python. The implemented functionality includes reading, writing, manipulating and storing the files. The currently supported force fields are Stillinger-Weber, Vashishta, USC and TIP4P, but additional force fields might be added with few lines of code. The package might be used to automatize parameter updates, which is useful when reparameterizing potentials.

Usage example
^^^^^^^^^^^^^

A common usage of this code is to read an existing parameter file, manipulating it and then write the modified version. Below we will break down the basic commands for this.

We use the :code:`read` function to read the parameter file into a :code:`ForceField` object. The force-field associated with the parameter file needs to be set with the :code:`format` argument, here demonstrated with the Vashishta potential:

.. code-block:: python

    >>> from genpot import read
    >>> potential = read("sio2.vashishta.1990", format="vashishta")

Other supported formats are :code:`sw`, :code:`usc` and :code:`tip4p`. Alternatively, the :code:`ForceField` object can be initialized from already saved parameter sets:

.. code-block:: python

    >>> from genpot import Vashishta
    >>> potential = Vashishta()
    >>> potential.list_params()
    lnp_branicio_2009, sio2_vashishta_1990, sic_vashishta_2007, sio2_vashishta_1997
    >>> potential.set_params('sio2_vashishta_1990')

Once the :code:`ForceField` object is initialized, the parameters can be modified. To update one parameter associated with an interaction group (e.g. Si-Si-Si), the :code:`update_params` method is used:

.. code-block:: python

    >>> potential.update_params({'SiSiSi': {'H': 1000}})

Several parameters and groups can be modified at once. Finally, the modified parameter file can be written to file

.. code-block:: python

    >>> potential.write("sio2.vashishta.1990.modified")

More advanced usage examples can be found on the force-field specific pages.
