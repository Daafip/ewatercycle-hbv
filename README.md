# eWaterCycle plugin - HBV

[![Python package](https://github.com/Daafip/ewatercycle-hbv/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Daafip/ewatercycle-hbv/actions/workflows/test.yml)
[![docs badge](https://readthedocs.org/projects/ewatercycle-hbv/badge/?version=latest)](https://ewatercycle-hbv.readthedocs.io/en/latest/index.html)
[![PyPI](https://img.shields.io/pypi/v/ewatercycle-HBV)](https://pypi.org/project/ewatercycle-HBV/)
[![github license badge](https://img.shields.io/github/license/Daafip/ewatercycle-hbv)](https://github.com/Daafip/ewatercycle-hbv)
[![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8B%20%20%E2%97%8B-yellow)](https://fair-software.eu)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Daafip_ewatercycle-hbv&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Daafip_ewatercycle-hbv)


This package is based on the [Leaky bucket](https://github.com/eWaterCycle/ewatercycle-leakybucket/tree/main) & is a wrapper for the [HBV-bmi](https://github.com/Daafip/HBV-bmi) model. 

HBV (Hydrologiska Byråns Vattenbalansavdelning) is a conceptual hydrological model. For more information on it's history, see this [paper](https://hess.copernicus.org/articles/26/1371/2022/).

This current implementation is _without_ a snow reservoir. 

## Installation
Install this package alongside your eWaterCycle installation

```console
pip install ewatercycle-hbv
```

Then HBV becomes available as one of the eWaterCycle models

```python
from ewatercycle.models import HBV
```
## Documentation
Some basic documentation can be found [here](https://ewatercycle-hbv.readthedocs.io/en/latest/index.html)

## Changelog
Changes can be found in [CHANGELOG.md](https://github.com/Daafip/ewatercycle-hbv/blob/main/CHANGELOG.md) on GitHub

## Implementing your own model

For more information on how this plugin works, and on how to implement your own model see the [plugin guide](https://github.com/eWaterCycle/ewatercycle-leakybucket/blob/main/plugin_guide.md)

## License

This is a `ewatercycle-plugin` & thus this is distributed under the same terms as the template: the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.

