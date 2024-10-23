"""eWaterCycle wrapper for the HBV model."""
import json
import warnings
import xarray as xr
from collections.abc import ItemsView
from pathlib import Path
from typing import Any, Type

from ewatercycle.forcing import LumpedMakkinkForcing
from ewatercycle.forcing import GenericLumpedForcing

from ewatercycle_HBV.forcing import HBVForcing # Use custom forcing instead
from ewatercycle.base.model import (
    ContainerizedModel,
    eWaterCycleModel,
    LocalModel,
    )
from ewatercycle.container import ContainerImage
from bmipy import Bmi


def import_bmi():
    """"Import BMI, raise useful exception if not found"""
    try:
        from HBV import HBV as HBV_bmi
    except ModuleNotFoundError:
        msg = (
            "HBV bmi package not found, install using: `pip install HBV`"
        )
        raise ModuleNotFoundError(msg)

    return HBV_bmi


SUPPORTED_FORCINGS = ("HBVForcing", "CaravanForcing", "LumpedMakkinkForcing")

HBV_PARAMS = (
    "Imax",
    "Ce",
    "Sumax",
    "Beta",
    "Pmax",
    "Tlag",
    "Kf",
    "Ks",
    "FM",
)

HBV_STATES = (
    "Si",
    "Su",
    "Sf",
    "Ss",
    "Sp",
)

class HBVMethods(eWaterCycleModel):
    """
    The eWatercycle HBV model.
    """

    forcing: LumpedMakkinkForcing | HBVForcing | GenericLumpedForcing
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

        validate_forcing(self)

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
        """
        # remove bmi
        self._bmi.finalize()
        del self._bmi


class HBV(ContainerizedModel, HBVMethods):
    """The HBV eWaterCycle model, with the Container Registry docker image."""
    bmi_image: ContainerImage = ContainerImage(
        "ghcr.io/daafip/hbv-bmi-grpc4bmi:v1.5.0"
    )

class HBVLocal(LocalModel, HBVMethods):
    """The HBV eWaterCycle model, with the local BMI."""
    bmi_class: Type[Bmi] = import_bmi()


def validate_forcing(model: HBVMethods):
    """Validate the forcing input of the model.

    Checks if:
        - the forcing object is officially supported by this model. Warns if not.
        - the user is trying to use GenericLumpedForcing. Raises error if they are.
        - the forcing is HBVForcing, and if so, deals with the txt/nc files correctly
        - the units are correct (if the data has attributes), and converts them it 
            they are not correct.

    Args:
        model: HBV Model class

    """
    if type(model.forcing).__name__ not in SUPPORTED_FORCINGS:
        msg = (
            f"{type(model.forcing).__name__} is not supported by this model and "
            "might not work!"
        )
        warnings.warn(msg)

    if type(model.forcing).__name__ == 'GenericLumpedForcing':
        msg = (
            "Generic Lumped Forcing does not provide potential evaporation,"
            " which this model needs"
        )
        raise ValueError(msg)

    if isinstance(model.forcing, HBVForcing):
        if model.forcing.test_data_bool:
            model.forcing.from_test_txt()
        elif model.forcing.camels_txt_defined():
            model.forcing.from_camels_txt()
        elif model.forcing.forcing_nc_defined():
            model.forcing.from_external_source()
        else:
            msg = (
                "Ensure either a txt file with camels data or an(/set of)"
                " xarrays is defined"
            )
            raise ValueError(msg)

    for var in ("pr", "tas", "evpsblpot"):
        if var not in model.forcing.filenames:
            msg = f"{var} is a required input variable!"
            raise ValueError(msg)

    fnames = {}
    fnames["pr"] = str(model.forcing.directory / model.forcing.filenames["pr"])
    fnames["tas"] = str(model.forcing.directory / model.forcing.filenames["tas"])
    fnames["evspsblpot"] = str(model.forcing.directory / model.forcing.filenames["evspsblpot"])

    for var in ("pr", "evspsblpot", "tas"):
        ds = xr.open_dataset(fnames[var])

        if hasattr(ds[var].attrs, "units"):  # Must have units attr to be able to check
            if ds[var].attrs["units"] == "kg s-1 m-2":
                ds[var].attrs.update({"units":"mm"})
                ds[var] = ds[var] * 86400
            if ds[var].attrs["units"] == "K":
                ds[var].attrs.update({"units":"degC"})
                ds[var] -= 273.15

            tmp_file = (
                model.forcing.directory /
                model.forcing.filenames[var].replace(var, f"{var}_converted")
            )
            ds.to_netcdf(tmp_file)
            ds.close()
            fnames[var] = str(tmp_file)

    ## finally asign fnames (possibly with converted files)
    model._config["precipitation_file"] = fnames["pr"]
    model._config["potential_evaporation_file"] = fnames["evspsblpot"]
    model._config["mean_temperature_file"] = fnames["tas"]
