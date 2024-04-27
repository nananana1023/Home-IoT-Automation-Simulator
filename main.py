import tkinter as tk
import random
import threading
import time
from datetime import datetime
from device import SmartLight, Thermostat, SecurityCamera
from automation import AutomationSystem

# Clear the sensor_data.txt file at the start of the program
with open("sensor_data.txt", "w") as file:
    file.truncate(0)

# Create the main window
root = tk.Tk()
root.title("Smart Home IoT Simulator")

# Create the Automation System instance
automation_system = AutomationSystem()
# Adding devices to the system
automation_system.add_device(SmartLight(1))
automation_system.add_device(Thermostat(2))
automation_system.add_device(SecurityCamera(3))

# Functions to handle device interaction
def toggle_device(device):
    if device.status:
        if isinstance(device, SmartLight):
            device.set_brightness(0)  # Reset brightness to 0
            device.turn_off()
            automation_system.log_sensor_data(device, 'Brightness', '0')  
        elif isinstance(device, Thermostat):
            device.set_temperature(15)  # Reset temperature to 15C
            device.turn_off()
            automation_system.log_sensor_data(device, 'Temperature', '15')  
        elif isinstance(device, SecurityCamera):
            device.turn_off()
            automation_system.log_sensor_data(device, 'Motion detected', 'No') 
    else:
        device.turn_on()
        if isinstance(device, SmartLight):
            device.set_brightness(100)  # Set default brightness to 100
            automation_system.log_sensor_data(device, 'Brightness', '100')  
        elif isinstance(device, Thermostat):
            device.set_temperature(23)  # Set default temperature 
            automation_system.log_sensor_data(device, 'Temperature', '23') 
        elif isinstance(device, SecurityCamera):
            automation_system.log_sensor_data(device, 'Motion detected', 'Yes' if device.motion_detected else 'No') 

def set_brightness(device, brightness):
    if device.status:
        brightness = int(brightness)
        device.set_brightness(brightness)
        automation_system.log_sensor_data(device, 'Brightness', brightness)
    
   
def set_temperature(device, temperature):
    if device.status:
        temperature = int(temperature)
        device.set_temperature(temperature)
        automation_system.log_sensor_data(device, 'Temperature', temperature)

def random_detect_motion(device):
    if device.status:
        device.detect_motion()
        automation_system.log_sensor_data(device, 'Motion Detected', 'Yes' if device.motion_detected else 'No')
    
def run_automation_loop():
    while True:
        if automation_system.automation_enabled:
            automation_system.simulate_sensor_data()
            automation_system.execute_automation_tasks()
            time.sleep(3)  # Wait for 3 seconds
        else:
            time.sleep(1)  # Short sleep to prevent busy waiting

def start_automation_loop():
    # Correctly pass the function without calling it
    automation_thread = threading.Thread(target=run_automation_loop)
    automation_thread.daemon = True
    automation_thread.start()

    
# Add a button to toggle automation
def toggle_automation():
    automation_system.toggle_automation()
    # Update the button text based on the state of automation
    automation_button.config(text=f"Automation {'ON' if automation_system.automation_enabled else 'OFF'}")
    if automation_system.automation_enabled:
        start_automation_loop()

def update_file_display():
    with open("sensor_data.txt", "r") as file:
        file_contents = file.read()
    file_display_text.delete(1.0, tk.END)
    file_display_text.insert(tk.END, file_contents)
    # Schedule this function to run again after 1000 milliseconds (1 second)
    root.after(1000, update_file_display)

# Define the GUI elements
controls_frame = tk.Frame(root)
controls_frame.pack(side=tk.LEFT, padx=20, pady=20)

automation_button = tk.Button(root, text="Automation OFF", command=toggle_automation)
automation_button.pack()

brightness_var = tk.DoubleVar()
brightness_scrollbar = tk.Scale(controls_frame, from_=0, to=100, orient='horizontal', label='Brightness', variable=brightness_var, command=lambda v: set_brightness(automation_system.devices[0], v))
brightness_scrollbar.pack()

temperature_var = tk.DoubleVar()
temperature_scrollbar = tk.Scale(controls_frame, from_=10, to=30, orient='horizontal', label='Temperature', variable=temperature_var, command=lambda v: set_temperature(automation_system.devices[1], v))
temperature_scrollbar.pack()

toggle_light_button = tk.Button(controls_frame, text="Toggle Light", command=lambda: toggle_device(automation_system.devices[0]))
toggle_light_button.pack()

toggle_thermostat_button = tk.Button(controls_frame, text="Toggle Thermostat", command=lambda: toggle_device(automation_system.devices[1]))
toggle_thermostat_button.pack()

toggle_camera_button = tk.Button(controls_frame, text="Toggle Camera", command=lambda: toggle_device(automation_system.devices[2]))
toggle_camera_button.pack()

random_motion_button = tk.Button(controls_frame, text="Random Detect Motion", command=lambda: random_detect_motion(automation_system.devices[2]))
random_motion_button.pack()

# Create a frame for file display
file_display_frame = tk.Frame(root)
file_display_frame.pack(side=tk.BOTTOM, padx=40, pady=40)

# Create a text widget for displaying the file contents
file_display_text = tk.Text(file_display_frame, width=70, height=30)
file_display_text.pack()

# Initialize the periodic file display update
update_file_display()
root.mainloop()
