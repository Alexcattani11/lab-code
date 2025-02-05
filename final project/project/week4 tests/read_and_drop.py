"""
Program to read the color of the delivery zone and drop the corresponding cube
"""

from utils.brick import Motor, TouchSensor, BP, wait_ready_sensors, EV3ColorSensor 
from utils.emergency_stop import ES
from colors import get_color
import time

#Initialize sensors
stopsensor = TouchSensor(1)
slidemotor = Motor("B")
pushmotor = Motor("C")
zone_color_sensor = EV3ColorSensor(2)

POWER_LIMIT = 40       # Power limit (percentage)
SPEED_LIMIT = 360      # Speed limit in degree per second

slidemotor.reset_encoder()                      # Reset encoder to 0 value
slidemotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
slidemotor.set_power(0)

pushmotor.reset_encoder()                      # Reset encoder to 0 value
pushmotor.set_limits(POWER_LIMIT, SPEED_LIMIT) # Set the power and speed limits
pushmotor.set_power(0)

wait_ready_sensors(True)
print("Done waiting.")

# amount we need to move to get to next position
step = 98.3

# We changed the initial position to be yellow because that makes the weight distribution better
cube_positions = {
    "red": -196.60,
    "orange": -98.3,
    "yellow": 0,
    "green": 98.3,
    "blue": 196.60,
    "purple": 294.9
}

def get_cube_positions():
    return cube_positions

#Move to a specific cube position: works with color name
def move_to_cube_position(color_name):
    position = cube_positions[color_name] 
    slidemotor.set_position_relative(position)
    time.sleep(2)

def move_to_base(current_color):
    position = cube_positions[current_color]
    slidemotor.set_position_relative((-1)*(position))
    time.sleep(2)
    
def push():
    pushmotor.set_position_relative(360)
    time.sleep(2)

#Main function
try:
    while not stopsensor.is_pressed():
        zone_color = get_color.get_mean_zone_color(zone_color_sensor)

        
        if zone_color == "red":
            move_to_cube_position("red")
            push()
            move_to_base("red")
        
        if zone_color == "orange": 
            move_to_cube_position("orange")
            push()
            move_to_base("orange")

        if zone_color == "yellow":  
            move_to_cube_position("yellow")
            push()
            move_to_base("yellow")

        if zone_color == "green":
            move_to_cube_position("green")
            push()
            move_to_base("green")

        if zone_color == "blue":
            move_to_cube_position("blue")
            push()
            move_to_base("blue")

        if zone_color == "purple":
            move_to_cube_position("purple")
            push()
            move_to_base("purple")   

    ES.emergency_stop()
except BaseException as error:
    print(error)
    exit()

