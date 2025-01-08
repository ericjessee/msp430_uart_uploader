import os

def extract_segments(filename):
    os.system(f'~/ti/gcc/bin/msp430-elf-readelf -S {filename} > sections.txt')
    with open("sections.txt", 'r') as sections:
        top = False
        bottom = False
        segments = []
        for line in sections:
            if "Section Headers" in line:
                top=True
            if top:
                if "Key to Flags" in line:
                    bottom = True
                elif not bottom:
                    items = line[7:].split() #split line
                    try: 
                        if not (items[6].isnumeric()) and (items[6] != "Flg"):
                            segments.append(items)
                    except IndexError:
                        pass
        return segments
    
def extract_bin_data(segments):
    no_init_addr = 0
    for segment in segments:
        print(segment)
        if segment[0] == ".noinit":
            no_init_addr = int(segment[2], 16) + int(segment[3], 16)
            print(f'skipping non-initialized segments at address {hex(no_init_addr)}')
            break
    for segment in segments:
        addr = int(segment[2], 16) + int(segment[3], 16)
        if addr != no_init_addr:
            os.system(f'')

if __name__ == "__main__":
    segments = extract_segments("fet120_1.out")
    extract_bin_data(segments)