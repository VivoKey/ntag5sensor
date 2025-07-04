import time

# Register addresses
TMP117_I2C_REG_TEMP_RESULT =        0x00
TMP117_I2C_REG_CONFIG =             0x01
TMP117_I2C_REG_THIGH_LIMIT =        0x02
TMP117_I2C_REG_TLOW_LIMIT =         0x03
TMP117_I2C_REG_EEPROM_UL =          0x04
TMP117_I2C_REG_EEPROM1 =            0x05
TMP117_I2C_REG_EEPROM2 =            0x06
TMP117_I2C_REG_TEMP_OFFSET =        0x07
TMP117_I2C_REG_EEPROM3 =            0x08
TMP117_I2C_REG_DEVICE_ID =          0x0F

# Reset command
TMP117_I2C_CALL_RESET_CMD =         0x06

# Config register flags
TMP117_CONFIG_FLAG_SOFT_RESET =     (1 << 1)
TMP117_CONFIG_FLAG_ALERT_SEL =      (1 << 2)
TMP117_CONFIG_FLAG_ALERT_POL =      (1 << 3)
TMP117_CONFIG_FLAG_TA_MODE =        (1 << 4)
TMP117_CONFIG_FLAG_AVG_MASK =       (3 << 5)
TMP117_CONFIG_FLAG_CONV_MASK =      (7 << 7)
TMP117_CONFIG_FLAG_MOD_MASK =       (3 << 10)
TMP117_CONFIG_FLAG_EEPROM_BUSY =    (1 << 12)
TMP117_CONFIG_FLAG_DATA_READY =     (1 << 13)
TMP117_CONFIG_FLAG_LOW_ALERT =      (1 << 14)
TMP117_CONFIG_FLAG_HIGH_ALERT =     (1 << 15)

# Average modes
TMP117_CONFIG_FLAG_AVG_NONE =       (0 << 5)
TMP117_CONFIG_FLAG_AVG_8 =          (1 << 5)
TMP117_CONFIG_FLAG_AVG_32 =         (2 << 5)
TMP117_CONFIG_FLAG_AVG_64 =         (3 << 5)

# Operating modes
TMP117_CONFIG_FLAG_MOD_CONT =       (0 << 10)
TMP117_CONFIG_FLAG_MOD_SHUTDOWN =   (1 << 10)
TMP117_CONFIG_FLAG_MOD_CONT2 =      (2 << 10)
TMP117_CONFIG_FLAG_MOD_ONESHOT =    (3 << 10)

# Device ID
TMP117_DEVICE_ID_DID_MASK =         0x0FFF
TMP117_DEVICE_ID_REV_MASK =         0xF000

# EEPROM unlock flags
TMP117_EEPROM_UL_EUN =              (1 << 15)
TMP117_EEPROM_UL_EEPROM_BUSY =      (1 << 14)


class TMP117:
    def __init__(self, ntag5link, address):
        self.chip = ntag5link
        self.address = address

    def raw_to_celsius(self, data):
        return (int.from_bytes(data, byteorder = "big", signed = True) * 7.8125) / 1000.0

    def read_register(self, register):
        while(self.chip.check_i2c_busy()):
            print("info: I2C bus is still busy, waiting ...")
            time.sleep(0.1)
        self.chip.write_i2c(self.address, bytes([register]))
        if(not self.chip.check_i2c_write_result()):
            raise Exception("Register address write was not acknowledged")
        self.chip.read_i2c(self.address, 2)
        data = self.chip.read_sram()
        return data[0:2]

    def write_register(self, register, data):
        while(self.chip.check_i2c_busy()):
            print("info: I2C bus is still busy, waiting ...")
            time.sleep(0.1)
        self.chip.write_i2c(self.address, bytes([register] + data))
        if(not self.chip.check_i2c_write_result()):
            raise Exception("Register address and data write was not acknowledged")

    def general_reset(self):
        # Perform I2C General-Call Reset
        while(self.chip.check_i2c_busy()):
            print("info: I2C bus is still busy, waiting ...")
            time.sleep(0.1)
        self.chip.write_i2c(0x00, bytes([TMP117_I2C_CALL_RESET_CMD]))
        if(not self.chip.check_i2c_write_result()):
            raise Exception("General call was not acknowledged")

    def get_config_info(self):
        config = self.read_register(TMP117_I2C_REG_CONFIG)
        config = int.from_bytes(config[0:2], byteorder="big")

        res = {}

        # Status flags
        res["status_flags"] = {
            "high_alert": bool(config & TMP117_CONFIG_FLAG_HIGH_ALERT),
            "low_alert": bool(config & TMP117_CONFIG_FLAG_LOW_ALERT),
            "data_ready": bool(config & TMP117_CONFIG_FLAG_DATA_READY),
            "eeprom_busy": bool(config & TMP117_CONFIG_FLAG_EEPROM_BUSY),
        }

        # Operating mode
        mode_lookup = {
            TMP117_CONFIG_FLAG_MOD_CONT: "continuous",
            TMP117_CONFIG_FLAG_MOD_SHUTDOWN: "shutdown",
            TMP117_CONFIG_FLAG_MOD_CONT2: "continuous",
            TMP117_CONFIG_FLAG_MOD_ONESHOT: "one_shot",
        }
        mode_bits = config & TMP117_CONFIG_FLAG_MOD_MASK
        res["mode"] = mode_lookup.get(mode_bits, "unknown")

        # Averaging
        avg_lookup = {
            TMP117_CONFIG_FLAG_AVG_NONE: "none",
            TMP117_CONFIG_FLAG_AVG_8: "8",
            TMP117_CONFIG_FLAG_AVG_32: "32",
            TMP117_CONFIG_FLAG_AVG_64: "64",
        }
        avg = config & TMP117_CONFIG_FLAG_AVG_MASK
        res["averaging"] = avg_lookup.get(avg, "unknown")

        conv = (config & TMP117_CONFIG_FLAG_CONV_MASK) >> 7
        # Sparse table of differences from the "1s" default
        conv_exceptions = {
            0: {
                TMP117_CONFIG_FLAG_AVG_NONE: 15.5,
                TMP117_CONFIG_FLAG_AVG_8:    125,
                TMP117_CONFIG_FLAG_AVG_32:   500
            },
            1: {
                TMP117_CONFIG_FLAG_AVG_NONE: 125,
                TMP117_CONFIG_FLAG_AVG_8:    125,
                TMP117_CONFIG_FLAG_AVG_32:   500
            },
            2: {
                TMP117_CONFIG_FLAG_AVG_NONE: 250,
                TMP117_CONFIG_FLAG_AVG_8:    250,
                TMP117_CONFIG_FLAG_AVG_32:   500,
            },
            3: {
                TMP117_CONFIG_FLAG_AVG_NONE: 500,
                TMP117_CONFIG_FLAG_AVG_8:    500,
                TMP117_CONFIG_FLAG_AVG_32:   500,
            },
            5: 4000,
            6: 8000,
            7: 16000,
        }
        # Logic: fallback default is "1s"
        if isinstance(conv_exceptions.get(conv), dict):
            res["conversion_cycle"] = conv_exceptions[conv].get(avg, 1000)
        else:
            res["conversion_cycle"] = conv_exceptions.get(conv, 1000)

        # Alert config
        res["alert_config"] = {
            "therm_mode": bool(config & TMP117_CONFIG_FLAG_TA_MODE),
            "alert_polarity_high": bool(config & TMP117_CONFIG_FLAG_ALERT_POL),
            "alert_select_data_ready": bool(config & TMP117_CONFIG_FLAG_ALERT_SEL),
        }

        # Reset flag
        res["soft_reset"] = bool(config & TMP117_CONFIG_FLAG_SOFT_RESET)

        return res

    def get_eeprom_info(self):
        ret = {}

        ret["thigh_limit"] = self.raw_to_celsius(self.read_register(TMP117_I2C_REG_THIGH_LIMIT))
        ret["tlow_limit"] = self.raw_to_celsius(self.read_register(TMP117_I2C_REG_TLOW_LIMIT))
        ret["eeprom1"] = self.read_register(TMP117_I2C_REG_EEPROM1)
        ret["eeprom2"] = self.read_register(TMP117_I2C_REG_EEPROM2)
        ret["eeprom3"] = self.read_register(TMP117_I2C_REG_EEPROM3)
        ret["temperature_offset"] = self.raw_to_celsius(self.read_register(TMP117_I2C_REG_TEMP_OFFSET))
        device_id = self.read_register(TMP117_I2C_REG_DEVICE_ID)
        device_id = int.from_bytes(device_id[0:2], byteorder="big")
        ret["device_id"] = {
            "id": device_id & TMP117_DEVICE_ID_DID_MASK,
            "rev": (device_id & TMP117_DEVICE_ID_REV_MASK) >> 12
        }

        return ret
            
    def write_config(self, eeprom_persistent = False, conversion_mode = None, 
            conversion_cycle = None, conversion_averaging = None):
        # Read current values
        config = self.read_register(TMP117_I2C_REG_CONFIG)
        config = int.from_bytes(config[0:2], byteorder="big")
        
        # Apply new parameters
        if(conversion_mode != None):
            config &= ~TMP117_CONFIG_FLAG_MOD_MASK
            config |= conversion_mode 
        if(conversion_cycle != None):
            config &= ~TMP117_CONFIG_FLAG_CONV_MASK
            config |= ((conversion_cycle << 7) & TMP117_CONFIG_FLAG_CONV_MASK)
        if(conversion_averaging != None):    
            config &= ~TMP117_CONFIG_FLAG_AVG_MASK
            config |= conversion_averaging

        if(not eeprom_persistent):
            # Write to memory only
            self.write_register(TMP117_I2C_REG_CONFIG, list(config.to_bytes(2, byteorder="big")))
        else:
            # Unlock the EEPROM by setting unlock bit in unlock register
            self.write_register(TMP117_I2C_REG_EEPROM_UL, list(TMP117_EEPROM_UL_EUN.to_bytes(2, byteorder="big")))
            # Write config to persistent storage
            self.write_register(TMP117_I2C_REG_CONFIG, list(config.to_bytes(2, byteorder="big")))
            # Wait for EEPROM write to complete
            while(True):
                # Check EEPROM busy flag
                eeprom_ul = self.read_register(TMP117_I2C_REG_EEPROM_UL)
                eeprom_ul = int.from_bytes(eeprom_ul[0:2], byteorder="big")
                if(eeprom_ul & TMP117_EEPROM_UL_EEPROM_BUSY == 0):
                    print("info: EEPROM writing completed")
                    break
                print("info: EEPROM writing is still ongoing, waiting ...")
                time.sleep(0.1)
            # Reset the chip
            self.general_reset()
            # Read the changed values
            config_new = self.read_register(TMP117_I2C_REG_CONFIG)
            config_new = int.from_bytes(config_new[0:2], byteorder="big")
            if(config_new != config):
                raise Exception("Could not confirm EEPROM changes after reset")

    def read_temperature(self):
        config = self.read_register(TMP117_I2C_REG_CONFIG)
        config = int.from_bytes(config[0:2], byteorder="big")
        if(bool(config & TMP117_CONFIG_FLAG_DATA_READY)):
            data = self.read_register(TMP117_I2C_REG_TEMP_RESULT)
            return self.raw_to_celsius(data)
        else:
            # Caller should try again, no data ready yet
            return None