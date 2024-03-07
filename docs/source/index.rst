.. eWaterCycle-HBV documentation master file, created by
   sphinx-quickstart on Thu Mar  7 10:34:21 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to eWaterCycle-HBV's documentation!
===========================================

HBV (Hydrologiska Byråns Vattenbalansavdelning) is a conceptual
hydrological model. For more information on it’s history, see this
`paper <https://hess.copernicus.org/articles/26/1371/2022/>`__.

This current implementation is *without* a snow reservoir.

This package is based on the `Leaky
bucket <https://github.com/eWaterCycle/ewatercycle-leakybucket/tree/main>`__
& is a wrapper for the `HBV-bmi <https://github.com/Daafip/HBV-bmi>`__
model designed for the `eWaterCycle <https://ewatercycle.nl/>`_ platform. 

Installation
------------

Install this package alongside your eWaterCycle installation

.. code:: console

   pip install ewatercycle-hbv

Then HBV becomes available as one of the eWaterCycle models

.. code:: python

   from ewatercycle.models import HBV

Implementing your own model
---------------------------

For more information on how this plugin works, and on how to implement
your own model see the `plugin
guide <https://github.com/eWaterCycle/ewatercycle-leakybucket/blob/main/plugin_guide.md>`__

Changelog
---------

Changes can be found in
`CHANGELOG.md <https://github.com/Daafip/ewatercycle-hbv/blob/main/CHANGELOG.md>`__
on GitHub

License
-------

This is a ``ewatercycle-plugin`` & thus this is distributed under the
same terms as the template: the
`Apache-2.0 <https://spdx.org/licenses/Apache-2.0.html>`__ license.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   model
   example_model_run_HBV

