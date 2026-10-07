from math import sqrt

import aspn23_lcm
import numpy as np
from navanalysis.lcm.conversions import llh_to_ned, ned_sigma_to_llh_sigma
from navanalysis.lcm.measurements import get_pva

from .Data import Data


class TimeData(Data):
    meas_ns: list | np.ndarray
    sigma: list | np.ndarray

    def __init__(self, label):
        super().__init__(label)
        self.time = []
        self.meas_ns = []
        self.sigma = []

    def add_data(self, time, aspn_msg):
        if not isinstance(aspn_msg, aspn23_lcm.measurement_time):
            return
        meas_ns = aspn_msg.elapsed_nsec[0]
        self.time.append(time)
        self.meas_ns.append(meas_ns)
        self.sigma.append(sqrt(aspn_msg.covariance[0][0]))
