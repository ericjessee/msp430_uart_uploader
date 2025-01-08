#!/bin/bash
pushd /home/eric/ti/msp/MSP430Ware_3_80_14_01/examples/devices/MSP430F1xx/MSP430F11x2_MSP430F12x_MSP430F12x2_Code_Examples/GCC_Makefile
./build.sh $1
popd
"/home/eric/Projects/msp430 experiments/pyserialtest/bin/python" "/home/eric/Projects/msp430 experiments/pyserialtest/test.py" /home/eric/ti/msp/MSP430Ware_3_80_14_01/examples/devices/MSP430F1xx/MSP430F11x2_MSP430F12x_MSP430F12x2_Code_Examples/GCC_Makefile/$1/$1.bin

