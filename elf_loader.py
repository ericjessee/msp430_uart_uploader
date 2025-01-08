import os

def extract_segments(filename):
    os.system(f'mkdir -p elf_data')
    os.system(f'~/ti/gcc/bin/msp430-elf-readelf -t {filename} > elf_data/sections.txt')
    segments = [filename] #place filename at first position in list
    with open("elf_data/sections.txt", 'r') as sections:
        top = False
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
                    items = line[7:].split()
                    seg['addr'] = items[1]
                    seg['off']  = items[2]
                    seg['size'] = items[3]
                    sec_pos = 2
                elif sec_pos == 2:
                    seg['tags'] = line[7:].split()[1:]
                    segments.append(seg.copy())
                    sec_pos = 0
    return segments
    
#so far just extract vector table entries and .text program code
def extract_bin_data(segments):
    final_segments = []
    final_seg_data = {}
    noinit_addr = ""
    for segment in segments:
        if isinstance(segment, dict): 
            if segment['name'] == ".noinit":
                noinit_addr = segment['addr']
                break
    for segment in segments:
        #dump the contents of the segment into a binary file
        if isinstance(segment, dict): #ensures the filename is skipped
            if (segment['addr'] != noinit_addr) and (("vector" in segment['name']) or (segment['name'] == ".text")):
                final_seg_data = segment.copy()
                final_seg_data['filename'] = f'seg_{segment['name']}.bin'
                final_segments.append(final_seg_data)
                os.system(f'~/ti/gcc/bin/msp430-elf-objcopy --dump-section {segment['name']}=elf_data/{final_seg_data['filename']} {segments[0]}')
    return final_segments

def prep_elf_contents(filename):
    segments = extract_segments(filename)
    return extract_bin_data(segments)

if __name__ == "__main__":
    #filename = sys.argv[1]
    filename="/home/eric/ti/msp/MSP430Ware_3_80_14_01/examples/devices/MSP430F1xx/MSP430F11x2_MSP430F12x_MSP430F12x2_Code_Examples/GCC_Makefile/fet120_ta_01/fet120_ta_01.out"
    seg_dict = prep_elf_contents(filename)
    for seg in seg_dict:
        print(seg)