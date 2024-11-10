Deaf-to-Blind Communication System
A project facilitating communication from deaf individuals to blind individuals using a web interface and tactile feedback via buzzers. The system converts textual input into Braille binary sequences and activates corresponding buzzers to represent Braille characters.

Table of Contents
Overview
Hardware Components
Software Requirements
Wiring Diagram
Installation
Usage
Troubleshooting
Future Enhancements
Credits
Overview
This project enables deaf individuals to communicate with blind individuals by translating text input from a web interface into Braille. The translation is achieved by converting each character into a 6-bit binary Braille representation, which then activates a set of buzzers corresponding to the Braille dots. This tactile feedback allows blind users to perceive the communicated message.

Hardware Components
ESP32 Development Board: Acts as the central controller handling serial communication and buzzer activation.
6 Buzzers: Represent the six dots of a Braille character.
6 Push Buttons: Allow users to input Braille binary sequences manually.
Enter Button: Submits the entered Braille character for processing.
3.5" TFT SPI 480x320 ILI9488 LCD Display: (Optional) Displays messages if additional visual feedback is desired.
Connecting Wires: For making connections between the ESP32, buzzers, and buttons.
Breadboard: Facilitates easy wiring and prototyping.
Software Requirements
Flask: A lightweight web framework for Python to create the web interface.
Python 3.x: To run the Flask application (gui.py).
MicroPython: Firmware flashed onto the ESP32 to run the buzzer control script (main.py).
Serial Communication Library: Such as pySerial for handling serial communication between the Flask app and ESP32.
Web Browser: To access the web interface for inputting sentences.
Wiring Diagram
ESP32 to Buzzers
ESP32 GPIO	Buzzer Number	Function
GPIO3	Buzzer 1	Braille Dot 1
GPIO4	Buzzer 2	Braille Dot 2
GPIO5	Buzzer 3	Braille Dot 3
GPIO6	Buzzer 4	Braille Dot 4
GPIO7	Buzzer 5	Braille Dot 5
GPIO8	Buzzer 6	Braille Dot 6
ESP32 to Buttons
ESP32 GPIO	Button Number	Function
GPIO12	Button 1	Braille Dot 1
GPIO19	Button 2	Braille Dot 2
GPIO13	Button 3	Braille Dot 3
GPIO18	Button 4	Braille Dot 4
GPIO14	Button 5	Braille Dot 5
GPIO17	Button 6	Braille Dot 6
GPIO15	Enter Button	Submit Character
ESP32 to LCD Display (Optional)
If using the LCD display for additional feedback, ensure the following connections:

ESP32 GPIO	ILI9488 Pin	Function
GPIO18	SCK	SPI Clock
GPIO23	MOSI	SPI Master Out
GPIO5	CS	Chip Select
GPIO17	DC	Data/Command
GPIO16	RST	Reset
GPIO4	BL	Backlight (Optional)
GND	GND	Ground
5V	VCC	Power (Ensure 5V)
Note: Ensure that the ESP32's ground (GND) is connected to all peripherals' grounds to maintain a common reference.

Installation
1. Setup the ESP32 with MicroPython
Flash MicroPython Firmware:

Download the latest MicroPython firmware for ESP32 from the official MicroPython website.
Use a tool like esptool.py to flash the firmware:
bash
Copy code
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-idf4-20210902-v1.17.bin
Install a Serial Communication Tool:

Use Thonny IDE or mpremote to upload scripts to the ESP32.
2. Install Python Dependencies
On your computer, install the required Python packages:

bash
Copy code
pip install flask pyserial
3. Upload Scripts
Upload main.py to ESP32:

Connect the ESP32 to your computer via USB.
Open Thonny IDE, select the correct interpreter (MicroPython (ESP32)), and upload main.py to the ESP32.
Prepare gui.py:

Ensure that gui.py is placed on your computer and is ready to run.
Usage
1. Running the Flask Web Interface
Connect the ESP32 to the Computer:

Ensure the ESP32 is connected via USB and is running main.py.
Identify the Serial Port:

Determine the serial port assigned to the ESP32 (e.g., COM3 on Windows or /dev/ttyUSB0 on Linux/Mac).
Run gui.py:

Open a terminal or command prompt.
Navigate to the directory containing gui.py.
Run the script:
bash
Copy code
python gui.py
The Flask server will start, typically accessible at http://127.0.0.1:5000/.
2. Using the Web Interface
Access the Web Interface:

Open a web browser and navigate to http://127.0.0.1:5000/.
Enter a Sentence:

Input your desired text into the provided text box and click the Translate button.
Transmission:

The entered text is converted into a Braille binary sequence and sent over serial to the ESP32.
3. ESP32 Processing and Buzzer Activation
Receiving Data:

The ESP32 running main.py listens for incoming Braille binary sequences via serial.
Activating Buzzers:

For each 6-bit binary code received, the corresponding buzzers are activated to represent the Braille dots.
Example:
Pressing Buttons 1 and 3 corresponds to the binary 101000, which maps to the character 'b'.
Buzzers 1 and 3 will activate, providing tactile feedback.
Message Completion:

After processing all binary codes, the ESP32 ensures all buzzers are turned off.
Troubleshooting
1. LCD Not Displaying
Verify Connections:

Ensure all SPI and control pins are correctly connected.
Check that the LCD is receiving adequate power (5V).
Check Driver Compatibility:

Confirm that the ili9488.py driver matches your LCD's controller.
Backlight Control:

If using the backlight, ensure it's powered on via GPIO4.
2. Buttons Not Being Detected
Check Wiring:

Ensure each button is connected to the correct GPIO pin with proper pull-down resistors.
Test Buttons:

Use a simple script to print button presses to the serial console.
python
Copy code
from machine import Pin
import time

button_pins = {
    1: Pin(12, Pin.IN, Pin.PULL_DOWN),
    2: Pin(19, Pin.IN, Pin.PULL_DOWN),
    3: Pin(13, Pin.IN, Pin.PULL_DOWN),
    4: Pin(18, Pin.IN, Pin.PULL_DOWN),
    5: Pin(14, Pin.IN, Pin.PULL_DOWN),
    6: Pin(17, Pin.IN, Pin.PULL_DOWN)
}
enter_button = Pin(15, Pin.IN, Pin.PULL_DOWN)

try:
    while True:
        for i in range(1,7):
            if button_pins[i].value():
                print(f"Button {i} pressed")
                while button_pins[i].value():
                    time.sleep(0.01)
        if enter_button.value():
            print("Enter Button pressed")
            while enter_button.value():
                time.sleep(0.01)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
3. Buzzers Not Activating
Check Wiring:

Ensure each buzzer is connected to the correct GPIO pin.
Power Requirements:

Some buzzers may require more current. Consider using transistors or MOSFETs to drive them.
Test Buzzers:

Use a simple script to activate each buzzer individually.
python
Copy code
from machine import Pin
import time

buzzer_pins = {
    1: Pin(3, Pin.OUT),
    2: Pin(4, Pin.OUT),
    3: Pin(5, Pin.OUT),
    4: Pin(6, Pin.OUT),
    5: Pin(7, Pin.OUT),
    6: Pin(8, Pin.OUT)
}

try:
    while True:
        for i in range(1,7):
            buzzer_pins[i].on()
            print(f"Buzzer {i} ON")
            time.sleep(0.5)
            buzzer_pins[i].off()
            print(f"Buzzer {i} OFF")
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
4. Serial Communication Issues
Check Serial Port:

Ensure that the correct serial port is specified in gui.py (e.g., COM8).
Permissions:

On Linux/Mac, ensure you have the necessary permissions to access the serial port.
Serial Driver:

Ensure that the necessary serial drivers are installed on your computer.
5. General Debugging
Use Serial Console:

Use Thonny IDE or another serial monitor to view debug messages from the ESP32.
LED Indicators:

Consider adding LEDs to indicate button presses or buzzer activations for visual confirmation.
Future Enhancements
Bi-directional Communication:

Enable communication from blind to deaf individuals using additional interfaces like speech recognition or tactile input devices.
Persistent Storage:

Implement storage mechanisms to save and retrieve messages.
Multi-line Display:

Enhance the LCD display to handle multi-line messages with scrolling capabilities.
Wireless Communication:

Integrate Wi-Fi or Bluetooth for wireless communication between the web interface and ESP32.
User Authentication:

Add authentication to the web interface for secure communication.
Credits
MicroPython ILI9488 Driver: russhughes/micropython-ili9488
Flask Framework: Flask Documentation
Bootstrap CSS Framework: Bootstrap Documentation
Project Inspiration: Enhancing accessibility and communication between deaf and blind individuals.
For any issues or contributions, please open an issue or submit a pull request on the project's repository.