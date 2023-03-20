The Vashishta force field
=========================

The Vashishta force field is associated with the :code:`Vashishta` object, and contains the same methods as the :code:`StillingerWeber` object described on the previous page:

.. code-block:: python

   from genpot import Vashishta

   potential = Vashishta()
   potential.list_params()

By calling this, a bunch of base parameterizations will appear. For this tutorial, we will use the original SiO2-parameters from 1990:

.. code-block:: python

   potential.set_params("sio2_vashishta_1990")

To change the steric repulsion parameter :code:`H` for the O-O interactions, we call the :code:`update_params`-method as usual:

.. code-block:: python

   potential.update_params({'OOO': {'H': 775.}})

A problem that one soon will realize is that many of the parameters depend on each other, they are coupled.


Coupled parameters
^^^^^^^^^^^^^^^^^^

Coupled parameters are parameters that depend on each other in some way. Examples on coupled parameters include the O-Si-Si and Si-O-O two-body parameters, which have to be the same since the Si-O and O-Si interactions should be equally strong. Multiple interaction groups can be specified by a comma delimiter:

.. code-block:: python

   potential.update_params({'SiOO,OSiSi': {'H': 0.85}})

Another example on a parameter couple is the Si and O effective charges, :code:`Z_Si` and :code:`Z_O`, respectively. They should be coupled such that the total molecule is neutral, i.e., :code:`Z_Si` =-2 :code:`Z_O`. As the molecule is defined in the parameter file, the code is able to change all the charges after this rule. Either :code:`Z_Si` og :code:`Z_O` has to be set using the :code:`global` group:

.. code-block:: python

   potential.update_params({'global': {'Z_Si': 1.5})

Finally, sometimes one wants to change a parameter across _all_ groups. This is usually the case for cutoff distances. To do that, use the 'all' group:

.. code-block:: python

   potential.update_params({'all': {'r4s': 4.5}})


Scaling the potential
^^^^^^^^^^^^^^^^^^^^^

Scaling the entire potential can be useful in a few situations, including when performing thermodynamic integration (TI). Scaling the potential with a scale factor :math:`\gamma` corresponds to scaling :code:`H`, :code:`D`, :code:`W` and :code:`B` with :math:`\gamma` and :code:`Z_Si` and :code:`Z_O` with :math:`\sqrt{\gamma}`. This is done by the :code:`scale`-method:

.. code-block:: python

   potential.scale(scalefactor=0.5)


