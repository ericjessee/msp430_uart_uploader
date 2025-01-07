import serial
import time

# Configure the serial port
port_name = "/dev/ttyUSB0"  # Replace with your port name, e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux
baud_rate = 9600    # Adjust as needed

def pulse():
    time.sleep(0.001)
    return

try:
    # Open the serial port with hardware flow control (RTS/CTS enabled)
    ser = serial.Serial(
        port=port_name,
        baudrate=baud_rate,
        timeout=1,
        rtscts=True,  # Enables RTS/CTS flow control
        dsrdtr=True   # Ensures DTR is used
    )
#
#    # Set RTS and DTR to high initially
    ser.rts = False
    ser.dtr = True
    time.sleep(0.1)
#    pulse()
#  #  print("RTS and DTR set to high.")
#
#    # Toggle RTS off and on twice quickly
    ser.rts = True
    ser.rts = False
    pulse()
    ser.rts = True
    ser.dtr= False
    ser.rts = False

    ser.rtscts=False
    ser.dsrdtr=False
    time.sleep(0.01)
    ser.write(b'\x80')
    ser.flush()
    byte = ser.read(1)
    print(byte)

#    pulse()

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")

