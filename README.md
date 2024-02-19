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
### V1.3.1
- now supports camels.txt files natively. Just download the ones you want from there and add it. 
- make sure you also include the alpha value which is a model output from the run, defaults to 1.26 but varies per catchment. Eq1 of camels paper.
### v1.3.2. - 1.3.3
- now correctly slices the ds to given start and end time whoops
- 