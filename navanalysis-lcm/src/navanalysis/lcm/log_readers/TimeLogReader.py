import numpy as np
from aspn23_xtensor import to_seconds
from navanalysis.lcm.data import TimeData
from numpy import float64
from numpy.typing import NDArray

from .LogReader import LogReader


class TimeLogReader(LogReader[TimeData]):
    # For converting LLH for all PVAs to NED relative to the same initial pos
    llh0: NDArray[float64] | None

    def __init__(
        self,
        logfile: str,
        desired_types: tuple,
        save_all: bool,
        config_file: str = '',
    ):
        super().__init__(logfile, TimeData, desired_types, save_all, config_file)

    def postprocess(self):
        for data in self.log_data.data.values():
            # Convert tov to relative time
            data.time = np.array([to_seconds(t - self.log_data.t0) for t in data.time])

            data.meas_ns = np.array(data.meas_ns)
            data.sigma = np.array(data.sigma)
