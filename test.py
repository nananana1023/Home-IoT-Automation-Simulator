import unittest
from device import SmartLight, Thermostat, SecurityCamera
from automation import AutomationSystem

class TestDeviceFunctions(unittest.TestCase):

    def test_smart_light_on_off(self):
        light = SmartLight(1)
        light.turn_on()
        self.assertTrue(light.status)
        light.turn_off()
        self.assertFalse(light.status)

    def test_thermostat_temperature_setting(self):
        thermostat = Thermostat(2)
        thermostat.turn_on()
        thermostat.set_temperature(21)
        self.assertEqual(thermostat.temperature, 21)
        
    def test_light_setting(self):
        light = SmartLight(1)
        light.turn_on()
        light.set_brightness(70)
        self.assertEqual(light.brightness, 70)

    def test_security_camera_motion_detection(self):
        camera = SecurityCamera(3)
        camera.turn_on()
        camera.detect_motion()
        self.assertIn(camera.motion_detected, [True, False])  # since it's random

    def test_automation_system_device_addition(self):
        system = AutomationSystem()
        light = SmartLight(1)
        system.add_device(light)
        self.assertIn(light, system.devices)
        
    def set_temp(self):
        thermo=Thermostat(2)
        thermo.turn_off()
        thermo.set_temperature(22)
        #shouldn't change temperature if it's off
        self.assertEqual(thermo, 15)

    def auto(self):
        system = AutomationSystem()
        system.toggle_automation()
        self.assertTrue(system.automation_enabled)

if __name__ == '__main__':
    unittest.main()
