from queries import *
import time
import serial

def pulse():
    time.sleep(0.001)
    return

def wait_ack(ser):
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

def sync(ser):
    print(" >> sending sync char")
    ser.write(b'\x80')
    ser.flush()
    wait_ack(ser)
    return

def init_ser(port_name, baud_rate):
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
    return ser

def dump_msg_contents(msg):
    for idx, bt in enumerate(msg):
        print(f'{idx}: {hex(bt)}')
    return

def read_bin(filename):
    bin_data = bytearray()
    with open(filename, 'rb') as file:
        byte = file.read(1)
        while byte != b'':
            bin_data.append(byte[0])
            byte=file.read(1)
        return bin_data

def get_bsl_ver(ser):
    sync(ser)
    ser.write(ver_query_msg)
    resp = ser.read(22)
    family = int.from_bytes(resp[4:6], byteorder='big')
    bsl_ver = int.from_bytes(resp[14:16], byteorder='big')
    print(f'got device family: {family}, BSL ver: {bsl_ver}')
    return

def unlock_memory(ser):
    sync(ser)
    print(f'attempting to unlock memory')
    #generate the default password - will be correct if mass erase first:
    password = bytearray()
    for i in range(32):
        password.append(0xff)
    cmd = password_unlock_cmd(password)
    ser.write(cmd)
    wait_ack(ser)
    print("memory unlock success")
    return

def clear_flash(ser):
    sync(ser)
    print("clearing flash contents")
    ser.write(mass_erase_cmd)
    wait_ack(ser)
    print("flash erase success")
    return

def write_data(ser, address, data):
    sync(ser)
    print(f'loading {len(data)} bytes to address 0x{address.hex()}')
    cmd = write_mem_cmd(address, data)
    ser.write(cmd)
    wait_ack(ser)
    return

def read_data(ser, address, length):
    sync()
    print(f'reading from memory')
    cmd = read_mem_query(address, length)
    ser.write(cmd)
    resp = ser.read(len+6)
    if resp == b'\xa0':
        print("msp430 refused request!")
    blocklen = resp[2]
    for idx, bt in enumerate(resp[4:4+blocklen]):
        print(f'{hex(address + idx)}: {hex(bt)}')
    return

def write_pc(ser, address):
    #code will begin executing from this address
    sync(ser)
    print(f'updating PC for program start')
    cmd = load_pc_cmd(address)
    ser.write(cmd)
    wait_ack(ser)