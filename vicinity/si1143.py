import time
from .i2cbase import I2CBase

SI1143_I2C_ADDRESS =                0x5A

# Register addresses
SI1143_I2C_REG_PART_ID =            0x00
SI1143_I2C_REG_REV_ID =             0x01
SI1143_I2C_REG_SEQ_ID =             0x02
SI1143_I2C_REG_INT_CFG =            0x03
SI1143_I2C_REG_IRQ_ENABLE =         0x04
SI1143_I2C_REG_IRQ_MODE1 =          0x05
SI1143_I2C_REG_IRQ_MODE2 =          0x06
SI1143_I2C_REG_HW_KEY =             0x07
SI1143_I2C_REG_MEAS_RATE =          0x08
SI1143_I2C_REG_ALS_RATE =           0x09
SI1143_I2C_REG_PS_RATE =            0x0A
SI1143_I2C_REG_ALS_LOW_TH0 =        0x0B
SI1143_I2C_REG_ALS_LOW_TH1 =        0x0C
SI1143_I2C_REG_ALS_HI_TH0 =         0x0D
SI1143_I2C_REG_ALS_HI_TH1 =         0x0E
SI1143_I2C_REG_PS_LED21 =           0x0F
SI1143_I2C_REG_PS_LED3 =            0x10
SI1143_I2C_REG_PS1_TH0 =            0x11
SI1143_I2C_REG_PS1_TH1 =            0x12
SI1143_I2C_REG_PS2_TH0 =            0x13
SI1143_I2C_REG_PS2_TH1 =            0x14
SI1143_I2C_REG_PS3_TH0 =            0x15
SI1143_I2C_REG_PS3_TH1 =            0x16
SI1143_I2C_REG_PARAM_WR =           0x17
SI1143_I2C_REG_COMMAND =            0x18
SI1143_I2C_REG_RESPONSE =           0x20
SI1143_I2C_REG_IRQ_STATUS =         0x21
SI1143_I2C_REG_ALS_VIS_DATA0 =      0x22
SI1143_I2C_REG_ALS_VIS_DATA1 =      0x23
SI1143_I2C_REG_ALS_IR_DATA0 =       0x24
SI1143_I2C_REG_ALS_IR_DATA1 =       0x25
SI1143_I2C_REG_PS1_DATA0 =          0x26
SI1143_I2C_REG_PS1_DATA1 =          0x27
SI1143_I2C_REG_PS2_DATA0 =          0x28
SI1143_I2C_REG_PS2_DATA1 =          0x29
SI1143_I2C_REG_PS3_DATA0 =          0x2A
SI1143_I2C_REG_PS3_DATA1 =          0x2B
SI1143_I2C_REG_AUX_DATA0 =          0x2C
SI1143_I2C_REG_AUX_DATA1 =          0x2D
SI1143_I2C_REG_PARAM_RD =           0x2E
SI1143_I2C_REG_CHIP_STAT =          0x30
SI1143_I2C_REG_ANA_IN_KEY0 =        0x3B
SI1143_I2C_REG_ANA_IN_KEY1 =        0x3C
SI1143_I2C_REG_ANA_IN_KEY2 =        0x3D
SI1143_I2C_REG_ANA_IN_KEY3 =        0x3E

# Part IDs
SI1143_PART_ID_SI1141 =             0x41
SI1143_PART_ID_SI1142 =             0x42
SI1143_PART_ID_SI1143 =             0x43

# Sequencer IDs
SI1143_SEQ_ID_A01 =                 0x01
SI1143_SEQ_ID_A02 =                 0x02
SI1143_SEQ_ID_A03 =                 0x03
SI1143_SEQ_ID_A10 =                 0x08
SI1143_SEQ_ID_A11 =                 0x09

# Hardware key
SI1143_HW_KEY_VALUE =               0x17


class SI1143(I2CBase):
    def __init__(self, ntag5link):
        super().__init__(ntag5link, SI1143_I2C_ADDRESS)

    def initialize(self):
        # The hardware key register is needed to transition to standby mode
        self.write_register(SI1143_I2C_REG_HW_KEY, [SI1143_HW_KEY_VALUE])

    def get_info(self):
        res = {}

        # Part, revision and sequencer information
        part_id = self.read_register(SI1143_I2C_REG_PART_ID, 1)
        if(part_id == SI1143_PART_ID_SI1141):
            res["part_id"] = "Si1141"
        elif(part_id == SI1143_PART_ID_SI1142):
            res["part_id"] = "Si1142"
        elif(part_id == SI1143_PART_ID_SI1143):
            res["part_id"] = "Si1143"
        else:
            res["part_id"] = "Unknown"
        
        res["rev_id"] = self.read_register(SI1143_I2C_REG_REV_ID, 1)
        
        seq_id = self.read_register(SI1143_I2C_REG_SEQ_ID, 1)
        if(seq_id == SI1143_SEQ_ID_A01):
            res["seq_id"] = "Si114x-A01"
        elif(seq_id == SI1143_SEQ_ID_A02):
            res["seq_id"] = "Si114x-A02"
        elif(seq_id == SI1143_SEQ_ID_A03):
            res["seq_id"] = "Si114x-A03"
        elif(seq_id == SI1143_SEQ_ID_A10):
            res["seq_id"] = "Si114x-A10"
        elif(seq_id == SI1143_SEQ_ID_A11):
            res["seq_id"] = "Si114x-A11"
        else:
            res["seq_id"] = "Unknown"

        return res
