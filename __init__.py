"""
Created on Fri Aug  5 09:16:23 2016

@author: mittelberger
"""

# standard libraries
try:
    from nion.swift.model import HardwareSource
    from Camera import CameraHardwareSource
except:
    pass
from . import temperature
from . import TemperatureCameraManagerImageSource

def register_camera(hardware_source_id, display_name):
    # create the camera
    camera = temperature.Camera()
    # create the hardware source
    camera_adapter = TemperatureCameraManagerImageSource.CameraAdapter(hardware_source_id, display_name, camera)
    hardware_source = CameraHardwareSource.CameraHardwareSource(camera_adapter, None)
    hardware_source.modes = camera_adapter.modes
    # register it with the manager
    HardwareSource.HardwareSourceManager().register_hardware_source(hardware_source)

register_camera('temperature_sensor', 'temperature sensor')