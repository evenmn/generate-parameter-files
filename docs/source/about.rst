About generate-parameter-files
===============================

:code:`generate-parameter-files` is a Python library which aims of generating customized parameter files to be used in LAMMPS. The currently supported force fields are Stillinger-Weber, Vashishta and TIP4P, but additional force fields might be added with few lines of code. One starts from an initial base parameterization (usually taken from the literature). The package might be used for reparameterizing potentials.

After chosing force field (in our case `Stillinger-Weber <https://docs.lammps.org/pair_sw.html>`_), one imports the force field from :code:`genpot`:

.. code-block:: python

   from genpot import StillingerWeber

To pick the initial parameters, we may list all base parameter sets:

.. code-block:: python

   potential = StillingerWeber()
   potential.list_params()

By doing this we will realize that there is only one base parameter set available, namely the initial parameters by Stillinger and Weber from 1985. This is the base parameterization that we will go for:

.. code-block:: python

   potential.set_params('si_stillinger_1985')

When we have the base parameterization, we are ready to modify the parameters. A parameter is well-defined by its keyword and the interacting elements. To change the ideal angle (angle that corresponds to lowest three-body interaction) between all the Si-Si-Si triplets, run

.. code-block:: python

   from math import pi, cos

   theta = 110
   cos_theta = cos(2 * pi * theta / 180) 
   potential.update_params({'SiSiSi': {'cos(theta)': cos_theta}})

Finally, the parameters are written to file using the :code:`write`-method:

.. code-block:: python

   potential.write("Si.sw")
