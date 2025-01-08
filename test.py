from commands import *
import sys

filename=sys.argv[1]
# Configure the serial port
port_name = "/dev/ttyUSB0"  # Replace with your port name, e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux
baud_rate = 9600    # Adjust as needed
ser = init_ser(port_name, baud_rate)
get_bsl_ver(ser)
clear_flash(ser)
unlock_memory(ser)
#bin_data = read_bin('/home/eric/ti/msp/MSP430Ware_3_80_14_01/examples/devices/MSP430F1xx/MSP430F11x2_MSP430F12x_MSP430F12x2_Code_Examples/GCC_Makefile/fet120_adc10_11/fet120_adc10_11.bin')
#dump_msg_contents(bin_data)
bin_data = read_bin(filename)
#test_data = gen_test_data(44)
data = bin_data
addr_bytes = bytes.fromhex("f000")
write_data(ser, addr_bytes, data)
#read_data(ser, addr_bytes, len(data))

#temp hack - these should be read from the elf file
#write isr vector 6
addr_bytes = bytes.fromhex("ffea")
data = bytearray([0x6e, 0xf0])
write_data(ser, addr_bytes, data)
read_data(ser, addr_bytes, 2)

#write isr vector 10
addr_bytes = bytes.fromhex("fff2")
data = bytearray([0x74, 0xf0])
write_data(ser, addr_bytes, data)
read_data(ser, addr_bytes, 2)

#set reset vector
addr_bytes = bytes.fromhex("fffe")
data = bytearray([0x00, 0xf0])
write_data(ser, addr_bytes, data)
read_data(ser, addr_bytes, 2)

#reset device to begin code execution
reset_msp(ser)
print("done. exiting...")