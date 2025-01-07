import serial
import time
from queries import ver_query_msg, mass_erase_cmd, read_mem_query, password_unlock_cmd, write_mem_cmd


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
    print("writing to memory")
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
    addr_str = "1000"
    cmd = write_mem_cmd(bytes.fromhex(addr_str), test_data)
    ser.write(cmd)
    wait_ack()

    sync()
    print(f'reading from memory')
    addr_str = "1000"
    len_str = "0020"
    cmd = read_mem_query(bytes.fromhex(addr_str), bytes.fromhex(len_str))
    ser.write(cmd)
    resp = ser.read(int(len_str, 16)+6)
    if resp == b'\xa0':
        print("msp430 refused request!")
    blocklen = resp[2]
    for idx, bt in enumerate(resp[4:4+blocklen]):
        print(f'{hex(int(addr_str, 16) + idx)}: {hex(bt)}')
    

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port
    if 'ser' in locals() and ser.is_open:
        ser.close()

