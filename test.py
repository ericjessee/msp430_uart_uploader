import serial
import time
from queries import *


# Configure the serial port
port_name = "/dev/ttyUSB0"  # Replace with your port name, e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux
baud_rate = 9600    # Adjust as needed

def pulse():
    time.sleep(0.001)
    return

def wait_ack():
    byte = ser.read(1)
    if (byte == b'\x90'):
        print(" >> got ACK from msp430")
        return
    elif (byte == b'\xa0'):
        print(" >> got NACK from msp430! (fail)")
        exit()
    else:
        print(" >> no response from msp430!")
        exit()

def sync():
    print(" >> sending sync char")
    ser.write(b'\x80')
    ser.flush()
    wait_ack()
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
    ser.rts = False
    ser.dtr = True
    time.sleep(0.1)

    #BSL invocation sequence
    ser.rts = True
    ser.rts = False
    pulse()
    ser.rts = True
    ser.dtr= False
    ser.rts = False

    #rts and dtr not needed for actual operation
    ser.rtscts=False
    ser.dsrdtr=False

    time.sleep(0.01)
    sync()
    
    #print(ver_query_msg)
    ser.write(ver_query_msg)
    resp = ser.read(22)
    # handy for inspecting frame contents:
    # for idx, bt in enumerate(resp):
    #     print(f'{idx}: {hex(bt)}')
    # print(bytearray(resp))
    family = int.from_bytes(resp[4:6], byteorder='big')
    bsl_ver = int.from_bytes(resp[14:16], byteorder='big')
    print(f'got device family: {family}, BSL ver: {bsl_ver}')

    sync()
    print("clearing flash contents")
    ser.write(mass_erase_cmd)
    wait_ack()
    print("flash erase success")

    sync()
    print(f'attempting to unlock memory')
    #generate the default password:
    password = bytearray()
    for i in range(32):
        password.append(0xff)
    cmd = password_unlock_cmd(password)
    ser.write(cmd)
    wait_ack()
    print("memory unlock success")

    
    
    sync()
    print("downloading program to memory")
    bin_data = bytearray()
    with open("fet120_1.bin", 'rb') as file:
        byte = file.read(1)
        while byte != b'':
            bin_data.append(byte[0])
            byte=file.read(1)
    for idx, bt in enumerate(bin_data):
        print(f'{idx}: {hex(bt)}')

    test_data = bytearray()
    toggle = True
    for i in range(16):
        if toggle:
            test_data.append(0xab)
            toggle = not toggle
        else:
            test_data.append(0xcd)
            toggle = not toggle
    print(test_data)

    #data = test_data
    data = bin_data

    addr_str = "f000"
    cmd = write_mem_cmd(bytes.fromhex(addr_str), data)
    ser.write(cmd)
    wait_ack()

    sync()
    print(f'reading from memory')
    # addr_str = "1000"
    # len_str = "0020"
    len = len(data)
    cmd = read_mem_query(bytes.fromhex(addr_str), len)
    ser.write(cmd)
    resp = ser.read(len+6)
    if resp == b'\xa0':
        print("msp430 refused request!")
    blocklen = resp[2]
    for idx, bt in enumerate(resp[4:4+blocklen]):
        print(f'{hex(int(addr_str, 16) + idx)}: {hex(bt)}')

    sync()
    print(f'updating PC for program start')
    # addr_str = "f000"
    cmd = load_pc_cmd(bytes.fromhex(addr_str))
    ser.write(cmd)
    wait_ack
    

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port
    if 'ser' in locals() and ser.is_open:
        ser.close()

