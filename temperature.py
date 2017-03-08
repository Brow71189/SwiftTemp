# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 12:59:33 2016

@author: Andi
"""
import time
import subprocess
import numpy as np

ssh_path = 'C:/cygwin64/bin/ssh.exe'
raspiname = 'pwmraspi'

class Camera():
    def __init__(self, **kwargs):
        self.mode = 'Run'
        self.mode_as_index = 0
        self.exposure_ms = 0
        self.binning = 1
        self.sensor_dimensions = (1,512)
        self.readout_area = self.sensor_dimensions
        self.frame_number = 0
        self.temperature_data = [[], []]

    def set_exposure_ms(self, exposure_ms, mode_id):
        self.exposure_ms = exposure_ms

    def get_exposure_ms(self, mode_id):
        return self.exposure_ms

    def set_binning(self, binning, mode_id):
        self.binning = binning

    def get_binning(self, mode_id):
        return self.binning

    def start_live(self):
        pass

    def stop_live(self):
        pass

    def acquire_image(self):
        time.sleep(0.5)
        res = subprocess.run([ssh_path, raspiname, 'vcgencmd', 'measure_temp'],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        temperature_string = res.stdout.decode()
        temperature = float(temperature_string[5:9])
        self.temperature_data[0].append(temperature)
        self.temperature_data[1].append(temperature+1)
        data_element = {}
        data_element['data'] = np.array(self.temperature_data)
        data_element['properties'] = {'spatial_calibrations': [{'offset': 0, 'scale': 1, 'units': None}]*2,
                                      'intensity_calibration': {'offset': 0, 'scale': 1, 'units': '°C'},
                                      'frame_number': self.frame_number}
        data_element['datum_dimension_count'] =  1
        data_element['collection_dimension_count'] = 1
        data_element['is_sequence'] = False
        self.frame_number += 1
        return data_element

    def acquire_sequence(self, n):
        raise NotImplementedError

    def open_monitor(self):
        raise NotImplementedError

    def open_configuration_interface(self):
        raise NotImplementedError