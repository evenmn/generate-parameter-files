The USC force-field
===================

The USC force field was developed at University of Southern California (USC) for modeling silica, water and interactions between the two substances. It is a generalized version of the Vashishta potential, and rely on the :code:`Vashishta` object (see previous page).

.. code-block:: python

   from genpot import Vashishta

   potential = Vashishta("sioh_wang_2007")

To read the potential, use the :code:`usc` format:

.. code-block:: python

    from genpot import read

    potential = read("SiOH2O.vashishta", format="usc")
