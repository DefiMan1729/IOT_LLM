import serial

# Replace 'COM3' with your Raspberry Pi serial port (e.g., '/dev/ttyUSB0' or '/dev/ttyS0')
SERIAL_PORT = '/dev/ttyUSB0'  
BAUD_RATE = 9600  # Match the baud rate of the device sending data

def serial_conn_read(serial_port, baud_rate):
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Connected to {serial_port} at {baud_rate} baud.")
        
        data = None  # Initialize data variable
        while True:
            # Read a line of data from the serial port
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                print(f"Received: {data}")
                break  # Exit the loop after one read for simplicity

        return data  # Return data after reading

    except serial.SerialException as e:
        print(f"Serial Error: {e}")
        return None

    except KeyboardInterrupt:
        print("\nExiting program...")

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")
