import random
import time
from datetime import datetime
from device import SmartLight, Thermostat, SecurityCamera

class AutomationSystem:
    def __init__(self):
        self.devices = []
        self.automation_enabled = False  # Track whether automation is enabled

    def add_device(self, device):
        self.devices.append(device)

    def simulate_sensor_data(self):
        # Randomly change sensor data for each device
        for device in self.devices:
            if isinstance(device, SmartLight) and device.status:
                new_brightness = random.randint(0, 100)
                device.set_brightness(new_brightness)
                self.log_sensor_data(device, 'Brightness', new_brightness)
            elif isinstance(device, Thermostat) and device.status:
                new_temperature = random.randint(10, 30)
                device.set_temperature(new_temperature)
                self.log_sensor_data(device, 'Temperature', new_temperature)
            elif isinstance(device, SecurityCamera) and device.status:
                device.detect_motion()
                self.log_sensor_data(device, 'Motion Detected', 'Yes' if device.motion_detected else 'No')

    def execute_automation_tasks(self):
        # Activating lights automatically when motion is detected.
        messages = []
        for device in self.devices:
            if isinstance(device, SecurityCamera) and device.motion_detected:
                for light in self.devices:
                    if isinstance(light, SmartLight) and not light.status:  # Check if light is off
                        light.turn_on()
                        light.set_brightness(100)
                        self.log_sensor_data(light, 'Brightness', '100')
                        messages.append("Turned on lights automatically when motion is detected.")
            #turn on camera if light is less than 50 
            elif isinstance(device, SmartLight) and device.brightness < 50:
                for camera in self.devices:
                    if isinstance(camera, SecurityCamera) and not camera.status:  # Check if camera is off
                        camera.turn_on()
                        self.log_sensor_data(camera, 'Status', 'On')
                        messages.append("Turned on security camera when light brightness is less than 50.")
        for message in messages:
            self.show_messages(message)

    def log_sensor_data(self, device, property_name, value):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = f"{timestamp} {device.device_id} {type(device).__name__} Status: {'On' if device.status else 'Off'} {property_name}: {value}\n"
        with open("sensor_data.txt", "a") as file:
            file.write(data)
    
    def show_message(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = f"{timestamp} {message}\n"
        with open("sensor_data.txt", "a") as file:
            file.write(data)
    
    def toggle_automation(self):
        self.automation_enabled = not self.automation_enabled

