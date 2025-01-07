from commands import *

# Configure the serial port
port_name = "/dev/ttyUSB0"  # Replace with your port name, e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux
baud_rate = 9600    # Adjust as needed
ser = init_ser(port_name, baud_rate)
get_bsl_ver(ser)
clear_flash(ser)
unlock_memory(ser)
bin_data = read_bin('fet120_1.bin')
test_data = gen_test_data(44)
data = bin_data
addr_str = "f000"
addr_bytes = bytes.fromhex(addr_str)
write_data(ser, addr_bytes, data)
#read_data(ser, addr_bytes, len(data))
write_pc(ser, addr_bytes)
print("done. exiting...")