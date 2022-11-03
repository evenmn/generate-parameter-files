The Vashishta force field
=========================

The Vashistha force field is associated with the :code:`Vashistha` object, and contains the same methods as the :code:`StillingerWeber` object described on the _about_ page. This includes the :code:`list_params`-method:

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

In some implementations of the Vashishta potential, the steric repulsion strength is expressed in terms of the ionic radii in the same fashion as in the Lorentz–Berthelot mixing rules:

.. math::

    H_{ij}=A_{ij}\left(\frac{\sigma_i+\sigma_j}{r_{ij}}\right)^\eta_{ij}

We can benefit from this as the parameters are linked to physical quantities, and less real parameters have to be set. In :code:`genpot`, setting :math:`H` from :math:`A, \sigma_i` and :math:`\sigma_j` happens automatically if either :math:`A` or :math:`\sigma_<X>` is set globally:

.. code-block:: python

    potential.update_params({'global': {'sigma_X': 0.9})

Setting :math:`H` indirectly requires that all the parameters A, sigmai and sigmaj exist in the parameter dictionary. If they do not, they need to be added (see the 'all' group below):

.. code-block:: python

    potential.update_params({'all': {'sigmai': 0.0, 'sigmaj': 0.0, 'A': 0.0}})  # create keys
    potential.update_params({'XXX': {'A': 34.76}, 'YYY': {'A': 52.91}, 'XYY,YXX': {'A': 2.11}})  # set A
    potential.update_params({'global': {'sigma_X': 2.7, 'sigma_Y': 1.8}})  # set sigma
    
Similarly, the induced charge-dipole interaction can be expressed in terms of the electronic polarizability,

.. math::

    D_{ij}=\frac{\alpha_i\Z_j^2+\alpha_j\Z_i^2}{2}

with :math:`\alpha_i` as the electronic polarizability of component :math:`i`. The parameter D is indirectly updated when the alphas are updated globally:

.. code-block:: python

    potential.update_params({'global': {'alpha_X': 1.3}})

Again, this only works if both alphai and alphaj exist. If not, they first need to be created:

.. code-block:: python

    potential.update_params({'all': {'alphai': 0.0, 'alphaj': 0.0}})  # create keys
    potential.update_params({'global': {'alpha_X': 1.3, 'alpha_Y': 1.65}})  # set alpha

Above, we have used the group 'all' on several occations. The 'all' group contains all other groups (but not 'global'), and can either be used to create a key or update a parameter across all the groups at the same time. The latter behavior is usually desired for cutoff distances:

.. code-block:: python

   potential.update_params({'all': {'r4s': 4.5}})


Scaling the potential
^^^^^^^^^^^^^^^^^^^^^

Scaling the entire potential can be useful in a few situations, including when performing thermodynamic integration (TI). Scaling the potential with a scale factor :math:`\gamma` corresponds to scaling :code:`H`, :code:`D`, :code:`W` and :code:`B` with :math:`\gamma` and :code:`Z_Si` and :code:`Z_O` with :math:`\sqrt{\gamma}`. This is done by the :code:`scale`-method:

.. code-block:: python

   potential.scale(scalefactor=0.5)


Initialize from dictionary
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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


