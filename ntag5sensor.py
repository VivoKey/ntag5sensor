#!/usr/bin/env python3

import time, sys

from reader.acr1552 import ACR1552
from vicinity.ntag5link import NTAG5Link, NXP_CONFIG_1_USE_CASE_CONF_I2C_MASTER, NXP_EH_CONFIG_EH_VOUT_I_SEL_4_0, NXP_EH_CONFIG_EH_VOUT_V_SEL_3_0, NXP_EH_CONFIG_EH_VOUT_V_SEL_2_4, NXP_EH_CONFIG_EH_VOUT_I_SEL_1_4, NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8, NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4, NXP_EH_CONFIG_EH_VOUT_I_SEL_0_6
from vicinity.tmp117 import TMP117

from cli import argparser, display


if __name__ == "__main__":
    args = argparser.parse()
   
    # Connect to chip on specified reader
    acr = ACR1552.cli_create_connect(args)
    chip = NTAG5Link(acr)

    # Setup chip for energy harvesting and I2C transfer
    # These write command work despite the reader claiming they timed out (TODO: investigate)
    print("info: Writing persistent configuration")
    try:
        chip.write_config1(sram_enable = True, use_case = NXP_CONFIG_1_USE_CASE_CONF_I2C_MASTER)
    except Exception as e:
        print(f"warning: Possibly failed to write CONFIG_1, ignoring error: {e}")
    try:
        chip.write_eh_config(current = NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4, voltage = NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8)
    except Exception as e:
        print(f"warning: Possibly failed to write EH_CONFIG, ignoring error: {e}")
    print("If the configuration has changed, power-cycle the chip once now")
    print("")

    # Display system information
    print("info: System information:")
    info = chip.get_system_info()
    display.print_system_info(info)
    print("")
    print("info: Extended system information:")
    ext_info = chip.get_extended_system_info()
    display.print_extended_system_info(ext_info)
    print("")
    print("info: NXP information:")
    nxp_info = chip.get_nxp_info()
    display.print_nxp_system_info(nxp_info)
    print("")

    # Display config information
    print("info: Persistent configuration:")
    config_info = chip.get_config_info()
    display.print_config_info(config_info)
    print("")

    # Start energy harvesting
    print("info: Triggering energy harvesting")
    chip.eh_control(trigger = True, enable = False)
    while(not chip.check_eh_load_ok()):
        print("info: Waiting for energy harvesting load stabilization")
        time.sleep(0.1)
    print("info: Energy harvesting load is stable, enabling")
    chip.eh_control(trigger = True, enable = True)
    print("info: Energy harvesting active")
    print("")

    # Read attached temperature sensor
    print("info: Reading sensor")
    temp_sensor = TMP117(chip)
    while(True):
        try:
            reading = temp_sensor.read_temperature()
            if(reading != None):
                print(f"info: Temperature is {reading} °C")
        except KeyboardInterrupt:
            break

    # Disconnect tag 
    acr.disconnect()
