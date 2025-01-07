import serial
import time
from checksum import append_checksum, reverse_byte_order

sync_char = b'\x80'
ack_char = b'\x90'
ver_query_msg = append_checksum(b'\x80\x1e\x04\x04\xde\xad\xbe\xef')
read_bytes_msg = b''


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
        parity="E",
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
    ser.write(sync_char)
    ser.flush()
    byte = ser.read(1)
    if (byte == ack_char):
        print("got ACK from msp430")
    else:
        print("no response from msp430!")
        exit()
    
    #print(ver_query_msg)
    ser.write(ver_query_msg)
    resp = ser.read(16)
    print(resp)


except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port
    if 'ser' in locals() and ser.is_open:
        ser.close()

