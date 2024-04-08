"""eWaterCycle wrapper for the HBV model."""
import json
import xarray as xr
import warnings
import os
from collections.abc import ItemsView
from pathlib import Path
from typing import Any, Type

from ewatercycle.forcing import LumpedMakkinkForcing
from ewatercycle.forcing import GenericLumpedForcing

from ewatercycle_HBV.forcing import HBVForcing # Use custom forcing instead
from ewatercycle.base.model import ContainerizedModel, eWaterCycleModel
from ewatercycle.container import ContainerImage

HBV_PARAMS = (
    "Imax",
    "Ce",
    "Sumax",
    "Beta",
    "Pmax",
    "Tlag",
    "Kf",
    "Ks",
)

HBV_STATES = (
    "Si",
    "Su",
    "Sf",
    "Ss"
)

class HBVMethods(eWaterCycleModel):
    """
    The eWatercycle HBV model.
    """

    forcing: LumpedMakkinkForcing|HBVForcing|GenericLumpedForcing  # The model requires forcing.
    parameter_set: None  # The model has no parameter set.

    _config: dict = {
        "precipitation_file": "",
        "potential_evaporation_file": "",
        "mean_temperature_file": "",
        "parameters": "",
        "initial_storage": "",
                        }

    def _make_cfg_file(self, **kwargs) -> Path:
        """Write model configuration file."""

        # do some basic test to check on forcing
        if type(self.forcing).__name__ == 'HBVForcing':
            if self.forcing.test_data_bool:
                self.forcing.from_test_txt()
            elif self.forcing.camels_txt_defined():
                self.forcing.from_camels_txt()
            elif self.forcing.forcing_nc_defined():
                self.forcing.from_external_source()
            else:
                raise UserWarning("Ensure either a txt file with camels data or an(/set of) xarrays is defined")

            self._config["precipitation_file"] = str(
                self.forcing.directory / self.forcing.pr
            )

            self._config["potential_evaporation_file"] = str(
                self.forcing.directory / self.forcing.pev
            )
            self._config["mean_temperature_file"] = str(
                self.forcing.directory / self.forcing.tasmean)


        elif type(self.forcing).__name__ == 'GenericLumpedForcing':
                raise UserWarning("Generic Lumped Forcing does not provide potential evaporation, which this model needs")

        elif type(self.forcing).__name__ == 'LumpedMakkinkForcing':
            temporary_pev_file = self.forcing.directory / self.forcing.filenames['evspsblpot'].replace('evspsblpot',
                                                                                                       'pev_mm')
            if not temporary_pev_file.is_file():
                ds = xr.open_dataset(self.forcing.directory / self.forcing.filenames['evspsblpot'])
                attributes = ds['evspsblpot'].attrs
                attributes['units'] = 'mm'
                ds = ds.rename({'evspsblpot': 'pev'})
                ds['pev'] = ds['pev'] * 86400
                ds['pev'].attrs = attributes
                ds.to_netcdf(temporary_pev_file)
                ds.close()

            temporary_pr_file = self.forcing.directory / self.forcing.filenames['pr'].replace('pr', 'pr_mm')
            if not temporary_pr_file.is_file():
                ds = xr.open_dataset(self.forcing.directory / self.forcing.filenames['pr'])
                attributes = ds['pr'].attrs
                attributes['units'] = 'mm'
                ds['pr'] = ds['pr'] * 86400
                ds['pr'].attrs = attributes
                ds.to_netcdf(temporary_pr_file)
                ds.close()

            temporary_tasmean_file = self.forcing.directory / self.forcing.filenames['tas'].replace('tas', 'tasmean')
            if not temporary_tasmean_file.is_file():
                ds = xr.open_dataset(self.forcing.directory / self.forcing.filenames['tas'])
                attributes = ds['tas'].attrs
                ds['tasmean'] = ds['tas']
                if ds['tasmean'].mean().values > 200: # adjust for kelvin units
                    ds['tasmean'] -= 273.15
                ds['tasmean'].attrs = attributes
                ds.to_netcdf(temporary_tasmean_file)
                ds.close()

            self._config["precipitation_file"] = str(
                temporary_pr_file
            )
            self._config["potential_evaporation_file"] = str(
                temporary_pev_file
            )

            self._config["mean_temperature_file"] = str(
                temporary_tasmean_file
            )

        for kwarg in kwargs:  # Write any kwargs to the config. - doesn't overwrite config?
            self._config[kwarg] = kwargs[kwarg]

        config_file = self._cfg_dir / "HBV_config.json"

        with config_file.open(mode="w") as f:
            f.write(json.dumps(self._config, indent=4))


        return config_file

    @property
    def parameters(self) -> ItemsView[str, Any]:
        """List the (initial!) parameters for this model.

        Exposed HBV parameters:
            Imax (mm): is the maximum amount of interception, under the assumption that all interception evaporates

            Ce(−): is a parameter used to describe what factor actually evaporates from the ground
                  (Unsaturated root zone: 𝑆𝑢) and is 𝐸𝐴=𝑆𝑢𝑆𝑢,𝑚𝑎𝑥×𝐶𝑒𝐸𝑝

            Sumax(mm): Is the size of the reservoir of the unsaturated root zone (𝑆𝑢)
                    i.e. the amount of water the top layer of soil can hold. This parameter is used in a few other calculations.

            Beta (−): is a factor controlling the split between fast and slow flow (overland vs groundwater).
                    Some water will be held by the soil whilst some flows over it and straight to the river.
                    𝐶𝑟=(𝑆𝑢/𝑆𝑢_𝑚𝑎𝑥)^𝛽 which is used to determine the water infiltrating: 𝑄𝑖𝑢=(1−𝐶𝑟)𝑃𝑒
                    where 𝑃𝑒 is the actual precipitation reaching the ground.
                    The rest flow into the fast reservoir 𝑄𝑢𝑓 – which is the groundwater.

            Pmax (mm): is the maximum amount of percolation which can occur from the ground
                       to the deeper groundwater flow: 𝑄𝑢𝑠=𝑃𝑚𝑎𝑥(𝑆𝑢𝑆𝑢,𝑚𝑎𝑥)

            T_lag (d): is the lag time between water falling and reaching the river.

            Kf (-): the fast flow is modelled as a linear reservoir thus a fraction
                    of the volume stored leaves to the river 𝑄𝑓=𝐾𝑓∗𝑆𝑓

            Ks (−): Similarly the slow flow is also modelled as 𝑄𝑆=𝐾𝑠∗𝑆𝑆.

            FM (mm/deg/d): Melt Factor: mm of melt per deg per day

        """
        pars: dict[str, Any] = dict(zip(HBV_PARAMS, self._config["parameters"].split(',')))
        return pars.items()

    @property
    def states(self) -> ItemsView[str, Any]:
        """List the (initial!) states for this model.

        Exposed HBV states:
            Si (mm): Interception storage, water stored in leaves
            Su (mm): Unsaturated rootzone storage, water stored accessible to plants
            Sf (mm): Fastflow storage, moving Fast through the soil - preferential flow paths, upper level
            Ss (mm): Groundwater storage, moving Slowly through the soil - deeper grounds water.
            Sp (mm): SnowPack Storage, amount of snow stored

        """
        pars: dict[str, Any] = dict(zip(HBV_STATES, self._config["initial_storage"].split(',')))
        return pars.items()


    def finalize(self) -> None:
        """Perform tear-down tasks for the model.

        After finalization, the model should not be used anymore.

        ADDED: Remove created config files, especially useful for DA models
        """

        # remove bmi
        self._bmi.finalize()
        del self._bmi

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

        if type(self.forcing).__name__ == 'HBVForcing':
            # NetCDF files created are timestamped and running them a lot creates many files, remove these
            if self.forcing.camels_txt_defined() or self.forcing.test_data_bool:
                self.unlink()

        elif type(self.forcing).__name__ == 'LumpedMakkinkForcing':
            # we created a temporary file so let's unlink that
            self.unlink()

    def unlink(self):
        for file in ["potential_evaporation_file", "precipitation_file","mean_temperature_file"]:
            path = self.forcing.directory / self._config[file]
            if path.is_file():  # often both with be the same, e.g. with camels data.
                path.unlink()
            else:
                pass

class HBV(ContainerizedModel, HBVMethods):
    """The HBV eWaterCycle model, with the Container Registry docker image."""
    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/daafip/hbv-bmi-grpc4bmi:v1.4.0"
    )
