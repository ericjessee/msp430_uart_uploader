import os
import sys

def extract_segments(filename):
    os.system(f'~/ti/gcc/bin/msp430-elf-readelf -t {filename} > sections.txt')
    with open("sections.txt", 'r') as sections:
        top = False
        segments = []
        sec_pos = 0
        seg={}
        for line in sections:
            if "[ 1]" in line:
                top=True
            if top:
                if sec_pos == 0: #name
                    seg['name'] = line[7:].split()[0]
                    sec_pos = 1
                elif sec_pos == 1:
                    seg['addr'] = line[7:].split()[1]
                    sec_pos = 2
                elif sec_pos == 2:
                    seg['tags'] = line[7:].split()[1:]
                    segments.append(seg.copy())
                    sec_pos = 0
        return segments
    
def extract_bin_data(segments):
    for segment in segments:
        print(segment)

if __name__ == "__main__":
    #filename = sys.argv[1]
    filename="/home/eric/ti/msp/MSP430Ware_3_80_14_01/examples/devices/MSP430F1xx/MSP430F11x2_MSP430F12x_MSP430F12x2_Code_Examples/GCC_Makefile/fet120_ta_01/fet120_ta_01.out"
    segments = extract_segments(filename)
    extract_bin_data(segments)