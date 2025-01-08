from commands import *
from elf_loader import *
import sys

filename=sys.argv[1]
# Configure the serial port
port_name = "/dev/ttyUSB0"  # Replace with your port name, e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux
baud_rate = 9600    # Adjust as needed
ser = init_ser(port_name, baud_rate)
get_bsl_ver(ser)
clear_flash(ser)
unlock_memory(ser)

segments = prep_elf_contents(filename)
for seg in segments:
    addr = bytes.fromhex(seg['addr'][-4:])
    data = read_bin(f'elf_data/{seg['filename']}')
    write_data(ser, addr, data)

#reset device to begin code execution
reset_msp(ser)
print("done. exiting...")