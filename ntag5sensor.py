#!/usr/bin/env python3

import time, sys

from reader.acr1552 import ACR1552
from vicinity.ntag5link import *
from vicinity.tmp117 import TMP117

from cli import argparser, display


# Energy selection options from CLI

I_SEL_CLI = {
    "0.4": NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4,
    "0.6": NXP_EH_CONFIG_EH_VOUT_I_SEL_0_6,
    "1.4": NXP_EH_CONFIG_EH_VOUT_I_SEL_1_4,
    "2.7": NXP_EH_CONFIG_EH_VOUT_I_SEL_2_7,
    "4.0": NXP_EH_CONFIG_EH_VOUT_I_SEL_4_0,
    "6.5": NXP_EH_CONFIG_EH_VOUT_I_SEL_6_5,
    "9.0": NXP_EH_CONFIG_EH_VOUT_I_SEL_9_0,
    "12.5": NXP_EH_CONFIG_EH_VOUT_I_SEL_12_5
}

V_SEL_CLI = {
    "1.8": NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8,
    "2.4": NXP_EH_CONFIG_EH_VOUT_V_SEL_2_4,
    "3.0": NXP_EH_CONFIG_EH_VOUT_V_SEL_3_0
}


if __name__ == "__main__":
    parser, args = argparser.parse()
    argparser.validate(parser, args)

    # List connected readers if selected
    if(args.listreaders):
        readers = ACR1552.list_readers()
        print("info: Connected ACR1552 readers:")
        for i, reader in enumerate(readers):
            print(f"{i}: {reader}")
        exit(1)
   
    # Connect to chip on specified reader
    acr = ACR1552.cli_create_connect(args)
    chip = NTAG5Link(acr)

    # Perform selected action
    if(args.action == "info"):
        # Display system information
        print("info: System information:")
        info = chip.get_system_info()
        display.print_system_info(info)
        print("info: Extended system information:")
        ext_info = chip.get_extended_system_info()
        display.print_extended_system_info(ext_info)
        print("info: NXP information:")
        nxp_info = chip.get_nxp_info()
        display.print_nxp_system_info(nxp_info)

        # Display system config information
        print("info: Persistent system configuration:")
        config_info = chip.get_config_info()
        display.print_config_info(config_info)
        print("info: Persistent energy configuration:")
        energy_info = chip.get_eh_ed_config_info()
        display.print_eh_ed_config_info(energy_info)

    elif(args.action == "setup"):
        # Setup chip for energy harvesting and I2C transfer
        # These write command work despite the reader claiming they timed out (TODO: investigate)
        print("info: Writing persistent configuration")
        try:
            print("info: Writing baseline: SRAM enable, I2C master mode")
            chip.write_config1(sram_enable = True, use_case = NXP_CONFIG_1_USE_CASE_CONF_I2C_MASTER)
        except Exception as e:
            print(f"warning: Possibly failed to write CONFIG_1, ignoring error: {e}")
        try:
            print(f"info: Writing output voltage: {args.voltage} V, energy harvesting trigger current: {args.current} mA")
            chip.write_eh_ed_config(current = I_SEL_CLI.get(args.current, NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4), 
                voltage = V_SEL_CLI.get(args.voltage, NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8))
        except Exception as e:
            print(f"warning: Possibly failed to write EH_CONFIG, ignoring error: {e}")
        print("If the configuration has changed, power-cycle the chip once now")

    elif(args.action == "tmp117"):
        # Start energy harvesting
        print("info: Triggering energy harvesting")
        chip.eh_control(trigger = True, enable = False)
        while(not chip.check_eh_load_ok()):
            print("info: Waiting for energy harvesting load stabilization")
            time.sleep(0.1)
        print("info: Energy harvesting load is stable, enabling")
        chip.eh_control(trigger = True, enable = True)
        print("info: Energy harvesting active")

        if(args.verb == "info"):
            pass
        elif(args.verb == "setup"):
            pass
        elif(args.verb == "read"):
            # Read attached temperature sensor
            print("info: Reading sensor")
            temp_sensor = TMP117(chip, args.address)
            while(True):
                try:
                    reading = temp_sensor.read_temperature()
                    if(reading != None):
                        print(f"info: Temperature is {reading} °C")
                except KeyboardInterrupt:
                    break

    # Disconnect tag 
    acr.disconnect()
