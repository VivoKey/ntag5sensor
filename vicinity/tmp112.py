import time
from .i2cbase import I2CBase

# Register addresses
TMP112_I2C_REG_TEMP_RESULT =            0x00
TMP112_I2C_REG_CONFIG =                 0x01
TMP112_I2C_REG_TLOW_LIMIT =             0x02
TMP112_I2C_REG_THIGH_LIMIT =            0x03

# Config register flags
TMP112_CONFIG_FLAG_EXTENDED_MODE =      (1 << 4)
TMP112_CONFIG_FLAG_ALERT =              (1 << 5)
TMP112_CONFIG_FLAG_CONV_RATE_MASK =     (3 << 6)
TMP112_CONFIG_FLAG_SHUTDOWN_MODE =      (1 << 8)
TMP112_CONFIG_FLAG_THERMOSTAT_MODE =    (1 << 9)
TMP112_CONFIG_FLAG_ALERT_POL =          (1 << 10)
TMP112_CONFIG_FLAG_FAULT_QUEUE_MASK =   (3 << 11)
TMP112_CONFIG_FLAG_RESOLUTION_MASK =    (3 << 13)
TMP112_CONFIG_FLAG_ONESHOT =            (1 << 15)

# Consecutive faults
TMP112_CONFIG_FLAG_FAULT_QUEUE_1 =      (0 << 11)
TMP112_CONFIG_FLAG_FAULT_QUEUE_2 =      (1 << 11)
TMP112_CONFIG_FLAG_FAULT_QUEUE_4 =      (2 << 11)
TMP112_CONFIG_FLAG_FAULT_QUEUE_6 =      (3 << 11)

# Resolution
TMP112_CONFIG_FLAG_RESOLUTION_12 =      (3 << 13)

# Conversion rates
TMP112_CONFIG_FLAG_CONVERSION_0_25 =    (0 << 6)
TMP112_CONFIG_FLAG_CONVERSION_1 =       (1 << 6)
TMP112_CONFIG_FLAG_CONVERSION_4 =       (2 << 6)
TMP112_CONFIG_FLAG_CONVERSION_8 =       (3 << 6)


class TMP112(I2CBase):
    def __init__(self, ntag5link, address):
        super().__init__(ntag5link, address)

    def raw_to_celsius(self, data):
        return ((int.from_bytes(data, byteorder = "big", signed = False) >> 4) * 62.5) / 1000.0

    def get_config_info(self):
        config = self.read_register(TMP112_I2C_REG_CONFIG, 2)
        config = int.from_bytes(config[0:2], byteorder="big")

        res = {}

        # Limits
        res["tlow_limit"] = self.raw_to_celsius(self.read_register(TMP112_I2C_REG_TLOW_LIMIT, 2))
        res["thigh_limit"] = self.raw_to_celsius(self.read_register(TMP112_I2C_REG_THIGH_LIMIT, 2))

        # Config flags
        res["shutdown_mode"] = bool(config & TMP112_CONFIG_FLAG_SHUTDOWN_MODE)
        res["thermostat_mode"] = bool(config & TMP112_CONFIG_FLAG_THERMOSTAT_MODE)
        res["alert_polarity_high"] = bool(config & TMP112_CONFIG_FLAG_ALERT_POL)
        res["oneshot"] = bool(config & TMP112_CONFIG_FLAG_ONESHOT)
        res["extended_mode"] = bool(config & TMP112_CONFIG_FLAG_EXTENDED_MODE)
        res["alert"] = bool(config & TMP112_CONFIG_FLAG_ALERT)

        # Fault queue
        fault_queue = config & TMP112_CONFIG_FLAG_FAULT_QUEUE_MASK
        fault_queue_lookup = {
            TMP112_CONFIG_FLAG_FAULT_QUEUE_1: 1,
            TMP112_CONFIG_FLAG_FAULT_QUEUE_2: 2,
            TMP112_CONFIG_FLAG_FAULT_QUEUE_4: 4,
            TMP112_CONFIG_FLAG_FAULT_QUEUE_6: 6,
        }
        res["fault_queue"] = fault_queue_lookup.get(fault_queue, 0)

        # Resolution
        resolution = config & TMP112_CONFIG_FLAG_RESOLUTION_MASK
        res["resolution"] = "12 Bit" if resolution == TMP112_CONFIG_FLAG_RESOLUTION_12 else "Unknown"

        # Conversion rate
        conv_rate = config & TMP112_CONFIG_FLAG_CONV_RATE_MASK
        conv_rate_lookup = {
            TMP112_CONFIG_FLAG_CONVERSION_0_25: "0.25 Hz",
            TMP112_CONFIG_FLAG_CONVERSION_1: "1 Hz",
            TMP112_CONFIG_FLAG_CONVERSION_4: "4 Hz",
            TMP112_CONFIG_FLAG_CONVERSION_8: "8 Hz",
        }
        res["conversion_rate"] = conv_rate_lookup.get(conv_rate, "Unknown")

        return res
            
    def write_config(self, shutdown_mode = False, oneshot = None):
        # Read current values
        config = self.read_register(TMP112_I2C_REG_CONFIG, 2)
        config = int.from_bytes(config[0:2], byteorder="big")
        
        # Apply new parameters
        if(shutdown_mode != None):
            config &= ~TMP112_CONFIG_FLAG_SHUTDOWN_MODE
            config |= TMP112_CONFIG_FLAG_SHUTDOWN_MODE if shutdown_mode else 0x00
        if(oneshot != None):
            config &= ~TMP112_CONFIG_FLAG_ONESHOT
            config |= TMP112_CONFIG_FLAG_ONESHOT if oneshot else 0x00
       
        self.write_register(TMP112_I2C_REG_CONFIG, list(config.to_bytes(2, byteorder="big")))
       
    def read_temperature(self):
        config = self.read_register(TMP112_I2C_REG_CONFIG, 2)
        config = int.from_bytes(config[0:2], byteorder="big")
        # Oneshot mode starts from shutdown
        if(bool(config & TMP112_CONFIG_FLAG_SHUTDOWN_MODE)):
            # OS = 0 during conversion, OS = 1 when finished
            if(not bool(config & TMP112_CONFIG_FLAG_ONESHOT)):
                # Caller should try again, no data ready yet
                return None
        data = self.read_register(TMP112_I2C_REG_TEMP_RESULT, 2)
        return self.raw_to_celsius(data)
