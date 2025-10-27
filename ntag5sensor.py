#!/usr/bin/env python3

import time, sys
from collections import deque

#from PyQt5 import QtWidgets
#import pyqtgraph as pg

from reader.acr1552 import ACR1552
from vicinity.ntag5link import *
from vicinity.tmp117 import *
from vicinity.tmp112 import *
from vicinity.si1143 import *

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


def start_eh(chip):
    # Start energy harvesting
    print("info: Triggering energy harvesting")
    chip.eh_control(trigger = True, enable = False)
    while(not chip.check_eh_load_ok()):
        print("info: Waiting for energy harvesting load stabilization")
        time.sleep(0.1)
    print("info: Energy harvesting load is stable, enabling")
    chip.eh_control(trigger = True, enable = True)
    print("info: Energy harvesting active")

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
    acr.trace = args.trace
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
        print("info: Writing CONFIG_0 defaults, except low field strength energy harvesting mode")
        chip.write_config0(eh_mode = NXP_CONFIG_0_EH_MODE_LOW_FIELD_STRENGTH)
        print("info: Writing CONFIG_1 defaults, except SRAM enable, I2C master mode")
        chip.write_config1(sram_enable = True, use_case = NXP_CONFIG_1_USE_CASE_CONF_I2C_MASTER)
        print("info: Writing CONFIG_2 defaults, except GPIO 0 and GPIO 1 disable")
        chip.write_config2(gpio0_in = NXP_CONFIG_2_GPIO0_PAD_IN_DISABLED, gpio1_in = NXP_CONFIG_2_GPIO1_PAD_IN_DISABLED)
        print(f"info: Writing output voltage: {args.voltage} V, energy harvesting trigger current: {args.current} mA")
        chip.write_eh_ed_config(current = I_SEL_CLI.get(args.current, NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4), 
            voltage = V_SEL_CLI.get(args.voltage, NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8))
        print("warning: If the configuration has changed, power-cycle the chip once now")

    elif(args.action == "tmp117"):
        # Start energy harvesting
        start_eh(chip)

        # Connect to attached TMP117 sensor
        print("info: Connecting to TMP117 sensor")
        tmp117 = TMP117(chip, args.address)

        if(args.verb == "info"):
            # Display TMP117 config
            print("info: Persistent TMP117 configuration:")
            tmp117_config_info = tmp117.get_config_info()
            display.print_tmp117_config_info(tmp117_config_info)

        elif(args.verb == "setup"):
            # Write supplied config options to TMP117 config EEPROM
            print("info: Writing persistent TMP117 configuration")
            print(f"info: Writing boot mode: {args.mode}, average: {args.average} samples, cycle mode: {args.cycle}")
            mode = TMP117_CONFIG_FLAG_MOD_SHUTDOWN
            if(args.mode == "continuous"):
                mode = TMP117_CONFIG_FLAG_MOD_CONT
            avg = TMP117_CONFIG_FLAG_AVG_8
            if(args.average == 1):
                avg = TMP117_CONFIG_FLAG_AVG_NONE
            elif(args.average == 32):
                avg = TMP117_CONFIG_FLAG_AVG_32
            elif(args.average == 64):
                avg = TMP117_CONFIG_FLAG_AVG_64
            tmp117.write_config(conversion_mode = mode, conversion_cycle = args.cycle, 
                conversion_averaging = avg, eeprom_persistent = True)
            print("info: Successfully wrote persistent configuration")

        elif(args.verb == "read"):
            # Sample temperature data from the sensor
            if(args.mode == "oneshot"):
                # In oneshot mode, manually trigger conversions
                while(True):
                    try:
                        print("info: Triggering oneshot measurement")
                        tmp117.write_config(conversion_mode = TMP117_CONFIG_FLAG_MOD_ONESHOT)
                        # Poll for data available
                        while(True):
                            reading = tmp117.read_temperature()
                            if(reading != None):
                                print(f"info: Temperature is {reading:.3f} °C, {display.celsius_to_fahrenheit(reading):.3f} °F")
                                break
                        print("info: Waiting for 2 seconds")
                        time.sleep(2)
                    except KeyboardInterrupt:
                        break
            elif(args.mode == "continuous"):
                print("info: Running in continuous measurement mode")
                tmp117.write_config(conversion_mode = TMP117_CONFIG_FLAG_MOD_CONT)
                # In continuous mode, just poll for data available
                while(True):
                    try:
                        reading = tmp117.read_temperature()
                        if(reading != None):
                            print(f"info: Temperature is {reading:.3f} °C, {display.celsius_to_fahrenheit(reading):.3f} °F")
                    except KeyboardInterrupt:
                        break

    elif(args.action == "tmp112"):
        # Start energy harvesting
        start_eh(chip)

        # Connect to attached TMP112 sensor
        print("info: Connecting to TMP112 sensor")
        tmp112 = TMP112(chip, args.address)

        if(args.verb == "info"):
            # Display TMP112 config
            print("info: TMP112 configuration:")
            tmp112_config_info = tmp112.get_config_info()
            display.print_tmp112_config_info(tmp112_config_info)

        elif(args.verb == "read"):
            # Sample temperature data from the sensor
            if(args.mode == "oneshot"):
                # In oneshot mode, manually trigger conversions
                tmp112.write_config(shutdown_mode = True, oneshot = False)
                while(True):
                    try:
                        print("info: Triggering oneshot measurement")
                        tmp112.write_config(oneshot = True)
                        # Poll for data available
                        while(True):
                            reading = tmp112.read_temperature()
                            if(reading != None):
                                print(f"info: Temperature is {reading:.3f} °C, {display.celsius_to_fahrenheit(reading):.3f} °F")
                                break
                        print("info: Waiting for 2 seconds")
                        time.sleep(2)
                    except KeyboardInterrupt:
                        break
            elif(args.mode == "continuous"):
                print("info: Running in continuous measurement mode")
                tmp112.write_config(shutdown_mode = False, oneshot = False)
                # In continuous mode, just poll for data available
                while(True):
                    try:
                        reading = tmp112.read_temperature()
                        if(reading != None):
                            print(f"info: Temperature is {reading:.3f} °C, {display.celsius_to_fahrenheit(reading):.3f} °F")
                            time.sleep(0.1)
                    except KeyboardInterrupt:
                        break

    elif(args.action == "si1143"):
        # Start energy harvesting
        start_eh(chip)

        # Connect to attached SI1143 sensor
        print("info: Connecting to SI1143 sensor")
        si1143 = SI1143(chip)

        # Start the sensor
        si1143.initialize()

        if(args.verb == "info"):
            # Display SI1143 info
            print("info: SI1143 information:")
            si1143_info = si1143.get_info()
            display.print_si1143_info(si1143_info)

        elif(args.verb == "read"):
            print("info: Configuring SI1143 sensor for measurements")

            # Configure channel list, enable AUX, ALS IR, ALS visible, PS1 and PS2
            si1143.command(SI1143_CMD_PARAM_SET | SI1143_PARAM_CHLIST, 
                SI1143_CHLIST_EN_AUX | SI1143_CHLIST_EN_ALS_IR | SI1143_CHLIST_EN_ALS_VIS |
                SI1143_CHLIST_EN_PS1 | SI1143_CHLIST_EN_PS2)

            # Configure which LED is driver for each channel
            # LED1 for PS1, LED2 for PS2, and none for PS3
            si1143.command(SI1143_CMD_PARAM_SET | SI1143_PARAM_PSLED12_SELECT,
                SI1143_PSLED12_SELECT_PS1_LED1 | SI1143_PSLED12_SELECT_PS2_LED2)
            si1143.command(SI1143_CMD_PARAM_SET | SI1143_PARAM_PSLED3_SELECT,
                SI1143_PSLED3_SELECT_PS3_NONE)

            # Configure PS ADC parameters
            si1143.command(SI1143_CMD_PARAM_SET | SI1143_PARAM_PS_ADC_MISC,
                SI1143_PS_ADC_MISC_NORMAL_SIGNAL_RANGE | SI1143_PS_ADC_MISC_NORMAL_PROX_MEAS_MODE)
            si1143.command(SI1143_CMD_PARAM_SET | SI1143_PARAM_PS_ADC_GAIN,
                SI1143_PS_ADC_GAIN_DIV_2)

            # Setup interrupts
            si1143.write_register(SI1143_I2C_REG_INT_CFG, [ 0x00 ])
            #    [SI1143_INT_CFG_AUTO_CLEAR | SI1143_INT_CFG_PIN_EN])
            si1143.write_register(SI1143_I2C_REG_IRQ_ENABLE, 
                [SI1143_IRQ_ENABLE_PS1_INT_EN | SI1143_IRQ_ENABLE_PS2_INT_EN])
            si1143.write_register(SI1143_I2C_REG_IRQ_MODE1, [ 0x00 ])
            #    [SI1143_CMD_INT_FLAG])
            #si1143.write_register(SI1143_I2C_REG_IRQ_MODE2, 
            #    [SI1143_CMD_INT_RESP_ERROR])

            # Setup measurement rate
            si1143.write_register(SI1143_I2C_REG_MEAS_RATE, 
                [0x94])
            si1143.write_register(SI1143_I2C_REG_ALS_RATE, 
                [SI1143_MEAS_AFTER_EVERY_WAKEUP])
            si1143.write_register(SI1143_I2C_REG_PS_RATE,
                 [SI1143_MEAS_AFTER_EVERY_WAKEUP])

            # Setup LED current
            # 22.4 mA for both
            si1143.write_register(SI1143_I2C_REG_PS_LED21, 
                [0b00110011])

            # Set auto mode for both PS and ALS
            si1143.command(SI1143_CMD_PSALS_AUTO)

            # Read sensor measurements continuously
            print("info: Reading SI1143 sensor data")

            # # Show a QT window
            # app = QtWidgets.QApplication(sys.argv)
            # win = pg.GraphicsLayoutWidget(show=True, title="Realtime Heartbeat")
            # plot = win.addPlot(labels={'left': 'Value', 'bottom': 'Samples'})
            # plot.addLegend()
            # plot.showGrid(x=True, y=True, alpha=0.3)
            # plot.enableAutoRange('y', True)

            # # Display options
            # show_raw = True
            # show_smooth = False

            # # Two curves for PS1 raw and smoothed
            # curve_ps1_raw = plot.plot(pen=pg.mkPen(color='red', width=1), name="PS1 Raw")
            # curve_ps1_smooth = plot.plot(pen=pg.mkPen(color='blue', width=2), name="PS1 Smooth")

            # BUFFER_SIZE = 200
            # ps1_raw_buf = deque(maxlen=BUFFER_SIZE)
            # ps1_smooth_buf = deque(maxlen=BUFFER_SIZE)
            # ps1_mean_buf = deque(maxlen=5)  # Buffer for 5-sample mean calculation

            # # Use a mutable object to track sample count
            # counters = {'sample_count': 0}

            target_period = 0.02  # 20ms for 50 Hz

            while(True):
                loop_start = time.time()

                try:
                    data = si1143.read_register(SI1143_I2C_REG_PS1_DATA0, 2)
                    ps1_data = int.from_bytes(data,  byteorder="little", signed=False)
                    print(ps1_data)

                    # # Add raw value to mean calculation buffer
                    # ps1_mean_buf.append(ps1_data)

                    # # Calculate 5-sample mean
                    # ps1_mean = sum(ps1_mean_buf) / len(ps1_mean_buf)

                    # # Append to display buffers
                    # ps1_raw_buf.append(ps1_data)
                    # ps1_smooth_buf.append(ps1_mean)

                    # counters['sample_count'] += 1

                    # # Create x-axis that matches the actual buffer length
                    # buffer_length = len(ps1_raw_buf)
                    # x = list(range(counters['sample_count'] - buffer_length, counters['sample_count']))

                    # # Update curves based on display options
                    # if show_raw:
                    #     curve_ps1_raw.setData(x, list(ps1_raw_buf))
                    # else:
                    #     curve_ps1_raw.setData([], [])

                    # if show_smooth:
                    #     curve_ps1_smooth.setData(x, list(ps1_smooth_buf))
                    # else:
                    #     curve_ps1_smooth.setData([], [])

                    # Optional: console log
                    # print(
                    #     f"\rALS_VIS:{als_vis_data} ALS_IR:{als_ir_data} "
                    #     f"PS1:{ps1_data} PS2:{ps2_data} PS3:{ps3_data} AUX:{aux_data}   ",
                    #     end=""
                    # )
                except Exception as e:
                    pass
                    # Avoid crashing the UI on occasional read errors
                    #print(f"\nwarn: sensor read failed: {e}")

                # Calculate elapsed time and delay to maintain 50 Hz
                loop_elapsed = time.time() - loop_start
                sleep_time = target_period - loop_elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

            # timer = pg.QtCore.QTimer()
            # timer.timeout.connect(update)
            # timer.start(0)  # Maximum possible sample rate

            # sys.exit(app.exec_())
            
    # Disconnect tag 
    acr.disconnect()
