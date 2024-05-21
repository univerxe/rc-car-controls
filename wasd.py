import serial
import keyboard

# Function to establish connection with the Arduino
def connect_to_arduino(port, baud_rate=9600):
    try:
        return serial.Serial(port, baud_rate)
    except serial.SerialException as e:
        print(f"Failed to connect on {port}: {e}")
        exit(1)

# Function to send command to Arduino
def send_command(ser, command):
    try:
        ser.write(command.encode())
        print(f"Sent '{command}' to Arduino")  # Print the command sent to Arduino
    except serial.SerialException as e:
        print(f"Error sending data: {e}")
        exit(1)

# Main function to set up controls
def main():
    port = 'COM10'  # COM port used by Arduino
    ser = connect_to_arduino(port)
    
    # Print instructions
    print("Control the car using 'W', 'S', 'A', 'D' keys. Press ESC to stop and exit.")
    
    # Binding keys to specific actions
    keyboard.add_hotkey('w', send_command, args=(ser, 'W'))
    keyboard.add_hotkey('s', send_command, args=(ser, 'S'))
    keyboard.add_hotkey('a', send_command, args=(ser, 'A'))
    keyboard.add_hotkey('d', send_command, args=(ser, 'D'))
    keyboard.add_hotkey('o', send_command, args=(ser, 'O'))
    
    keyboard.on_press_key('esc', lambda _: send_command(ser, 'X'))  # Stop and exit

    # Wait for the 'esc' key to exit
    keyboard.wait('esc')

    # Cleanup on exit
    ser.close()

if __name__ == "__main__":
    main()
