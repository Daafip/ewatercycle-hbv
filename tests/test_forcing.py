import numpy as np
from ewatercycle_HBV.forcing import calc_pet


def test_calc_pet():
    """tests s_rad, t_min, t_max, doy, alpha, elev, lat"""
    assert calc_pet(np.array([0]), np.array([0]), np.array([0]), np.array([0]), np.array([0]), np.array([0]), np.array([0])) == np.array([0])