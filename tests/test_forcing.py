import numpy as np
from ewatercycle_HBV.forcing import calc_PET


def test_calc_PET():
    """tests s_rad, t_min, t_max, doy, alpha, elev, lat"""
    assert calc_PET(np.array([0]), np.array([0]), np.array([0]), np.array([0]), np.array([0]), np.array([0]), np.array([0])) == np.array([0])