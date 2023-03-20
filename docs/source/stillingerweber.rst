The Stillinger-Weber force field
================================

The Stillinger-Weber force field is described here: `Stillinger-Weber <https://docs.lammps.org/pair_sw.html>`_. The original silicon parameters can be fetched with

.. code-block:: python

   from genpot import StillingerWeber

   potential = StillingerWeber("si_stillinger_1985")

When we have the base parameterization, we are ready to modify the parameters. A parameter is well-defined by its keyword and the interacting elements. To change the ideal angle (angle that corresponds to lowest three-body interaction) between all the Si-Si-Si triplets, run

.. code-block:: python

   from math import pi, cos

   theta = 110
   cos_theta = cos(2 * pi * theta / 180) 
   potential.update_params({'SiSiSi': {'cos(theta)': cos_theta}})

Finally, the parameters are written to file using the :code:`write`-method:

.. code-block:: python

   potential.write("Si.sw")
