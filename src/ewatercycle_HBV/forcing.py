"""Forcing related functionality for HBV."""
# Based on https://github.com/eWaterCycle/ewatercycle-marrmot/blob/main/src/ewatercycle_marrmot/forcing.py

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import xarray as xr
import numpy as np

from ewatercycle.base.forcing import DefaultForcing
# from ewatercycle.esmvaltool.builder import RecipeBuilder
from ewatercycle.esmvaltool.schema import Dataset, Recipe


class HBVForcing(DefaultForcing):
    """Container for HBV forcing data.

    Args:
        directory: Directory where forcing data files are stored.
        start_time: Start time of forcing in UTC and ISO format string e.g.
            'YYYY-MM-DDTHH:MM:SSZ'.
        end_time: End time of forcing in UTC and ISO format string e.g.
            'YYYY-MM-DDTHH:MM:SSZ'.
        shape: Path to a shape file. Used for spatial selection.

        -------------------------
        --> Either supply a forcing file: (sadly still often used by hydroligists)
        forcing_file: .txt file that contains forcings for HBV model including precipitation and evaporation
                    contains columns: ["year", "month", "day", "pr", "pev"] seperated by a space
        Use this with .to_xarray() to generate the files
        -------------------------

        --> or directly supply the netcdf dataset file
        precipitation_file: xarray containing precipition
        potential_evaporation_file: xarray containing potential evaporation, same format as above

    Examples:

        From existing forcing data:

        .. code-block:: python

            from ewatercycle.forcing import sources

            forcing = sources.HBVForcing(
                directory='/home/davidhaasnoot/Code/Forcing/',
                start_time='1997-08-01T00:00:00Z',
                end_time='2000-08-31T00:00:00Z',
                forcing_file='forcing.txt',
            )

            # ---------------- or --------------------
            forcing = sources.HBVForcing(
                directory='/home/davidhaasnoot/Code/Forcing/',
                start_time='1997-08-01T00:00:00Z',
                end_time='2000-08-31T00:00:00Z',
                precipitation_file="precipitation_file.nc"
                potential_evaporation_file="potential_evaporation_file.nc"
            )
            # where precipitation_file & potential_evaporation_file can be the same aslong as
            # they contain a 'pr' & 'pev' value

    """

    # either a forcing file is supplied
    forcing_file: Optional[str] = "forcing.txt"
    # or pr and pev are supplied seperately - can also be the same dataset
    pr: Optional[str] = "forcing.nc"
    pev: Optional[str] = "forcing.nc"
    alpha: Optional[float] = 1.26


    # @classmethod
    # def _build_recipe(
    #     cls,
    #     start_time: datetime,
    #     end_time: datetime,
    #     shape: Path,
    #     dataset: Dataset | str | dict,
    #     **model_specific_options,
    # ):
    #     return build_marrmot_recipe(
    #         start_year=start_time.year,
    #         end_year=end_time.year,
    #         shape=shape,
    #         dataset=dataset,
    #     )

    # TODO Implement this to take .txt and add them?
    def from_test_txt(self) -> xr.Dataset:
        """Load forcing data from a txt file into an xarray dataset.
        Must contain ["year", "month", "day", "pr","Q", "pev"] in columns
        Will convert date to pandas.Timestamp()
        pr (precipitation), Q (discharge), pev (potential evaportaion) - all im mm's
        Returns:
            Dataset with forcing data.
        """
        if self.directory is None or self.forcing_file is None:
            raise ValueError("Directory or forcing_file is not set")
        fn = self.directory / self.forcing_file
        forcing = np.loadtxt(fn, delimiter="	")
        names = ["year", "month", "day", "pr","Q", "pev"]
        df_in = pd.DataFrame(forcing, columns=names)
        df_in.index = df_in.apply(lambda x: pd.Timestamp(f'{int(x.year)}-{int(x.month)}-{int(x.day)}'), axis=1)
        df_in.drop(columns=["year", "month", "day"], inplace=True)
        df_in.index.name = "time"
        # TODO use netcdf-cf conventions
        ds = xr.Dataset(data_vars=df_in,
                        attrs={
                            "title": "HBV forcing data",
                            "history": "Created by ewatercycle_HBV.forcing.HBVForcing.to_xarray()",
                                },
                        )
        time = str(datetime.now())[:-10].replace(":","_")
        ds_name = f"HBV_forcing_{time}.nc"
        out_dir = self.directory / ds_name
        if not out_dir.exists():
            ds.to_netcdf(out_dir)
        self.pr = ds_name  # these are appended in model.py
        self.pev = ds_name # these are appended in model.py
        return ds

    def from_camels_txt(self) -> xr.Dataset:
        """Load forcing data from a txt file into an xarray dataset.
        Must be in the same format as the CAMELS dataset:
        3 lines containing: lat, elevation and area.
        4th line with headers: 'Year Mnth Day Hr dayl(s) prcp(mm/day) srad(W/m2) swe(mm) tmax(C) tmin(C) vp(Pa)'
        Takes from the 5th line onwards with \t delimiter.
        Will convert date to pandas.Timestamp()
        Then convert from pandas to a xarray.
        Returns:
            Dataset with forcing data.
        """
        if self.directory is None or self.forcing_file is None:
            raise ValueError("Directory or forcing_file is not set")
        fn = self.directory / self.forcing_file
        data = {}
        with open(fn, 'r') as fin:
            line_n = 0
            for line in fin:
                if line_n == 0:
                    data["lat"] = float(line.strip())
                elif line_n == 1:
                    data["elevation(m)"] = float(line.strip())
                elif line_n == 2:
                    data["area basin(m^2)"] = float(line.strip())
                elif line_n == 3:
                    header = line.strip()
                else:
                    break
                line_n += 1

        headers = header.split(' ')[3:]
        headers[0] = "YYYY MM DD HH"

        # read with pandas
        df = pd.read_csv(fn, skiprows=4, delimiter="\t", names=headers)
        df.index = df.apply(lambda x: pd.Timestamp(x["YYYY MM DD HH"][:-3]), axis=1)
        df.drop(columns="YYYY MM DD HH", inplace=True)
        df.index.name = "time"

        # rename
        new_names = [item.split('(')[0] for item in list(df.columns)]
        rename_dict = dict(zip(headers[1:], new_names))
        df.rename(columns=rename_dict, inplace=True)
        rename_dict2 = {'prcp': 'pr',
                        'tmax': 'tasmax',
                        'tmin': 'tasmin'}
        df.rename(columns=rename_dict2, inplace=True)

        # add attributes
        attrs = {"title": "HBV forcing data",
                 "history": "Created by ewatercycle_HBV.forcing.HBVForcing.from_camels_txt()",
                 "units": "daylight(s), precipitation(mm/day), mean radiation(W/m2), snow water equivalen(mm), temperature max(C), temperature min(C), vapour pressure(Pa)", }

        # add the data lines with catchment characteristics to the description
        attrs.update(data)
        # TODO use netcdf-cf conventions
        ds = xr.Dataset(data_vars=df,
                        attrs=attrs,
                        )
        # Potential Evaporation conversion using srad & tasmin/maxs
        ds['pev'] = calc_PET(ds['srad'],
                             ds["tasmin"].values,
                             ds["tasmax"].values,
                             ds["time.dayofyear"].values,
                             self.alpha,
                             ds.attrs['elevation(m)'],
                             ds.attrs['lat']
                             )
        # crop ds
        start = np.datetime64(self.start_time)
        end = np.datetime64(self.end_time)
        ds = ds.isel(time=(ds['time'].values > start) & ((ds['time'].values < end)))

        time = str(datetime.now())[:-10].replace(":","_")
        # TODO maybe change this time aspect? can get quite large - or simply remove in finalize
        ds_name = f"HBV_forcing_CAMELS_{time}.nc"
        out_dir = self.directory / ds_name
        if not out_dir.exists():
            ds.to_netcdf(out_dir)

        self.pev = ds_name # these are appended in model.py
        self.pr = ds_name  # these are appended in model.py
        return ds

def calc_PET(s_rad, t_min, t_max, doy, alpha, elev, lat):
    """
    calculates Potential Evaporation using Priestly–Taylor PET estimate, callibrated with longterm P-T trends from the camels data set (alpha).
    -------
    Params:
    Rn: net radiation estimate in W/m^2: converted to J/m^2/d
    s: (aka delta), is the slope of the saturation vapor pressure relationship in kPa/degC
    alpha: factor callibrated from longterm P-T trend compensating for lack of other data.
    -------
    Assumptions:
    G = 0 in a day: no loss to ground.

    -------
    reference:

    based on code from:
    https://github.com/neuralhydrology/neuralhydrology/blob/master/neuralhydrology/datautils/pet.py
    kratzert et al. 2022
    NeuralHydrology --- A Python library for Deep Learning research in hydrology,
    Frederik Kratzert and Martin Gauch and Grey Nearing and Daniel Klotz,
    https://doi.org/10.21105/joss.04050

    Who base on allen et al. (1998) 'FOA 56' & Newman et al (2015) 'CAMELS dataset'

    """
    G = 0
    LAMBDA = 2.45  # MJ/kg

    s_rad = s_rad * 0.0864  # conversion Wm-2 -> MJm-2day-1
    albedo = 0.23  # planetary albedo
    in_sw_rad = (1 - albedo) * s_rad

    # solar declination
    sol_dec = 0.409 * np.sin((2 * np.pi) / 365 * doy - 1.39)  # Equation 24 FAO-56 Allen et al. (1998)

    # Sunset hour angle
    lat = lat * (np.pi / 180)  # degree to rad
    term = -np.tan(lat) * np.tan(sol_dec)
    term[term < -1] = -1
    term[term > 1] = 1
    sha = np.arccos(term)

    # Inverse relative distance between Earth and Sun:
    ird = 1 + 0.033 * np.cos((2 * np.pi) / 365 * doy)  # Equation 23 FAO-56 Allen et al. (1998)

    # Extraterrestrial Radiation -  Equation 21 FAO-56 Allen et al. (1998)
    et_rad = ((24 * 60) / np.pi * 0.082 * ird) * (
                sha * np.sin(lat) * np.sin(sol_dec) + np.cos(lat) * np.cos(sol_dec) * np.sin(sha))

    # Clear sky radiation Equation 37 FAO-56 Allen et al. (1998)
    cs_rad = (0.75 + 2 * 10e-5 * elev) * et_rad

    # Actual vapor pressure estimated using min temperature - Equation 48 FAO-56 Allen et al. (1998
    avp = 0.611 * np.exp((17.27 * t_min) / (t_min + 237.3))

    # Net outgoing longwave radiation - Equation 49 FAO-56 Allen et al. (1998)
    term1 = ((t_max + 273.16) ** 4 + (t_min + 273.16) ** 4) / 2  # conversion in K in equation
    term2 = 0.34 - 0.14 * np.sqrt(avp)
    term3 = 1.35 * s_rad / cs_rad - 0.35
    stefan_boltzman = 4.903e-09
    out_lw_rad = stefan_boltzman * term1 * term2 * term3

    # psychrometer constant (kPa/C) - varies with altitude
    temp = (293.0 - 0.0065 * elev) / 293.0
    atm_pressure = np.power(temp, 5.26) * 101.3  # Equation 7 FAO-56 Allen et al. (1998)
    gamma = 0.000665 * atm_pressure

    # Slope of saturation vapour pressure curve Equation 13 FAO-56 Allen et al. (1998)
    t_mean = 0.5 * (t_min + t_max)
    s = 4098 * (0.6108 * np.exp((17.27 * t_mean) / (t_mean + 237.3))) / ((t_mean + 237.3) ** 2)

    Rn = in_sw_rad - out_lw_rad
    PET = ((alpha / LAMBDA) * s * (Rn - G)) / (s + gamma)
    return PET * 0.408  # energy to evap
# TODO add generate from ERA5 forcing dataset and Rhine.
"""
.. code-block:: python

    from ewatercycle.forcing import sources
    from ewatercycle.testing.fixtures import rhine_shape

    shape = rhine_shape()
    forcing = sources.MarrmotForcing.generate(
        dataset='ERA5',
        start_time='2000-01-01T00:00:00Z',
        end_time='2001-01-01T00:00:00Z',
        shape=shape,
    )
"""
# def build_marrmot_recipe(
#     start_year: int,
#     end_year: int,
#     shape: Path,
#     dataset: Dataset | str | dict,
# ) -> Recipe:
#     """Build an ESMValTool recipe for generating forcing for MARRMoT.
#
#     Args:
#         start_year: Start year of forcing.
#         end_year: End year of forcing.
#         shape: Path to a shape file. Used for spatial selection.
#         dataset: Dataset to get forcing data from.
#             When string is given a predefined dataset is looked up in
#             :py:const:`ewatercycle.esmvaltool.datasets.DATASETS`.
#             When dict given it is passed to
#             :py:class:`ewatercycle.esmvaltool.models.Dataset` constructor.
#     """
#     return (
#         RecipeBuilder()
#         .title("Generate forcing for the MARRMoT hydrological model")
#         .description("Generate forcing for the MARRMoT hydrological model")
#         .dataset(dataset)
#         .start(start_year)
#         .end(end_year)
#         .shape(shape)
#         # TODO do lumping in recipe preprocessor instead of in diagnostic script
#         # .lump()
#         .add_variables(("tas", "pr", "psl", "rsds"))
#         .add_variable("rsdt", mip="CFday")
#         .script(
#             str((Path(__file__).parent / "forcing_diagnostic_script.py").absolute()),
#             {"basin": shape.stem})
#         .build()
#     )