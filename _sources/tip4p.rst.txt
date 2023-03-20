The TIP4P force field
=====================

The TIP4P force field object differs from the :code:`StillingerWeber` and :code:`Vashishta` objects in the sense that a parameter file is not written, but rather a LAMMPS script that can be included in the LAMMPS input script. Apart from that, the usage is similar to the other force field objects:

.. code-block:: python

   from genpot import TIP4P

   potential = TIP4P("tip4p-2005")

Since TIP4P always contains one molecule type (water), interaction groups are never specified. The possible parameters are :code:`Z_H`, :code:`Z_O`, :code:`r0`, :code:`theta`, :code:`OM`, :code:`epsilon`, :code:`sigma` and :code:`r4s`. They can be modified by

.. code-block:: python

   potential.update_params({'epsilon': 0.1855, 'sigma': 3.16})

As for the :code:`Vashishta`-object, the charges are considered as coupled such that the molecule is neutral. Therefore, changing :code:`Z_H` would also change :code:`Z_O`. The LAMMPS script is written to file using the :code:`write`-method:

.. code-block:: python

   potential.write("tip4p.water")
