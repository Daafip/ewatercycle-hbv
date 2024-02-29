import numpy as np
from ewatercycle_HBV.forcing import calc_PET


def test_calc_PET():
    """s_rad, t_min, t_max, doy, alpha, elev, lat"""
    assert calc_PET(np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan) == np.nan # test nans?