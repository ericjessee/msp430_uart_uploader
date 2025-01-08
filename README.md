There weren't many resources out there about getting this to work without official TI hardware.
The BSL documentation is quite good, and provides good detail on the harware configuration, but I couldn't find anywhere the correct software to use with this setup, so I decided to write my own.

Currently this does the bare minimum of loading elf contents to the device's flash memory. I've never tried to write any kind of elf loader before, so i'm sure I did many things wrong. Use at your own risk.

Hardware considerations:
Serial signals must be level shifted to 3.3V (down from the USB default of 5V). The FTDI board I had on hand supported this directly with a jumper setting. If not, a seperate level shifting scheme must be used.
In order to get the DTR and RTS to remain in the correct default state during serial communication, the RTS signal has to be inverted (I used a 5V CMOS logic inverter followed by a voltage divider to shift the level back down to 3.3V).
Pin connections are as follows (assuming an MSP430F1122):

(FTDI -> MCU)

 DTR  -> !RST/NMI

 RTS  -> (not gate) -> TEST

 TX   -> P2.2

 Rx   <- P1.1


The FTDI chip seems to invert the signals by default, so your mileage may vary (may just need to swap the "True" and "False" in the invocation sequence)