# eWaterCycle plugin - HBV

[![PyPI](https://img.shields.io/pypi/v/ewatercycle-HBV)](https://pypi.org/project/ewatercycle-HBV/)

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

## Implementing your own model

For more information on how this plugin works, and on how to implement your own model see the [plugin guide](https://github.com/eWaterCycle/ewatercycle-leakybucket/blob/main/plugin_guide.md)

## License

This is a `ewatercycle-plugin` & thus this is distributed under the same terms as the template: the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.

## Changelog

### v1.0.0
working basic version after various testing [versions](https://test.pypi.org/project/ewatercycle-HBV/)
#### v1.1.0
upgrade to new version: added support for updating memory vector on the fly for Data assimilation
##### v1.1.1
Fixed bug with Tlag and setting memory vector correctly 
##### v1.1.2
Adding `.finalize()` method - clears up the directory. Especially useful for DA. 
### V1.2.0
- pretty big issue with setting values fixed - won't affect most use but will cause issues for Data Assimilation
- use opportunity to name all HBV packages/naming/images to 1.2.0 