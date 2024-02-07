"""eWaterCycle wrapper for the LeakyBucket model."""
import json
from collections.abc import ItemsView
from pathlib import Path
from typing import Any

from ewatercycle.base.forcing import GenericLumpedForcing
from ewatercycle.base.model import ContainerizedModel, eWaterCycleModel
from ewatercycle.container import ContainerImage


class HBVMethods(eWaterCycleModel):
    """
    The eWatercycle HBV model.
    

    """
    forcing: GenericLumpedForcing  # The model requires forcing.
    parameter_set: None  # The model has no parameter set.

    _config: dict = {
        "forcing_file": "",
        "timestep": 0,
        "parameters": "",
        "initial_storage": "",
    }

    def _make_cfg_file(self, **kwargs) -> Path:
        """Write model configuration file."""

        for kwarg in kwargs:  # Write any kwargs to the config.
            self._config[kwarg] = kwargs[kwarg]

        config_file = self._cfg_dir / "HBV_config.json"

        with config_file.open(mode="w") as f:
            f.write(json.dumps(self._config, indent=4))

        return config_file

    @property
    def parameters(self) -> ItemsView[str, Any]:
        return self._config.items()


class HBV(ContainerizedModel, HBVMethods):
    """The HBV eWaterCycle model, with the Container Registry docker image."""
    bmi_image: ContainerImage = ContainerImage(
        "dockerhub.io/daafip/hbv-numpy-grpc4bmi:v0.0.1"
    )
