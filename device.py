# Part 1: IoT Device Emulation (25 %)
# ◆ Device Classes: Create Python classes for each type of IoT device you
# want to simulate, such as SmartLight, Thermostat, and
# SecurityCamera. Each class should have attributes like device ID,
# status (on/off), and relevant properties (e.g., temperature for
# thermostats, brightness for lights, and security status for cameras).
# ◆ Device Behavior: Implement methods for each device class that allows
# for turning devices on/off and changing their properties. Simulate
# realistic behavior, such as gradual dimming for lights or setting
# temperature ranges for thermostats.
from datetime import datetime
import random

class Device:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = False  # Default to off for all devices

    def turn_on(self):
        self.status = True

    def turn_off(self):
        self.status = False

class SmartLight(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.brightness = 0

    def set_brightness(self, brightness):
        if self.status:  # Only allow changes if the light is on
            self.brightness = brightness

class Thermostat(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.temperature = 15

    def set_temperature(self, temperature):
        if self.status:  # Only allow changes if the thermostat is on
            self.temperature = temperature


class SecurityCamera(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.motion_detected = False 

    def detect_motion(self):
        if self.status:  # Only detect motion if the camera is on
            self.motion_detected = random.choice([True, False])
        else:
            self.motion_detected = False  # No motion detected if the camera is off