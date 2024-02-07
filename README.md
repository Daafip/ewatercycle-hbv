# eWaterCycle plugin example: a leaky bucket model

This repository is a template for adding models to eWatercycle, and will guide you through all required steps.

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

For more information on how this plugin works, and on how to implement your own model see the [plugin guide](plugin_guide.md)

## License

`ewatercycle-plugin` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
