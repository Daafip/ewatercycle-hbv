"""eWaterCycle wrapper for the LeakyBucket model."""
import json
from collections.abc import ItemsView
from pathlib import Path
from typing import Any

from ewatercycle.base.forcing import GenericLumpedForcing
from ewatercycle.base.model import ContainerizedModel, eWaterCycleModel
from ewatercycle.container import ContainerImage


class LeakyBucketMethods(eWaterCycleModel):
    """The eWatercycle LeakyBucket model.
    
    Setup args:
        leakiness: The "leakiness" of the bucket in [d-1].
    """
    forcing: GenericLumpedForcing  # The model requires forcing.
    parameter_set: None  # The model has no parameter set.

    _config: dict = {
        "forcing_file": "",
        "precipitation_file": "",
        "leakiness": 0.05,
    }

    def _make_cfg_file(self, **kwargs) -> Path:
        """Write model configuration file."""
        self._config["precipitation_file"] = str(
            self.forcing.directory / self.forcing.pr
        )
        self._config["temperature_file"] = str(
            self.forcing.directory / self.forcing.tas
        )

        for kwarg in kwargs:  # Write any kwargs to the config.
            self._config[kwarg] = kwargs[kwarg]

        config_file = self._cfg_dir / "leakybucket_config.json"

        with config_file.open(mode="w") as f:
            f.write(json.dumps(self._config, indent=4))

        return config_file

    @property
    def parameters(self) -> ItemsView[str, Any]:
        return self._config.items()


class LeakyBucket(ContainerizedModel, LeakyBucketMethods):
    """The LeakyBucket eWaterCycle model, with the Container Registry docker image."""
    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/ewatercycle/leakybucket-grpc4bmi:v0.0.1"
    )
