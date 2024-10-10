9# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 12:29:32 2023

@author: joachimb
"""

import autograd.numpy as np
import datetime
from dataclasses import dataclass

from brams import files

from typing import Any, Dict

from scipy.signal import filtfilt, find_peaks, hilbert, savgol_filter
from scipy.signal.windows import blackman
from scipy.special import fresnel
from scipy.interpolate import interp1d

import scipy.stats as stats

import matplotlib.pyplot as plt

from types import MappingProxyType

from KDEpy import FFTKDE

from utils.global_constants import WAVELENGTH

from .fresnel_transform import compute_ft, optimize_ft

IDENTIFICATION_HALF_RANGE_FREQUENCY = 100
FILTERING_HALF_RANGE_FREQUENCY = 287
FILTERING_LENGTH_KERNEL = 2501
PREPADDING_DURATION = 2.5
POSTPADDING_DURATION = 2.5
SG_ORDER = 4

NOISE_DURATION = 1

# Time delays
AMPL_SG_WINDOW_DURATION = 35*1E-3 #s
MIN_PEAK_PROMINENCE_AMPL = 0.1
MIN_PEAK_HEIGHT_AMPL = 1

# FOR UQ 
MINIMUM_SNR = 0
MINIMUM_RISE_DURATION = 0
MAXIMUM_RISE_DURATION = 1

"""
MINIMUM_SNR = 8 
MAXIMUM_RISE_DURATION = 0.04
MINIMUM_RISE_DURATION = 0.002
"""

TIMING_CORRECTIONS = MappingProxyType({"AR": 24.5 * 1E-3, "ICOM": 1.9 * 1E-3, "RSP2": 33.3 * 1E-3})

# Pre-t0
MINIMUM_CROPPED_PHASE_VALUE = -17.244160851361816 #-10.939944483167269 # -17.244160851361816 # 5 Fresnel zones -20.392561110298526 # 6 Fresnel zones # -14.098024352514232 # Corresponds to 4 Fresnel zones - 10.939944483167269 # Corresponds to 3 Fresnel zones before t0 10.939944483167269 # Corresponds to 3 Fresnel zones before t0

PHASE_SG_WINDOW = 1
PROMINENCE_PHASE = 1 # rad
MAXIMUM_PHASE_VALUE = -0.5135047640574028 # rad

FRESNEL_PARAMETER_AT_MAXIMUM_PHASE = 0.571758 
MINIMUM_FRESNEL_PARAMETER = -10
NUMBER_FRESNEL_PARAMETERS = 10000

MAXIMUM_DURATION_KNEE_TO_MAXIMUM_PHASE = 200*1E-3 # s

NUMBER_OFFSETS_AROUND_T0 = 150
NUMBER_OFFSETS_AFTER_MINIMUM_PHASE = 150

MINIMUM_LENGTH_SLIDING_SLOPE = 30
NUMBER_WINDOWS_SLIDING_SLOPE = 100
MINIMUM_r_value_pre_t0 = 0.99
MINIMUM_SIZE_HISTOGRAM = 30
POINTS_AROUND_HISTOGRAM_PEAK = 30


@dataclass
class Meteor:

    timing: float = None
    SNR: float = None
    v_pseudo_pre_t0: float = None
    r_value_pre_t0: float = None
    fresnel_acceleration: float = None

    def json(self) -> Dict[str, Any]:

        return self.__dict__
        
    def extract_infos(self, start:str, end:str, file:files.File, plot:bool):
        
        print("")
        print(f"Extracting meteor infos for {file.system_code} ...")
        
        i_meteor_signal, q_meteor_signal, sample_meteor_start, times = self.extract_i_q_meteor(start, end, file, plot=plot)
        
        meteor_ampl = np.sqrt(i_meteor_signal**2 + q_meteor_signal**2)
        output_t0 = compute_t0_and_SNR(meteor_ampl, file.signal.samplerate, times, plot=plot)

        if output_t0:

            index_meteor, rise_duration, SNR = output_t0
            meteor_sample = index_meteor + sample_meteor_start
  
            self.timing = extrapolate_time(meteor_sample, file.signal.pps.timestamps.get_s(), file.signal.pps.index, file.signal.samplerate) - TIMING_CORRECTIONS[file.type]
            self.SNR = SNR
 
            print("Meteor timing successfully determined !")
        
            # Phase
            corrected_meteor_phase = detrend_doppler_shift(i_meteor_signal, q_meteor_signal, self.frequency, times-times[0])
            
            output_pre_t0 = compute_pre_t0_speed(meteor_ampl, corrected_meteor_phase, index_meteor, file.signal.samplerate, times, plot)

            if output_pre_t0:

                index_meteor_pre_t0, v_pseudo_pre_t0, r_value_pre_t0 = output_pre_t0
                meteor_sample_pre_t0 = index_meteor_pre_t0 + sample_meteor_start

                #self.timing_pre_t0 = extrapolate_time(meteor_sample_pre_t0 , file.signal.pps.timestamps.get_s(), file.signal.pps.index, file.signal.samplerate) - TIMING_CORRECTIONS[file.type]
                self.v_pseudo_pre_t0 = v_pseudo_pre_t0
                self.r_value_pre_t0 = r_value_pre_t0


        """
        complex_meteor_signal = i_meteor_signal + 1j*q_meteor_signal
        complex_echo_signal = complex_meteor_signal[echo]

        delta = 1/file.signal.samplerate
 
        fresnel_acceleration = optimize_ft(complex_echo_signal, WAVELENGTH, delta, infl = index_meteor_in_rise, plot = True)
        self.fresnel_acceleration = fresnel_acceleration

        """

    def extract_i_q_meteor(self, start:str, end:str, file:files.File, plot:bool = False):

        start_dt = datetime.datetime.fromisoformat(f"{start}+00:00")
        end_dt = datetime.datetime.fromisoformat(f"{end}+00:00")

        shifted_pps = file.signal.pps.timestamps.get_s() - file.signal.pps.timestamps.get_s()[0]
        index_pps = file.signal.pps.index
        
        user_start = start_dt.timestamp()
        user_end = end_dt.timestamp()

        sample_user_start = round((user_start - file.wav.header.start_us / 1e6) * file.signal.samplerate)
    
        if sample_user_start < 0:
            return
        
        sample_user_end = round((user_end - file.wav.header.start_us / 1e6) * file.signal.samplerate)
        
        user_signal = file.signal.data[sample_user_start : sample_user_end + 1]
        
        filtered_user_signal, _ = filter_signal(user_signal, file.signal.samplerate, file.signal.beacon_frequency, FILTERING_HALF_RANGE_FREQUENCY, FILTERING_LENGTH_KERNEL)

        hilbert_user_signal = hilbert(filtered_user_signal)
        i_user_signal, q_user_signal = np.real(hilbert_user_signal), np.imag(hilbert_user_signal)

        user_ampl = np.sqrt(i_user_signal**2 + q_user_signal**2)

        ampl_sg_window_points = round(AMPL_SG_WINDOW_DURATION * file.signal.samplerate)
        user_ampl = apply_sg_smoothing(user_ampl, ampl_sg_window_points, SG_ORDER)
        
        index_meteor_peak = np.argmax(user_ampl)
        
        sample_meteor_start = sample_user_start + index_meteor_peak - round(PREPADDING_DURATION * file.signal.samplerate)
        sample_meteor_end = sample_user_start + index_meteor_peak + round(POSTPADDING_DURATION * file.signal.samplerate)
        
        meteor_signal = file.signal.data[sample_meteor_start : sample_meteor_end + 1]
        
        filtered_meteor_signal, self.frequency = filter_signal(meteor_signal, file.signal.samplerate, file.signal.beacon_frequency, FILTERING_HALF_RANGE_FREQUENCY, FILTERING_LENGTH_KERNEL)
            
        hilbert_meteor_signal = hilbert(filtered_meteor_signal)
        i_meteor_signal, q_meteor_signal = np.real(hilbert_meteor_signal), np.imag(hilbert_meteor_signal)

        samples_meteor = np.arange(sample_meteor_start, sample_meteor_end + 1)
        times = np.empty(len(meteor_signal))

        for i in range(len(meteor_signal)):

            times[i] = extrapolate_time(samples_meteor[i], shifted_pps, index_pps, file.signal.samplerate)


        if plot:

            meteor_ampl = np.sqrt(i_meteor_signal**2 + q_meteor_signal**2)

            plt.figure()
            plt.title(f" Amplitude curve - {file.system_code} ({file.type})")
            plt.plot(times, meteor_ampl/max(meteor_ampl))
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude [-]")
            plt.tight_layout()
            plt.grid(True)
            plt.show()

        return i_meteor_signal, q_meteor_signal, sample_meteor_start, times
    
    
def compute_t0_and_SNR(meteor_ampl, samplerate, times:np.array=None, plot:bool=False):

    ampl_sg_window_points = round(AMPL_SG_WINDOW_DURATION * samplerate)

    meteor_ampl = apply_sg_smoothing(meteor_ampl, ampl_sg_window_points, SG_ORDER)
    normalized_meteor_ampl = meteor_ampl/max(meteor_ampl)

    noise = np.arange(round(NOISE_DURATION * samplerate))
    mean_noise = np.mean(normalized_meteor_ampl[noise])

    index_global_max_ampl = np.argmax(normalized_meteor_ampl)
    index_ref_max_ampl = index_global_max_ampl

    local_indices_max_ampl, _ = find_peaks(normalized_meteor_ampl[noise[-1]:index_global_max_ampl], height = mean_noise + MIN_PEAK_HEIGHT_AMPL*(normalized_meteor_ampl[index_global_max_ampl] - mean_noise))

    if any(local_indices_max_ampl):
        index_ref_max_ampl = min(noise[-1] + local_indices_max_ampl)

    start_rise = -1
    condition_minimum = normalized_meteor_ampl[noise[-1]:index_ref_max_ampl+1] < mean_noise
    local_indices_minimum_ampl = np.where(condition_minimum)[0]

    if any(local_indices_minimum_ampl):
        start_rise = noise[-1] + local_indices_minimum_ampl[-1]
    
    else:
        start_rise = noise[-1]
        
    indices = np.arange(len(normalized_meteor_ampl))
    
    rise = np.where((indices <= index_global_max_ampl) & (indices >= start_rise))[0]  
    
    if (len(rise) == 0):
        print("No rise found")
        return
        
    start_exponential = index_global_max_ampl
    local_end_exponential = np.argmax(normalized_meteor_ampl[start_exponential:] < mean_noise)

    if local_end_exponential == 0:
        end_exponential = len(normalized_meteor_ampl)

    else:
        end_exponential = start_exponential + local_end_exponential

    exponential = np.arange(start_exponential, end_exponential)
            
    echo = np.concatenate((rise, exponential))
    not_echo = np.setdiff1d(indices, echo)

    index_meteor_in_rise = np.argmax(normalized_meteor_ampl[rise] >= (mean_noise + 0.42710125034355456*(normalized_meteor_ampl[index_ref_max_ampl] - 1*mean_noise)))
    index_meteor = index_meteor_in_rise + rise[0]

    index_meteor_end_rise = np.argmax(normalized_meteor_ampl[rise] >= (mean_noise + 0.56473319371993620*(normalized_meteor_ampl[index_ref_max_ampl] - 1*mean_noise)))
    index_meteor_beg_rise = np.argmax(normalized_meteor_ampl[rise] >= (mean_noise + 0.32282681346294560*(normalized_meteor_ampl[index_ref_max_ampl] - 1*mean_noise)))
    rise_duration = (index_meteor_end_rise - index_meteor_beg_rise)/samplerate

    if plot:

        # Plot split signal

        if times is None:

            times = np.arange(0, len(normalized_meteor_ampl), 1/samplerate)
            
        plt.figure()
        plt.plot(times[rise], normalized_meteor_ampl[rise], '.g', label = 'Rise')
        plt.plot(times[exponential], normalized_meteor_ampl[exponential], '.b', label = "Exponential")
        plt.plot(times[not_echo], normalized_meteor_ampl[not_echo], '.r', label = "Not echo")
        plt.plot(times[index_meteor], normalized_meteor_ampl[index_meteor], '*', markersize = 14, label = r'$t_{0}$')
        plt.plot(times[index_ref_max_ampl], normalized_meteor_ampl[index_ref_max_ampl], 'd', markersize = 14, label = 'Ref max')
        plt.axhline(y=normalized_meteor_ampl[rise[0]+index_meteor_end_rise], color='b', linestyle='--')
        plt.axhline(y=normalized_meteor_ampl[rise[0]+index_meteor_beg_rise], color='r', linestyle='--')
        plt.grid(True)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude [-]')
        plt.legend(loc='best')
        plt.title(f"Amplitude curve")          
        plt.tight_layout()
        plt.show()
        

    power_echo = np.max(normalized_meteor_ampl)**2
    power_noise = mean_noise**2
    SNR = 10*np.log10((power_echo-power_noise)/power_noise)


    if SNR < MINIMUM_SNR or rise_duration < MINIMUM_RISE_DURATION or rise_duration > MAXIMUM_RISE_DURATION or index_meteor_in_rise == 0:
        print("No meteor detected")
        return None
    
    return index_meteor, rise_duration, SNR

    
def detrend_doppler_shift(i_meteor_signal, q_meteor_signal, frequency, shifted_times):

    meteor_phase = np.arctan2(q_meteor_signal, i_meteor_signal)

    meteor_phase_unwrapped = np.unwrap(meteor_phase)
    corrected_meteor_phase = meteor_phase_unwrapped - (2 * np.pi * frequency * shifted_times)

    corrected_meteor_phase = apply_sg_smoothing(corrected_meteor_phase, PHASE_SG_WINDOW, SG_ORDER)

    return corrected_meteor_phase

    
def compute_pre_t0_speed(meteor_ampl, corrected_meteor_phase, index_meteor, samplerate:float, times:np.array=None, plot:bool = False):

    index_global_max_ampl = np.argmax(meteor_ampl)

    indices_minimum_phase, _ = find_peaks(-corrected_meteor_phase, prominence=PROMINENCE_PHASE)
    index_minimum_phase = find_closest_smaller(indices_minimum_phase, index_meteor)
    
    index_maximum_phase = index_meteor + np.argmax(corrected_meteor_phase[index_meteor:index_global_max_ampl+1])
    
    shifted_meteor_phase = corrected_meteor_phase - (corrected_meteor_phase[index_maximum_phase] - MAXIMUM_PHASE_VALUE)
    
    index_t0 = index_maximum_phase

    while shifted_meteor_phase[index_t0] > -np.pi/4:

        index_t0 = index_t0 - 1

        if index_t0 <= 0:

            return
    
    if abs(shifted_meteor_phase[index_t0] + np.pi/4) > abs(shifted_meteor_phase[index_t0] + np.pi/4):

        index_t0 = index_t0 + 1
        
    if (index_t0 <= index_minimum_phase):
        print("Index_t0 < Index_minimum_phase")
        return
    
    cropped_meteor_phase = shifted_meteor_phase[index_minimum_phase : index_maximum_phase + 1]
        
    if plot:

        if times is None:

            times = np.arange(0, len(corrected_meteor_phase), 1/samplerate)

        plt.figure()
        plt.title(f"Cropped phase")
        plt.plot(times[index_minimum_phase : index_maximum_phase+1], cropped_meteor_phase, color = 'red')
        plt.ylabel("Phase [rad]")
        plt.xlabel("Time [s]")
        plt.grid(True)
        plt.show() 

    fresnel_parameters_to_maximum_phase = np.linspace(MINIMUM_FRESNEL_PARAMETER, FRESNEL_PARAMETER_AT_MAXIMUM_PHASE, NUMBER_FRESNEL_PARAMETERS)
    
    fresnel_reference_point = -0.5 - 0.5j
    
    fresnel_sine, fresnel_cosine = fresnel(fresnel_parameters_to_maximum_phase)
    fresnel_integral = fresnel_cosine + 1j * fresnel_sine
    fresnel_phase = np.unwrap(np.angle(fresnel_integral - fresnel_reference_point))    
    fresnel_phase = -fresnel_phase
    
    index_maximum_fresnel_phase = np.argmax(fresnel_phase)
    fresnel_phase = fresnel_phase - (fresnel_phase[index_maximum_fresnel_phase] - MAXIMUM_PHASE_VALUE)
    
    cropped_fresnel_parameters = interp1d(fresnel_phase, fresnel_parameters_to_maximum_phase, kind = 'linear', fill_value = 'extrapolate')(cropped_meteor_phase)
    
    index_knee = find_knee(cropped_fresnel_parameters) + index_minimum_phase
    
    if plot:
        
        normalized_meteor_ampl = meteor_ampl/np.max(meteor_ampl)

        fig, ax = plt.subplots()
        twin = ax.twinx()
        plt.title(f"Phase and amplitude around knee")
        plt.xlabel("Time [s]")
        plt.grid(True)
        p1, = ax.plot(times[index_knee-2000:index_knee+2000], corrected_meteor_phase[index_knee-2000:index_knee+2000], label = "Phase", color = 'red')
        ax.set_ylabel("Phase [rad]")
        p2, = twin.plot(times[index_knee-2000:index_knee+2000], normalized_meteor_ampl[index_knee-2000:index_knee+2000], label = "Amplitude", color = 'blue')
        twin.set_ylabel("Amplitude [-]")
        plt.legend(handles=[p1, p2])
        plt.grid(True)
        plt.show()
    
    minimum_meteor_cropped_phase, index_minimum_meteor_cropped_phase = np.min(cropped_meteor_phase), np.argmin(cropped_meteor_phase)
    
    if minimum_meteor_cropped_phase > MINIMUM_CROPPED_PHASE_VALUE or index_minimum_meteor_cropped_phase > 0: 
        
        print("No pre-t0 speed detected")
        return
    
    offsets_minimum_phase = np.arange(NUMBER_OFFSETS_AFTER_MINIMUM_PHASE+1)
    v_pseudo_pre_t0s = np.zeros((len(offsets_minimum_phase),))
    r_value_pre_t0s = np.zeros((len(offsets_minimum_phase),))
    indices_t0 = np.zeros((len(offsets_minimum_phase),), dtype = np.int32)

    for i in range(len(offsets_minimum_phase)):

        offset_minimum_phase = offsets_minimum_phase[i]

        try:

            r_value_pre_t0s[i], v_pseudo_pre_t0s[i], indices_t0[i] = get_pre_t0_speed_correlation(index_knee, index_minimum_phase + offset_minimum_phase, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase)
        
        except:

            continue

    if not r_value_pre_t0s.size or max(r_value_pre_t0s) < MINIMUM_r_value_pre_t0:
        print("Too small pre-t0 correlation")
        return
    
    r_value_pre_t0, best_r_value_pre_t0_index = np.max(r_value_pre_t0s), np.argmax(r_value_pre_t0s)
    v_pseudo_pre_t0 = v_pseudo_pre_t0s[best_r_value_pre_t0_index]
    
    print("Pre-t0 speed succesfully determined !")
    print("Pre-t0 pseudo speed = ", v_pseudo_pre_t0)

    best_index_t0 = indices_t0[best_r_value_pre_t0_index]
    best_index_minimum_phase = index_minimum_phase + offsets_minimum_phase[best_r_value_pre_t0_index]
    index_meteor_pre_t0 = best_index_t0

    #best_fresnel_std, best_v_pseudo_pre_t0, best_median_r_value_pre_t0, best_index_t0, best_peak_index = check_pre_t0_speed_histograms_pssst(index_minimum_phase+offsets_minimum_phase, indices_t0, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase) 

    best_fresnel_std, best_v_pseudo_pre_t0, best_median_r_value_pre_t0, best_index_t0, best_peak_index = check_pre_t0_speed_histograms_pssst([best_index_minimum_phase], [best_index_t0], shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase) 

    print("Pre-t0 psst pseudo speed = ", best_v_pseudo_pre_t0)
    print("Pre-t0 psst pseudo speed std = ", best_fresnel_std)
    print("Pre-t0 psst std/speed = ", best_fresnel_std/best_v_pseudo_pre_t0)

    if plot:
        plt.figure()
        plt.title(f"Best phase curve")
        plt.plot(times[best_index_minimum_phase : best_index_t0], corrected_meteor_phase[best_index_minimum_phase : best_index_t0], color = 'red')
        plt.ylabel("Phase [rad]")
        plt.xlabel("Time [s]")
        plt.grid(True)
        plt.show() 


    return index_meteor_pre_t0, v_pseudo_pre_t0, r_value_pre_t0 

    
def get_pre_t0_speed_correlation(index_meteor, index_minimum_phase, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase): 

    v_pseudo_pre_t0s = np.array([])
    r_value_pre_t0s = np.array([])
    indices_t0 = np.array([], dtype = np.int32)
    
    index_t0_guesses = np.arange(index_meteor - NUMBER_OFFSETS_AROUND_T0, index_meteor + NUMBER_OFFSETS_AROUND_T0 + 1)
    
    for index_t0_guess in index_t0_guesses:
        
        if index_t0_guess - index_minimum_phase + 1 < MINIMUM_LENGTH_SLIDING_SLOPE:
            continue
        
        sliding_slope_meteor_phase = shifted_meteor_phase[index_minimum_phase:index_t0_guess+1]
        sliding_slope_meteor_phase = sliding_slope_meteor_phase - sliding_slope_meteor_phase[-1] - np.pi/4
        
        if min(sliding_slope_meteor_phase) > MINIMUM_CROPPED_PHASE_VALUE:
            continue
                    
        sliding_slope_times = times[index_minimum_phase:index_t0_guess+1]
        
        try:
            sliding_slope_fresnel_parameters = interp1d(fresnel_phase, fresnel_parameters_to_maximum_phase, kind = 'linear', fill_value = 'extrapolate')(sliding_slope_meteor_phase)
        except:
            print('Lack of points making the interpolation impossible. Probably due to a decreasing phase curve.')
            continue
        
        sliding_slope_fresnel_distance = sliding_slope_fresnel_parameters*np.sqrt(WAVELENGTH/2) 
                    
        speed, _, r_value_pre_t0, _, _ = stats.linregress(sliding_slope_times, sliding_slope_fresnel_distance)

        v_pseudo_pre_t0s = np.append(v_pseudo_pre_t0s, speed)
        r_value_pre_t0s = np.append(r_value_pre_t0s, r_value_pre_t0)
        indices_t0 = np.append(indices_t0, index_t0_guess)

    best_r_value_pre_t0, best_r_value_pre_t0_index = np.max(r_value_pre_t0s), np.argmax(r_value_pre_t0s)
    best_v_pseudo_pre_t0 = v_pseudo_pre_t0s[best_r_value_pre_t0_index]
    best_index_t0 = indices_t0[best_r_value_pre_t0_index]

    return best_r_value_pre_t0, best_v_pseudo_pre_t0, best_index_t0
                
      
def check_pre_t0_speed_histograms_pssst(indices_start_phase, indices_t0, shifted_meteor_phase, times, fresnel_phase, fresnel_parameters_to_maximum_phase):
    
    best_v_pseudo_pre_t0s = np.array([])
    std_v_pseudo_pre_t0s = np.array([])
    median_r_value_pre_t0s = np.array([])
    
    peak_indices = np.arange(0, len(indices_start_phase))
            
    for i in range(len(indices_start_phase)):
        
        index_start_phase = indices_start_phase[i]
        index_t0 = indices_t0[i]

        if index_t0 - index_start_phase + 1 < MINIMUM_LENGTH_SLIDING_SLOPE:
            continue
            
        sliding_slope_meteor_phase = shifted_meteor_phase[index_start_phase:index_t0+1]
        sliding_slope_meteor_phase = sliding_slope_meteor_phase - sliding_slope_meteor_phase[-1] - np.pi/4
                    
        sliding_slope_times = times[index_start_phase:index_t0+1]
        
        try:
            sliding_slope_fresnel_parameters = interp1d(fresnel_phase, fresnel_parameters_to_maximum_phase, kind = 'linear', fill_value = 'extrapolate')(sliding_slope_meteor_phase)
        except:
            print('Lack of points making the interpolation impossible. Probably due to a decreasing phase curve.')
            continue
        
        sliding_slope_fresnel_distance = sliding_slope_fresnel_parameters*np.sqrt(WAVELENGTH/2) 
                    
        maximum_window_length = len(sliding_slope_meteor_phase)
        minimum_window_length = 2 #maximum_window_length - NUMBER_WINDOWS_SLIDING_SLOPE + 1 
        
        window_lengths = np.arange(minimum_window_length, maximum_window_length+1)
        
        v_pseudo_pre_t0_histogram = np.array([])
        fresnel_intercept_histogram = np.array([])
        r_value_pre_t0s = np.array([])
        
        for window_length in window_lengths:
            
            for window_start in range(maximum_window_length-window_length+1):
                
                window_fresnel_distance = sliding_slope_fresnel_distance[window_start:window_start+window_length]
                window_times = sliding_slope_times[window_start:window_start+window_length]
                
                window_speed, window_intercept, window_r_value_pre_t0, _, _ = stats.linregress(window_times, window_fresnel_distance)
                
                if (window_r_value_pre_t0 > MINIMUM_r_value_pre_t0):
                    v_pseudo_pre_t0_histogram  = np.append(v_pseudo_pre_t0_histogram, window_speed)
                    fresnel_intercept_histogram = np.append(fresnel_intercept_histogram, window_intercept)
                    r_value_pre_t0s = np.append(r_value_pre_t0s, window_r_value_pre_t0)

        if len(v_pseudo_pre_t0_histogram) >= MINIMUM_SIZE_HISTOGRAM:

            kde_speeds, kde_speed_density = FFTKDE(kernel = 'gaussian', bw = 'scott').fit(v_pseudo_pre_t0_histogram).evaluate()

            # Find the maximum value of the KDE
            kde_max = np.max(kde_speed_density)

            # Compute half of the maximum (Half Maximum)
            half_max = kde_max / 2

            # Find the points where KDE crosses the half-max (FWHM)
            indices_above_half_max = np.where(kde_speed_density >= half_max)[0]

            # The FWHM is the distance between the first and last points where the KDE is above the half-max
            fwhm = kde_speeds[indices_above_half_max[-1]] - kde_speeds[indices_above_half_max[0]]
            
            peak_speeds_indices, _ = find_peaks(kde_speed_density, height = (None, None))
            peak_speeds = kde_speeds[peak_speeds_indices]
            
            peak_intercepts = np.array([])
            
            for peak_speed in peak_speeds:

                closest_intercept_indices = find_closest_indices(fresnel_intercept_histogram, peak_speed, POINTS_AROUND_HISTOGRAM_PEAK)
                cropped_fresnel_intercept_histogram = fresnel_intercept_histogram[closest_intercept_indices]
                
                kde_intercepts, kde_intercept_density = FFTKDE(kernel = 'gaussian', bw = 'scott').fit(cropped_fresnel_intercept_histogram).evaluate()
                peak_intercepts_indices, peak_intercepts_dict = find_peaks(kde_intercept_density, height = (None, None))
                peak_intercepts_heights = peak_intercepts_dict['peak_heights']       
                highest_peak_intercepts_index = peak_intercepts_indices[np.argmax(peak_intercepts_heights)]
                peak_intercepts = np.append(peak_intercepts, kde_intercepts[highest_peak_intercepts_index])
                
            residual_intercepts = abs(peak_intercepts + peak_speeds*times[index_t0])
            best_intercept_index = np.argmin(residual_intercepts)
            
            best_v_pseudo_pre_t0s = np.append(best_v_pseudo_pre_t0s, peak_speeds[best_intercept_index])
            std_v_pseudo_pre_t0s = np.append(std_v_pseudo_pre_t0s, np.std(v_pseudo_pre_t0_histogram))
            median_r_value_pre_t0s = np.append(median_r_value_pre_t0s, np.median(r_value_pre_t0s))
            
            
    final_std_v_pseudo_pre_t0, index_minimum_std_v_pseudo_pre_t0s = np.min(std_v_pseudo_pre_t0s), np.argmin(std_v_pseudo_pre_t0s)
    final_v_pseudo_pre_t0 = best_v_pseudo_pre_t0s[index_minimum_std_v_pseudo_pre_t0s]
    final_median_r_value_pre_t0 = median_r_value_pre_t0s[index_minimum_std_v_pseudo_pre_t0s]
    
    final_index_t0 = indices_t0[index_minimum_std_v_pseudo_pre_t0s]
    final_peak_index = peak_indices[index_minimum_std_v_pseudo_pre_t0s]

    return final_std_v_pseudo_pre_t0, final_v_pseudo_pre_t0, final_median_r_value_pre_t0, final_index_t0, final_peak_index   
    
    
def filter_signal(signal, samplerate, beacon_frequency, FILTERING_HALF_RANGE_FREQUENCY, FILTERING_LENGTH_KERNEL):
    # Filter signal
    
    real_fft_signal = np.fft.rfft(signal, len(signal)) / len(signal)
    real_fft_signal_freq = np.fft.rfftfreq(len(signal), d = 1 / samplerate)
    
    indices_signal_range = np.argwhere( (real_fft_signal_freq >= beacon_frequency - IDENTIFICATION_HALF_RANGE_FREQUENCY) &
                                        (real_fft_signal_freq <= beacon_frequency + IDENTIFICATION_HALF_RANGE_FREQUENCY)
                                        )
    
    real_fft_signal = real_fft_signal[indices_signal_range]
    real_fft_signal_freq = real_fft_signal_freq[indices_signal_range]
    signal_index = np.argmax(abs(real_fft_signal))
    
    signal_frequency = real_fft_signal_freq[signal_index][0]

        
    signal_fc_low = (signal_frequency + FILTERING_HALF_RANGE_FREQUENCY) / samplerate
    signal_fc_high = (signal_frequency - FILTERING_HALF_RANGE_FREQUENCY) / samplerate
    
    filtered_signal = apply_blackman_filter(signal, signal_fc_low, signal_fc_high, FILTERING_LENGTH_KERNEL)

    return filtered_signal, signal_frequency
    
    
def apply_blackman_filter(signal, fc_low, fc_high, N):
    # Filter signal with a band-pass Blackman filter

    if N%2 == 0:
        N = N+1
    
    n = np.arange(N)

    # Low-pass Blackman filter
    low_blackman_filter = np.sinc(2 * fc_low * (n - (N - 1) / 2.)) * blackman(N)
    low_blackman_filter = low_blackman_filter / np.sum(low_blackman_filter)

    # High-pass Blackman filter
    high_blackman_filter = np.sinc(2 * fc_high * (n - (N - 1) / 2.)) * blackman(N)
    high_blackman_filter = high_blackman_filter / np.sum(high_blackman_filter)
    high_blackman_filter = -high_blackman_filter  # Convert to high-pass
    high_blackman_filter[int(np.floor(N / 2))] = high_blackman_filter[int(np.floor(N / 2))] + 1

    # Convolution between high-pass and low-pass filters
    blackman_filter = np.convolve(low_blackman_filter, high_blackman_filter)

    b = blackman_filter
    a = np.array([1.])

    filtered_signal_blackman = filtfilt(b, a, signal, axis=0, padtype='odd')

    return filtered_signal_blackman
    

def apply_sg_smoothing(array, window, order, deriv = 0, mode = 'mirror'):

    if window > order:

        return savgol_filter(array, window, order, deriv = deriv, mode = mode)
    
    return array
 

def extrapolate_time(sample, timestamps, sample_numbers, fs):
    # Find the time corresponding to the determined sample

    index = find_nearest(sample_numbers, sample)
    closest_timestamp = timestamps[index]
    time = closest_timestamp + (sample - sample_numbers[index]) / fs
    return time
    

def find_closest_smaller(arr, value):
    limit = float('-inf')
    closest = -1
    for num in arr:
        if num < value and num > limit:
            closest = num
    return closest
    

def find_nearest(array, value):
    return (np.abs(array - value)).argmin() 
    
    
def find_closest_indices(array, value, n):

    # Calculate the absolute differences between the array elements and the value
    absolute_diff = np.abs(array - value)

    # Sort the absolute differences and get the indices of the sorted elements
    sorted_indices = np.argsort(absolute_diff)

    # Return the first n indices
    return sorted_indices[:n]
    
    
def find_knee(signal):
    residual = np.zeros(len(signal)-1)
    for i in range (len(signal)-1):
        signal1, signal2 = np.split(signal, [i+1])
        sse1, sse2 = sum_squared_diff(signal1), sum_squared_diff(signal2)
        residual[i] = sse1 + sse2
    index_knee = np.argmin(residual) + 1
    return index_knee

    
def sum_squared_diff(signal):
    x = np.arange(len(signal))
    y = signal
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = m*x + c
    deviation = np.sum((y - y_pred)**2)
    return deviation
    

def compute_doppler_shift(times, start_rise, end_rise, meteor_signal, meteor_frequency, plot):
        
    time_crossings = find_zero_crossings(times, meteor_signal)
            
    number_crossings = len(time_crossings)
    NUMBER_PERIODS_AVERAGE = 20
    number_crossings_average = 2*NUMBER_PERIODS_AVERAGE + 1
    number_doppler_average = number_crossings - number_crossings_average + 1
    
    time_crossings_average = np.zeros(number_doppler_average)
    doppler_shift_average = np.zeros(number_doppler_average)

    for i in range(number_doppler_average):
        time_crossings_average[i] = np.mean(time_crossings[i : i+number_crossings_average])
        doppler_shift_average[i] = (number_crossings_average-1) / (2 * (time_crossings[i+number_crossings_average-1]-time_crossings[i] ))
            
    doppler_shift = 1/(2*np.gradient(time_crossings))
    
    if plot:
        plt.figure()
        plt.plot(time_crossings, doppler_shift)
        plt.plot(time_crossings_average, doppler_shift_average)
        plt.show()
    
    TIME_SPAN_DOPPLER = 0.2
    MINIMUM_DOPPLER_SHIFT = 30
    
    time_start_rise = times[start_rise]
    time_end_rise = times[end_rise]
    
    index_start_rise_average = np.argmin(abs(time_crossings_average - time_start_rise))
    index_end_rise_average = np.argmin(abs(time_crossings_average - time_end_rise))
         
    index_start_doppler = index_start_rise_average + np.argmax(doppler_shift_average[index_start_rise_average : index_end_rise_average+1])
    time_start_doppler = time_crossings_average[index_start_doppler]
    index_end_doppler = np.argmin(abs(time_crossings_average - (time_start_doppler + TIME_SPAN_DOPPLER)))

    time_crossings_average_crop = time_crossings_average[index_start_doppler : index_end_doppler+1]
    doppler_shift_average_crop = doppler_shift_average[index_start_doppler : index_end_doppler+1]
    
    if plot:
        plt.figure()
        plt.plot(time_crossings_average_crop, doppler_shift_average_crop)
        plt.show()
        
    index_end_fit = np.where(doppler_shift_average_crop < meteor_frequency + MINIMUM_DOPPLER_SHIFT)[0][0]
    index_start_fit = 1
    
    time_crossings_average_fit = time_crossings_average_crop[index_start_fit:index_end_fit]
    doppler_shift_average_fit = doppler_shift_average_crop[index_start_fit:index_end_fit]
    
    if plot:
        plt.figure()
        plt.plot(time_crossings_average_fit, doppler_shift_average_fit)
        plt.show()
            

def find_zero_crossings(times, signal):
    idx = np.where(signal[1:] * signal[:-1] < 0)[0]
    time_crossings = np.zeros(len(idx))
    
    for i, j in enumerate(idx):
        time_crossings[i] = np.interp(0.0, signal[j:j+2], times[j:j+2])      
        
    return time_crossings

