import time
from tkgpio import TkCircuit
from gpiozero import LED, Button, AngularServo, Buzzer, MCP3008
from enum import Enum
import random

configuration = {
    "width": 600,
    "height": 600,
    "leds": [{"x": 50, "y": 40, "name": "OnLed", "pin": 16}, {"x": 150, "y": 40, "name": "EMLed", "pin": 20}],
    "buttons": [{"x": 50, "y": 150, "name": "Start System", "pin": 18},
                {"x": 150, "y": 150, "name": "Reset System", "pin": 8}],
    "buzzers": [{"x": 50, "y": 250, "name": "Buzzer", "pin": 9, "frequency": 440}],
    "servos": [{"x": 50, "y": 350, "name": "Servomotor", "pin": 23, "min_angle": -90, "max_angle": 90, "initial_angle": 20}],
}
circuit = TkCircuit(configuration)


@circuit.run
def main():
    class System_States(Enum):
        ENTRY_IDLE_STATE = 0
        STAY_IDLE_STATE = 1
        ENTRY_MONITORING_TEMP_STATE = 2
        STAY_MONITORING_TEMP_STATE = 3
        TEMP_HIGH_STATE = 4
        EMERGENCY_STATE = 5

    #Temp_Sensor = MCP3008(channel=0)
    System_On_Led = LED(16)
    Emergency_Led = LED(20)
    ventilation_Motor = AngularServo(23, min_angle=0, max_angle=180)
    Start_SystemPB = Button(18, bounce_time=0.1)
    Rest_SystemPB = Button(8, bounce_time=0.1)
    Alert = Buzzer(9)
    global current_state
    current_state = System_States.ENTRY_IDLE_STATE

    def get_Temp():
        temp_value = random.uniform(20, 50)
        return temp_value

    def Start_System():
        global current_state
        if current_state == System_States.STAY_IDLE_STATE:
            current_state = System_States.ENTRY_MONITORING_TEMP_STATE

    def reset_system():
        global current_state
        if current_state == System_States.EMERGENCY_STATE:
            current_state = System_States.ENTRY_IDLE_STATE

    Start_SystemPB.when_pressed = Start_System
    Rest_SystemPB.when_pressed = reset_system

    while True:
        print(f"Current State : {current_state.name}")

        if current_state == System_States.ENTRY_IDLE_STATE:
            System_On_Led.off()
            Emergency_Led.off()
            Alert.off()
            ventilation_Motor.angle = 0
            current_state = System_States.STAY_IDLE_STATE
            idle_start_time = time.time()  # Start the timer

        elif current_state == System_States.STAY_IDLE_STATE:
            # Check if 10 seconds have passed or Start button is pressed

            if time.time() - idle_start_time >= 10:
                print(f"Current State : {current_state.name}")
                current_state = System_States.ENTRY_MONITORING_TEMP_STATE
            time.sleep(0.1)  # Small delay for CPU relief

        elif current_state == System_States.ENTRY_MONITORING_TEMP_STATE:
            System_On_Led.on()
            Emergency_Led.off()
            Alert.off()
            ventilation_Motor.angle = 0
            current_state = System_States.STAY_MONITORING_TEMP_STATE

        elif current_state == System_States.STAY_MONITORING_TEMP_STATE:
            temp_value = get_Temp()
            print(f"Temperature: {temp_value}")  # Print temperature
            # if 30 < Temp_Sensor.read_temp_c() <= 40 :
            if 30 < temp_value <= 40:
                current_state = System_States.TEMP_HIGH_STATE
            #elif Temp_Sensor.read_temp_c() > 40:
            elif temp_value > 40:
                current_state = System_States.EMERGENCY_STATE

        elif current_state == System_States.TEMP_HIGH_STATE:
            System_On_Led.on()
            Emergency_Led.off()
            Alert.off()
            ventilation_Motor.angle = 90
            temp_value = get_Temp()
            print(f"Temperature: {temp_value}")  # Print temperature
            time.sleep(3)
            #if Temp_Sensor.read_temp_c() < 30 :
            if temp_value < 30:
                current_state = System_States.ENTRY_MONITORING_TEMP_STATE

        elif current_state == System_States.EMERGENCY_STATE:
            System_On_Led.on()
            Emergency_Led.on()
            ventilation_Motor.angle = 180
            Alert.on()
            temp_value = get_Temp()
            print(f"Temperature: {temp_value}")  # Print temperature

        time.sleep(0.1)  # Small delay for CPU relief
