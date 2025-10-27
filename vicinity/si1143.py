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

# Commands
SI1143_CMD_PARAM_QUERY =            0x80
SI1143_CMD_PARAM_SET =              0xA0
SI1143_CMD_PARAM_AND =              0xC0
SI1143_CMD_PARAM_OR =               0xE0
SI1143_CMD_NOP =                    0x00
SI1143_CMD_RESET =                  0x01
SI1143_CMD_BUSADDR =                0x02
SI1143_CMD_PS_FORCE =               0x05
SI1143_CMD_ALS_FORCE =              0x06
SI1143_CMD_PSALS_FORCE =            0x07
SI1143_CMD_PS_PAUSE =               0x09
SI1143_CMD_ALS_PAUSE =              0x0A
SI1143_CMD_PSALS_PAUSE =            0x0B
SI1143_CMD_PS_AUTO =                0x0D
SI1143_CMD_ALS_AUTO =               0x0E
SI1143_CMD_PSALS_AUTO =             0x0F

# Parameter RAM addresses
SI1143_PARAM_I2C_ADDR =             0x00
SI1143_PARAM_CHLIST =               0x01
SI1143_PARAM_PSLED12_SELECT =       0x02
SI1143_PARAM_PSLED3_SELECT =        0x03
SI1143_PARAM_PS_ENCODING =          0x05
SI1143_PARAM_ALS_ENCODING =         0x06
SI1143_PARAM_PS1_ADCMUX =           0x07
SI1143_PARAM_PS2_ADCMUX =           0x08
SI1143_PARAM_PS3_ADCMUX =           0x09
SI1143_PARAM_PS_ADC_COUNTER =       0x0A
SI1143_PARAM_PS_ADC_GAIN =          0x0B
SI1143_PARAM_PS_ADC_MISC =          0x0C
SI1143_PARAM_ALS_IR_ADCMUX =        0x0E
SI1143_PARAM_AUX_ADCMUX =           0x0F
SI1143_PARAM_ALS_VIS_ADC_COUNTER =  0x10
SI1143_PARAM_ALS_VIS_ADC_GAIN =     0x11
SI1143_PARAM_ALS_VIS_ADC_MISC =     0x12
SI1143_PARAM_ALS_HYST =             0x16
SI1143_PARAM_PS_HYST =              0x17
SI1143_PARAM_PS_HISTORY =           0x18
SI1143_PARAM_ALS_HISTORY =          0x19
SI1143_PARAM_ADC_OFFSET =           0x1A
SI1143_PARAM_LED_REC =              0x1C
SI1143_PARAM_ALS_IR_ADC_COUNTER =   0x1D
SI1143_PARAM_ALS_IR_ADC_GAIN =      0x1E
SI1143_PARAM_ALS_IR_ADC_MISC =      0x1F

# Responses
SI1143_RESP_NO_ERROR =              0x00
SI1143_RESP_INVALID_SETTING =       0x80
SI1143_RESP_PS1_ADC_OVERFLOW =      0x88
SI1143_RESP_PS2_ADC_OVERFLOW =      0x89
SI1143_RESP_PS3_ADC_OVERFLOW =      0x8A
SI1143_RESP_VIS_ADC_OVERFLOW =      0x8C
SI1143_RESP_IR_ADC_OVERFLOW =       0x8D
SI1143_RESP_AUX_ADC_OVERFLOW =      0x8E

# Measurement frequency 
SI1143_MEASURE_10MS =               0x84
SI1143_MEASURE_20MS =               0x94
SI1143_MEASURE_100MS =              0xB9
SI1143_MEASURE_496MS =              0xDF
SI1143_MEASURE_984MS =              0xFF
SI1143_MEASURE_AFTER_NEVER =        0x00
SI1143_MEASURE_AFTER_1 =            0x08
SI1143_MEASURE_AFTER_10 =           0x32
SI1143_MEASURE_AFTER_100 =          0x69

# Channel list config
SI1143_CHLIST_EN_AUX =              0x40
SI1143_CHLIST_EN_ALS_IR =           0x20
SI1143_CHLIST_EN_ALS_VIS =          0x10
SI1143_CHLIST_EN_PS3 =              0x04
SI1143_CHLIST_EN_PS2 =              0x02
SI1143_CHLIST_EN_PS1 =              0x01

# LED driver per channel config
SI1143_PSLED12_SELECT_PS1_NONE =    0x00
SI1143_PSLED12_SELECT_PS1_LED1 =    0x01
SI1143_PSLED12_SELECT_PS1_LED2 =    0x02
SI1143_PSLED12_SELECT_PS1_LED3 =    0x04
SI1143_PSLED12_SELECT_PS2_NONE =    0x00
SI1143_PSLED12_SELECT_PS2_LED1 =    0x10
SI1143_PSLED12_SELECT_PS2_LED2 =    0x20
SI1143_PSLED12_SELECT_PS2_LED3 =    0x40
SI1143_PSLED3_SELECT_PS3_NONE =     0x00
SI1143_PSLED3_SELECT_PS3_LED1 =     0x01
SI1143_PSLED3_SELECT_PS3_LED2 =     0x02
SI1143_PSLED3_SELECT_PS3_LED3 =     0x04

# ADC misc configuration
SI1143_PS_ADC_MISC_NORMAL_SIGNAL_RANGE =    0x00
SI1143_PS_ADC_MISC_HIGH_SIGNAL_RANGE =      0x20
SI1143_PS_ADC_MISC_RAW_ADC_MEAS_MODE =      0x00
SI1143_PS_ADC_MISC_NORMAL_PROX_MEAS_MODE =  0x04

# ADC gain configuration 
SI1143_PS_ADC_GAIN_DIV_1 =          0x00
SI1143_PS_ADC_GAIN_DIV_2 =          0x01
SI1143_PS_ADC_GAIN_DIV_4 =          0x02
SI1143_PS_ADC_GAIN_DIV_8 =          0x03
SI1143_PS_ADC_GAIN_DIV_16 =         0x04
SI1143_PS_ADC_GAIN_DIV_32 =         0x05
SI1143_PS_ADC_GAIN_DIV_64 =         0x06
SI1143_PS_ADC_GAIN_DIV_128 =        0x07

# INT_CFG register bit definitions
SI1143_INT_CFG_AUTO_CLEAR =         0x04
SI1143_INT_CFG_PIN_EN =             0x01

# IRQ_ENABLE register bit definitions
SI1143_IRQ_ENABLE_PS1_INT_EN =      0x01
SI1143_IRQ_ENABLE_PS2_INT_EN =      0x02
SI1143_IRQ_ENABLE_PS3_INT_EN =      0x04
SI1143_IRQ_ENABLE_ALS_INT_EN =      0x08
SI1143_IRQ_ENABLE_CMD_INT_EN =      0x20

# IRQ_MODE2 register bit definitions
SI1143_CMD_INT_RESP_ERROR =          0x04

# MEAS_RATE register values
SI1143_DEV_WAKEUP_MYSTERY =          0x38
SI1143_DEV_WAKEUP_EVERY_10MS =       0x84

# ALS_RATE and PS_RATE register values
SI1143_MEAS_AFTER_EVERY_WAKEUP =     0x08

# LED current definitions
SI1143_LED_NO_CURRENT =              0x00
SI1143_LED_MIN_CURRENT =             0x01
SI1143_LED_MAX_CURRENT =             0x0F

# Interrupt flags
SI1143_CMD_INT_FLAG =                0x20
SI1143_PS3_INT_FLAG =                0x10
SI1143_PS2_INT_FLAG =                0x08
SI1143_PS1_INT_FLAG =                0x04
SI1143_ALS_INT_FLAG =                0x03
SI1143_INT_CLEARED =                 0x00


class SI1143(I2CBase):
    def __init__(self, ntag5link):
        super().__init__(ntag5link, SI1143_I2C_ADDRESS)

    def initialize(self):
        # The hardware key register is needed to transition to standby mode
        self.write_register(SI1143_I2C_REG_HW_KEY, [SI1143_HW_KEY_VALUE])

    def get_info(self):
        res = {}

        # Part, revision and sequencer information
        part_id = self.read_register(SI1143_I2C_REG_PART_ID, 1)[0]
        if(part_id == SI1143_PART_ID_SI1141):
            res["part_id"] = "Si1141"
        elif(part_id == SI1143_PART_ID_SI1142):
            res["part_id"] = "Si1142"
        elif(part_id == SI1143_PART_ID_SI1143):
            res["part_id"] = "Si1143"
        else:
            res["part_id"] = "Unknown"
        
        res["rev_id"] = self.read_register(SI1143_I2C_REG_REV_ID, 1)[0]
        
        seq_id = self.read_register(SI1143_I2C_REG_SEQ_ID, 1)[0]
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

    def command(self, command, param_w = None):
        # First, clear the response register by sensing a NOP command
        self.write_register(SI1143_I2C_REG_COMMAND, [SI1143_CMD_NOP])
        response = self.read_register(SI1143_I2C_REG_RESPONSE, 1)[0]
        if(response != SI1143_RESP_NO_ERROR):
            raise Exception(f"Response after NOP was not empty (was {hex(response)})")
        
        # Preload the write parameter if specified
        if(param_w != None):
            self.write_register(SI1143_I2C_REG_PARAM_WR, [param_w])

        # Execute the command
        self.write_register(SI1143_I2C_REG_COMMAND, [command])

        # Wait for the command to execute and update the response register
        if(command != SI1143_CMD_RESET):
            # For non-reset commands, read the response
            response = 0x00
            counter = 0
            while(True):
                response = self.read_register(SI1143_I2C_REG_RESPONSE, 1)[0]
                if(response != 0x00):
                    break
                else:
                    time.sleep(0.01)
                    counter += 1
                    # After checking 5 times (50 ms), abort
                    if(counter > 5):
                        raise Exception("Response did not arrive within 50ms")

            # Check the response
            if(response >= 0x00 and response <= 0x0F):
                # Success, read param_rd
                param_rd = self.read_register(SI1143_I2C_REG_PARAM_RD, 1)[0]
                return param_rd
            elif(response == SI1143_RESP_INVALID_SETTING):
                raise Exception("Invalid Command Encountered during command processing")
            elif(response == SI1143_RESP_PS1_ADC_OVERFLOW):
                raise Exception("ADC Overflow encountered during PS1 measurement")
            elif(response == SI1143_RESP_PS2_ADC_OVERFLOW):
                raise Exception("ADC Overflow encountered during PS2 measurement")
            elif(response == SI1143_RESP_PS3_ADC_OVERFLOW):
                raise Exception("ADC Overflow encountered during PS3 measurement")
            elif(response == SI1143_RESP_VIS_ADC_OVERFLOW):
                raise Exception("ADC Overflow encountered during ALS-VIS measurement")
            elif(response == SI1143_RESP_IR_ADC_OVERFLOW):
                raise Exception("ADC Overflow encountered during ALS-IR measurement")
            elif(response == SI1143_RESP_AUX_ADC_OVERFLOW):
                raise Exception("ADC Overflow encountered during AUX measurement")

        else:
            # Wait for reset command to finish
            time.sleep(0.01)