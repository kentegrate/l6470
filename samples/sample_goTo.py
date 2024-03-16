#!/usr/bin/env python3
# coding: utf-8

from l6470 import l6470

import time
import sys
import traceback


def dec_to_hex_22bit(value):
    # Check if the value is within the range of 22-bit signed integers
    if not (-2**21 <= value < 2**21):
        raise ValueError("Value out of range for 22-bit signed integer")

    # Convert negative values to their 2's complement representation
    if value < 0:
        value += 2**22
    
    # Format the value as a hexadecimal string with 6 characters (22 bits is represented by 6 hex digits)
    hex_value = f'{value:06x}'

    return hex_value


def abs_cmd(value):
    hex = dec_to_hex_22bit(value)
    cmd = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]
    return cmd

if __name__ == '__main__':

    device = None

    try:
        # open spi device bus:0, client0
        device = l6470.Device(0, 0)

        # reset L6470 
        device.resetDevice()

        # parameter value setting
        device.setParam(l6470.MAX_SPEED, [0x00, 0x10])        
        device.setParam(l6470.STEP_MODE, [0x02])
        device.setParam(l6470.KVAL_HOLD, [0x00])
        device.setParam(l6470.KVAL_RUN,  [0xF0])
        device.setParam(l6470.KVAL_ACC,  [0x00])
        device.setParam(l6470.KVAL_DEC,  [0x00])

        # exec "goTo" command
        device.goTo([0x00, 0x00, 0x00])
        device.wait_until_not_busy()

        for i in range(1):

            time.sleep(1)

            # get device status
            status = device.updateStatus()
            print(status)

        # exec "goTo" command
#        device.goTo([0x00, 0x64, 0x00])
#        device.goTo([0x00, 0xc7, 0x38])
#        device.goTo(abs_cmd(25443*10))
        device.goToDec(25500)

        device.wait_until_not_busy()

        # for i in range(1):

        #     time.sleep(1)

        #     # get device status
        #     status = device.updateStatus()
        #     print(status)

        # # exec "goTo" command
        # device.goTo([0x00, 0x00, 0x00])
        # device.wait_until_not_busy()

        # for i in range(1):

        #     time.sleep(1)

        #     # get device status
        #     status = device.updateStatus()
        #     print(status)

    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))
    except KeyboardInterrupt:
        pass
    finally:
        if device is not None:
            # exec "soft_stop" command
            device.softStop()