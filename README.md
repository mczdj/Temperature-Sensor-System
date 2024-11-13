# TkCircuit-Based Temperature Monitoring and Emergency System

This project simulates a temperature monitoring and emergency system using the TkCircuit library for a virtual GPIO interface. It includes features such as temperature monitoring, system state management, and emergency alerts.

---

## Features
- **Virtual Components**: Simulates LEDs, Buttons, Buzzer, Servo Motor, and Temperature Sensor.
- **State Machine**: Manages system states for idle, monitoring, and emergency modes.
- **Temperature Simulation**: Random temperature generation for testing various states.
- **Emergency Handling**: Activates an alert and ventilation motor in critical temperature conditions.

---

## Components Used
The system uses the following simulated components via `TkCircuit`:
1. **LEDs**:
   - System On LED (Pin 16)
   - Emergency LED (Pin 20)
2. **Buttons**:
   - Start System Button (Pin 18)
   - Reset System Button (Pin 8)
3. **Buzzer**:
   - Alert Buzzer (Pin 9)
4. **Servo Motor**:
   - Ventilation Motor (Pin 23)
5. **Temperature Sensor**:
   - Simulated using random values.

---

## Circuit Configuration
The GUI layout is specified using the following `TkCircuit` configuration:
```python
configuration = {
    "width": 600,
    "height": 600,
    "leds": [{"x": 50, "y": 40, "name": "OnLed", "pin": 16}, {"x": 150, "y": 40, "name": "EMLed", "pin": 20}],
    "buttons": [{"x": 50, "y": 150, "name": "Start System", "pin": 18},
                {"x": 150, "y": 150, "name": "Reset System", "pin": 8}],
    "buzzers": [{"
