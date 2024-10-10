from __future__ import annotations
from .timestamps import Timestamps
import autograd.numpy as np
import datetime
import matplotlib.pyplot as plt

class PPS:

    def __init__(self, index: np.ndarray, time: np.ndarray):

        self.index = index
        self.time = time
        self.timestamps = Timestamps(self.time)
        self.update_properties()


    def correct(self, file_type: str) -> None:
            
        if file_type == "RSP2":
 
            indices = self.index
            times = self.timestamps.get_us()
            p = np.polyfit(indices, times - times[0], 1)
            new_timestamps = times[0] + np.polyval(p, indices)

            self.timestamps.set_us([int(round(new_timestamp)) for new_timestamp in new_timestamps])
            self.time = self.timestamps.get_us()
        
            self.update_properties()


    def update_properties(self):

        self.datetime = [datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=int(x)) for x in self.time]
        self.dt = np.diff(self.time)
        self.di = np.diff(self.index)
        self.shifted_timestamps = self.timestamps.get_s() - self.timestamps.get_s()[0]
        self.slope, self.intercept_time = np.polyfit(self.index, self.shifted_timestamps, 1)
        self.samplerate = 1/self.slope

        self.residual_pps = self.shifted_timestamps - (self.slope*self.index + self.intercept_time)

    
    def plot_uncertainty(self) -> None:

        plt.figure()
        plt.plot(self.index - self.index[0], self.shifted_timestamps, '*-')
        plt.xlabel("Sample index")
        plt.ylabel("PPS timing [s] ")
        plt.title(f"PPS timing as a function of sample number ")
        plt.tight_layout()
        plt.show()
    

        plt.figure()
        plt.plot(self.shifted_timestamps, 1E3*self.residual_pps, '*-')
        plt.xlabel("PPS timing [s]")
        plt.ylabel("Residual [ms]")
        plt.title(f"PPS residual - Number of PPS = {len(self.index)} - $\mu$ = {np.round(1E6*np.mean(np.abs(self.residual_pps)), 2)} µs - $\sigma$ = {np.round(1E6*np.std(np.abs(self.residual_pps)), 2)} µs " )
        plt.tight_layout()
        plt.show()

        fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)
        # We can set the number of bins with the *bins* keyword argument.
        axs.hist(self.residual_pps)
        plt.show


        

