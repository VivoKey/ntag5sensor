import time, math

# General calls
I2C_CALL_RESET_CMD = 0x06


class I2CBase:
    def __init__(self, ntag5link, address):
        self.chip = ntag5link
        self.address = address

    def read_register(self, register, length):
        while(self.chip.check_i2c_busy()):
            print("info: I2C bus is still busy, waiting ...")
            time.sleep(0.1)
        self.chip.write_i2c(self.address, bytes([register]))
        if(not self.chip.check_i2c_write_result()):
            raise Exception("Register address write was not acknowledged")
        self.chip.read_i2c(self.address, length)
        # One page is four bytes
        data = self.chip.read_sram(num_blocks = math.ceil(length / 4.0))
        return data[0:length]

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
        self.chip.write_i2c(0x00, bytes([I2C_CALL_RESET_CMD]))
        if(not self.chip.check_i2c_write_result()):
            raise Exception("General call was not acknowledged")
