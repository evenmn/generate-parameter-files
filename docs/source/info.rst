Other useful functionality
--------------------------

Initialize from dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^

The parameters can also be initialized from a dictionary. This can be useful for inputting custom parameters to LAMMPS, for instance. The molecule has to be given to make coupled parameters work, but may just be a single atom. Usage example:

.. code-block:: python

    params =      {"XXX":    {"H": 1.0,
                              "eta": 1.0,
                              "Zi": 0.0,
                              "Zj": 0.0,
                              "r1s": 1.0,
                              "D": 0.0,
                              "r4s": 1.0,
                              "W": 0.0,
                              "rc": 10.0,
                              "B": 0.0,
                              "xi": 0.0,
                              "r0": 0.0,
                              "C": 0.0,
                              "cos(theta)": 0.0}}

    potential = Vashishta(params=params, molecule="X")


Reduce information
^^^^^^^^^^^^^^^^^^

The default behavior is to output a message to the terminal when a parameter set was successfully written to file. Avoid this by setting :code:`success_msg=False`:

.. code-block:: python

   potential.write("Si.sw", success_msg=False)


When the parameter file is modified, a line is added to the file header:

.. code-block:: bash

   # NB: THE PARAMETERS HAVE BEEN MODIFIED

Avoid this by setting :code:`mod_msg=False`:

.. code-block:: python

   potential.update_params({'SiSiSi': {'p': 0.4}}, mod_msg=False)

