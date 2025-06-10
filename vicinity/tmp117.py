import time

TMP117_I2C_REG_TEMPERATURE =    0x00
TMP117_I2C_REG_CONFIG =         0x01  

# Config register flags
TMP117_CONFIG_FLAG_DATA_READY = (1 << 13)


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

    def read_temperature(self):
        config = self.read_register(TMP117_I2C_REG_CONFIG)
        config = int.from_bytes(config[0:2], byteorder="big")
        if(config & TMP117_CONFIG_FLAG_DATA_READY == TMP117_CONFIG_FLAG_DATA_READY):
            data = self.read_register(TMP117_I2C_REG_TEMPERATURE)
            return self.raw_to_celsius(data)
        else:
            # Caller should try again, no data ready yet
            return None
