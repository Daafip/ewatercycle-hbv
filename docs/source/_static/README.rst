eWaterCycle plugin - HBV
========================

|PyPI| |github license badge| |fair-software badge| |Quality Gate
Status|

This package is based on the `Leaky
bucket <https://github.com/eWaterCycle/ewatercycle-leakybucket/tree/main>`__
& is a wrapper for the `HBV-bmi <https://github.com/Daafip/HBV-bmi>`__
model.

HBV (Hydrologiska Byråns Vattenbalansavdelning) is a conceptual
hydrological model. For more information on it’s history, see this
`paper <https://hess.copernicus.org/articles/26/1371/2022/>`__.

This current implementation is *without* a snow reservoir.

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

.. |PyPI| image:: https://img.shields.io/pypi/v/ewatercycle-HBV
   :target: https://pypi.org/project/ewatercycle-HBV/
.. |github license badge| image:: https://img.shields.io/github/license/Daafip/ewatercycle-hbv
   :target: https://github.com/Daafip/ewatercycle-hbv
.. |fair-software badge| image:: https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8B%20%20%E2%97%8B-yellow
   :target: https://fair-software.eu
.. |Quality Gate Status| image:: https://sonarcloud.io/api/project_badges/measure?project=Daafip_ewatercycle-hbv&metric=alert_status
   :target: https://sonarcloud.io/summary/new_code?id=Daafip_ewatercycle-hbv
