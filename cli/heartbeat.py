import time
from collections import deque

import heartpy
import numpy as np


class HeartRateCalculator:

    def __init__(self, buffer_size=500, computation_interval=5.0, min_samples=150):
        self.ppg_buffer = deque(maxlen=buffer_size)
        self.timestamps = deque(maxlen=buffer_size)
        self.last_computation = time.time()
        self.computation_interval = computation_interval
        self.min_samples = min_samples
        self.current_bpm = 0.0

    def add_sample(self, ppg_value, timestamp=None):
        if timestamp is None:
            timestamp = time.time()

        self.ppg_buffer.append(ppg_value)
        self.timestamps.append(timestamp)

    def should_compute(self):
        current_time = time.time()
        return (current_time - self.last_computation >= self.computation_interval and
                len(self.ppg_buffer) >= self.min_samples)

    def compute_heart_rate(self):
        if not self.should_compute():
            return None

        try:
            # Convert buffer to numpy array and scale data
            ppg_data = np.array(list(self.ppg_buffer), dtype=float)

            # Calculate sample rate using heartpy's mstimer function
            timerdata = np.array(list(self.timestamps), dtype=float) * 1000.0
            sample_rate = heartpy.get_samplerate_mstimer(timerdata)

            # Filter out signal noise
            filtered_data = heartpy.filter_signal(
                ppg_data,
                cutoff = [0.8, 2.5],
                sample_rate = sample_rate,
                filtertype = 'bandpass',
                order = 3
            )

            # Scale filtered data
            scaled_data = heartpy.scale_data(filtered_data)

            # Process with HeartPy
            working_data, measures = heartpy.process(
                scaled_data,
                sample_rate,
                report_time=False
            )

            # Update internal state
            self.current_bpm = measures['bpm']
            self.last_computation = time.time()

            return measures

        except Exception as e:
            print(f"Heart rate analysis failed: {e}")
            return None

    def get_current_bpm(self):
        return self.current_bpm

    def reset(self):
        self.ppg_buffer.clear()
        self.timestamps.clear()
        self.last_computation = time.time()
        self.current_bpm = 0.0

    def get_buffer_size(self):
        return len(self.ppg_buffer)

    def is_ready(self):
        return len(self.ppg_buffer) >= self.min_samples