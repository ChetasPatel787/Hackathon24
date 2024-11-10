from machine import Pin
import sys
import time

# Define GPIO pins for the 6 buzzers (representing Braille dots)
buzzer_pins = {
    1: Pin(3, Pin.OUT),    # Buzzer 1
    2: Pin(4, Pin.OUT),    # Buzzer 2
    3: Pin(5, Pin.OUT),    # Buzzer 3
    4: Pin(8, Pin.OUT),    # Buzzer 4
    5: Pin(27, Pin.OUT),    # Buzzer 5
    6: Pin(26, Pin.OUT)     # Buzzer 6
}

def process_binary_input(binary_input):
    """Processes a binary input and activates the buzzers accordingly."""
    binary_input = binary_input.strip()
    if len(binary_input) != 6 or not all(bit in '01' for bit in binary_input):
        print(f"Warning: '{binary_input}' is not a valid 6-bit binary sequence.")
        return

    for i, bit in enumerate(binary_input):
        buzzer = buzzer_pins[i + 1]  # Access buzzer pin directly
        if bit == '1':
            buzzer.on()  # Turn buzzer on
            print(f"Buzzer {i + 1} ON")
        else:
            buzzer.off()  # Turn buzzer off
            print(f"Buzzer {i + 1} OFF")
    time.sleep(0.5)  # Brief vibration for each input

    # Turn off all buzzers after each input
    for buzzer in buzzer_pins.values():
        buzzer.off()

try:
    while True:
        # Read a sequence of binary strings from serial input
        print("Waiting for input...")
        binary_sequence_input = sys.stdin.readline()
        if not binary_sequence_input:
            continue  # No data received, continue loop
        binary_sequence_input = binary_sequence_input.strip()
        if binary_sequence_input == '!':
            break
        # Split the input on underscores to get individual binary codes
        binary_codes = binary_sequence_input.split('_')
        for binary_code in binary_codes:
            process_binary_input(binary_code)
            time.sleep(1)  # Pause for 1 second between symbols

except KeyboardInterrupt:
    pass
finally:
    # Deactivate all buzzers
    for buzzer in buzzer_pins.values():
        buzzer.off()