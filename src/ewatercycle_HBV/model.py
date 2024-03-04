"""eWaterCycle wrapper for the HBV model."""
import json
import warnings
from collections.abc import ItemsView
from pathlib import Path
from typing import Any, Type

from ewatercycle.base.forcing import GenericLumpedForcing # or later Use custom forcing instead?
from ewatercycle_HBV.forcing import HBVForcing # Use custom forcing instead
from ewatercycle.base.model import ContainerizedModel, eWaterCycleModel
from ewatercycle.container import ContainerImage


class HBVMethods(eWaterCycleModel):
    """
    The eWatercycle HBV model.
    

    """
    forcing: HBVForcing  # The model requires forcing.
    parameter_set: None  # The model has no parameter set.

    _config: dict = {
        "precipitation_file": "",
        "potential_evaporation_file": "",
        "parameters": "",
        "initial_storage": "",
        "alpha": 1.26,
    }

    def _make_cfg_file(self, **kwargs) -> Path:
        """Write model configuration file."""

        # do some basic test to check on forcing
        if self.forcing.test_data_bool:
            self.forcing.from_test_txt()
        elif self.forcing.camel_txt_defined():
            self.forcing.from_camels_txt()
        elif self.forcing.forcing_nc_defined():
            pass # to do: quality check here in future rather than in model.
        else:
            raise UserWarning("Ensure either a txt file with camels data or an(/set of) xarrays is defined")

        self._config["precipitation_file"] = str(
            self.forcing.directory / self.forcing.pr
        )

        self._config["potential_evaporation_file"] = str(
            self.forcing.directory / self.forcing.pev
        )
        ## possibly add later for snow?
        # self._config["temperature_file"] = str(
        #     self.forcing.directory / self.forcing.tas
        # )
        # self._config["temperature_min_file"] = str(
        #     self.forcing.directory / self.forcing.tasmin
        # )
        # self._config["temperature_max_file"] = str(
        #     self.forcing.directory / self.forcing.tasmax
        # )

        for kwarg in kwargs:  # Write any kwargs to the config.
            self._config[kwarg] = kwargs[kwarg]

        config_file = self._cfg_dir / "HBV_config.json"

        with config_file.open(mode="w") as f:
            f.write(json.dumps(self._config, indent=4))


        return config_file

    @property
    def parameters(self) -> ItemsView[str, Any]:
        return self._config.items()


    def finalize(self) -> None:
        """Perform tear-down tasks for the model.

        After finalization, the model should not be used anymore.

        ADDED: Remove created config files, especially useful for DA models
        """

        # remove bmi
        self._bmi.finalize()
        del self._bmi

        # TODO: remove data set file
        # TODO maybe change this time aspect? can get quite large - or simply remove in finalize
        # ds_name = f"HBV_forcing_CAMELS_{time}.nc"
        # out_dir = self.directory / ds_name
        # if not out_dir.exists():
        #     ds.to_netcdf(out_dir)

        try:
            # remove config file
            config_file = self._cfg_dir / "HBV_config.json"
            config_file.unlink()
        except FileNotFoundError:
            warnings.warn(message=f'Config not found at {config_file}, removed by user?',category=UserWarning)

        try:
            # once empty, remove it
            self._cfg_dir.rmdir()
        except FileNotFoundError:
            warnings.warn(message=f'Config folder not found at {self._cfg_dir.rmdir()}',category=UserWarning)


        for file in ["potential_evaporation_file", "precipitation_file"]:
            self._config[file]

class HBV(ContainerizedModel, HBVMethods):
    """The HBV eWaterCycle model, with the Container Registry docker image."""
    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/daafip/hbv-bmi-grpc4bmi:v1.2.0"
    )
