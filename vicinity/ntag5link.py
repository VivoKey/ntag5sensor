from .iso15693 import *


# Command codes
NXP_CMD_SYSTEM_INFO =                           0xAB
NXP_CMD_READ_CONFIG =                           0xC0
NXP_CMD_WRITE_CONFIG =                          0xC1
NXP_CMD_READ_SRAM =                             0xD2
NXP_CMD_READ_I2C =                              0xD5
NXP_CMD_WRITE_I2C =                             0xD4

# Command parameters
NXP_CMD_MANUF_CODE_NXP =                        0x04

# Config addresses
NXP_CONFIG_ADDR_CONFIG =                        0x37
NXP_CONFIG_ADDR_EH_CONFIG_REG =                 0xA7
NXP_CONFIG_ADDR_I2C_M_STATUS_REG =              0xAD
NXP_CONFIG_ADDR_EH_CONFIG =                     0x3D

# Config flags
NXP_CONFIG_0_AUTO_STANDBY_MODE_EN =             (1 << 0)
NXP_CONFIG_0_LOCK_SESSION_REG =                 (1 << 1)
NXP_CONFIG_0_EH_MODE_RFU0 =                     (0 << 2)
NXP_CONFIG_0_EH_MODE_RFU1 =                     (1 << 2)
NXP_CONFIG_0_EH_MODE_LOW_FIELD_STRENGTH =       (2 << 2)
NXP_CONFIG_0_EH_MODE_HIGH_FIELD_STRENGTH =      (3 << 2)
NXP_CONFIG_0_SRAM_COPY_EN =                     (1 << 7)

NXP_CONFIG_1_PT_TRANSFER_DIR =                  (1 << 0)
NXP_CONFIG_1_SRAM_ENABLE =                      (1 << 1)
NXP_CONFIG_1_ARBITER_MODE_NORMAL =              (0 << 2)
NXP_CONFIG_1_ARBITER_MODE_SRAM_MIRROR =         (1 << 2)
NXP_CONFIG_1_ARBITER_MODE_SRAM_PASSTHROUGH =    (2 << 2)
NXP_CONFIG_1_ARBITER_MODE_SRAM_PHDC =           (3 << 2)
NXP_CONFIG_1_USE_CASE_CONF_I2C_SLAVE =          (0 << 4)
NXP_CONFIG_1_USE_CASE_CONF_I2C_MASTER =         (1 << 4)
NXP_CONFIG_1_USE_CASE_CONF_GPIO_PWM =           (2 << 4)
NXP_CONFIG_1_USE_CASE_CONF_TRISTATE =           (3 << 4)
NXP_CONFIG_1_EH_ARBITER_MODE_EN =               (1 << 7)

NXP_CONFIG_2_GPIO0_SLEW_RATE =                  (1 << 0)
NXP_CONFIG_2_GPIO1_SLEW_RATE =                  (1 << 1)
NXP_CONFIG_2_LOCK_BLOCK_COMMAND_SUPPORTED =     (1 << 2)
NXP_CONFIG_2_EXTENDED_COMMANDS_SUPPORTED =      (1 << 3)
NXP_CONFIG_2_GPIO0_PAD_IN_DISABLED =            (0 << 4)
NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN_PULLUP =        (1 << 4)
NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN =               (2 << 4)
NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN_PULLDOWN =      (3 << 4)
NXP_CONFIG_2_GPIO1_PAD_IN_DISABLED =            (0 << 6)
NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN_PULLUP =        (1 << 6)
NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN =               (2 << 6)
NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN_PULLDOWN =      (3 << 6)

# Master mode I2C status flags
NXP_I2C_M_WDT_EXPIRED_MASK =                    0x08
NXP_I2C_M_TRANS_STATUS_MASK =                   0x06
NXP_I2C_M_BUSY_MASK =                           0x01
NXP_I2C_M_TRANS_STATUS_RESET =                  (0 << 1)
NXP_I2C_M_TRANS_STATUS_ADDRESS_NAK =            (1 << 1)
NXP_I2C_M_TRANS_STATUS_DATA_NAK =               (2 << 1)
NXP_I2C_M_TRANS_STATUS_SUCCESS =                (3 << 1)

# Energy harvesting config flags
NXP_EH_ENABLE =                                 (1 << 0)
NXP_EH_TRIGGER =                                (1 << 3)
NXP_EH_LOAD_OK =                                (1 << 7)

# Protection Pointer Condition bits (bit 0–5)
NXP_CMD_SYSTEM_INFO_FLAG_PPC_RL =               (1 << 0)
NXP_CMD_SYSTEM_INFO_FLAG_PPC_WL =               (1 << 1)
NXP_CMD_SYSTEM_INFO_FLAG_PPC_RH =               (1 << 4)
NXP_CMD_SYSTEM_INFO_FLAG_PPC_WH =               (1 << 5)

# Lock Bits (bit 1–3)
NXP_CMD_SYSTEM_INFO_FLAG_LOCK_EAS =             (1 << 1)
NXP_CMD_SYSTEM_INFO_FLAG_LOCK_DSFID =           (1 << 2)
NXP_CMD_SYSTEM_INFO_FLAG_LOCK_NFC_PP_AREA_0H =  (1 << 3)

# Feature flags byte 0 (bit 0–7)
NXP_CMD_SYSTEM_INFO_FLAG_UM_PROT =              (1 << 0)
NXP_CMD_SYSTEM_INFO_FLAG_COUNTER =              (1 << 1)
NXP_CMD_SYSTEM_INFO_FLAG_EAS_ID =               (1 << 2)
NXP_CMD_SYSTEM_INFO_FLAG_EAS_PROT =             (1 << 3)
NXP_CMD_SYSTEM_INFO_FLAG_AFI_PROT =             (1 << 4)
NXP_CMD_SYSTEM_INFO_FLAG_INV_READ_EXT =         (1 << 5)
NXP_CMD_SYSTEM_INFO_FLAG_EAS_IR =               (1 << 6)
NXP_CMD_SYSTEM_INFO_FLAG_CID =                  (1 << 7)

# Feature flags byte 1 (bit 0–7)
NXP_CMD_SYSTEM_INFO_FLAG_PERSISTENT_QUIET =     (1 << 2)
NXP_CMD_SYSTEM_INFO_FLAG_NFC_PRIVACY =          (1 << 4)
NXP_CMD_SYSTEM_INFO_FLAG_DESTROY =              (1 << 5)
NXP_CMD_SYSTEM_INFO_FLAG_WRITE_CID =            (1 << 6)
NXP_CMD_SYSTEM_INFO_FLAG_HIGH_BITRATES =        (1 << 7)

# Feature flags byte 2 (bit 0)
NXP_CMD_SYSTEM_INFO_FLAG_ORIG_SIG =             (1 << 0)

# Feature flags byte 3 (bit 0–7)
NXP_CMD_SYSTEM_INFO_FLAG_NUM_KEYS_MASK =        0x0F
NXP_CMD_SYSTEM_INFO_FLAG_INTERFACE_SHIFT =      5
NXP_CMD_SYSTEM_INFO_FLAG_INTERFACE_MASK =       0x60
NXP_CMD_SYSTEM_INFO_FLAG_EXT_FLAG =             (1 << 7)

# Energy harvesting configuration flags
NXP_EH_CONFIG_EH_ENABLE =                       (1 << 0)
NXP_EH_CONFIG_DISABLE_POWER_CHECK =             (1 << 3)

# Energy harvesting output current selection
NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4 =               (0 << 4)
NXP_EH_CONFIG_EH_VOUT_I_SEL_0_6 =               (1 << 4)
NXP_EH_CONFIG_EH_VOUT_I_SEL_1_4 =               (2 << 4)
NXP_EH_CONFIG_EH_VOUT_I_SEL_2_7 =               (3 << 4)
NXP_EH_CONFIG_EH_VOUT_I_SEL_4_0 =               (4 << 4)
NXP_EH_CONFIG_EH_VOUT_I_SEL_6_5 =               (5 << 4)
NXP_EH_CONFIG_EH_VOUT_I_SEL_9_0 =               (6 << 4)
NXP_EH_CONFIG_EH_VOUT_I_SEL_12_5 =              (7 << 4)

# Energy harvesting output voltage selection
NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8 =               (0 << 1)
NXP_EH_CONFIG_EH_VOUT_V_SEL_2_4 =               (1 << 1)
NXP_EH_CONFIG_EH_VOUT_V_SEL_3_0 =               (2 << 1)
NXP_EH_CONFIG_EH_VOUT_V_SEL_RFU =               (3 << 1)

# Energy detection configuration flags
NXP_ED_CONFIG_DISABLE =                         0x00
NXP_ED_CONFIG_NFC_FIELD_DETECT =                0x01
NXP_ED_CONFIG_PWM =                             0x02
NXP_ED_CONFIG_I2C_TO_NFC_PASS_THROUGH =         0x03
NXP_ED_CONFIG_NFC_TO_I2C_PASS_THROUGH =         0x04
NXP_ED_CONFIG_ARBITER_LOCK =                    0x05
NXP_ED_CONFIG_NDEF_MSG_TLV_LENGTH =             0x06
NXP_ED_CONFIG_STANDBY_MODE =                    0x07
NXP_ED_CONFIG_WRITE_CMD_INDICATION =            0x08
NXP_ED_CONFIG_READ_CMD_INDICATION =             0x09
NXP_ED_CONFIG_START_OF_COMMAND_INDICATION =     0x0A
NXP_ED_CONFIG_READ_FROM_SYNCH_BLOCK =           0x0B
NXP_ED_CONFIG_WRITE_TO_SYNCH_BLOCK =            0x0C
NXP_ED_CONFIG_SOFTWARE_INTERRUPT =              0x0D
NXP_ED_CONFIG_RFU1 =                            0x0E
NXP_ED_CONFIG_RFU2 =                            0x0F


class NTAG5Link(ISO15693):
    def __init__(self, reader):
        super().__init__(reader)

    def get_nxp_info(self):
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, NXP_CMD_SYSTEM_INFO, NXP_CMD_MANUF_CODE_NXP]))

        res = {}

        res["pp_pointer"] = data[0]

        pp_cond = data[1]
        res["pp_condition"] = {
            "read_protect_page_0l": bool(pp_cond & NXP_CMD_SYSTEM_INFO_FLAG_PPC_RL),
            "write_protect_page_0l": bool(pp_cond & NXP_CMD_SYSTEM_INFO_FLAG_PPC_WL),
            "read_protect_page_0h": bool(pp_cond & NXP_CMD_SYSTEM_INFO_FLAG_PPC_RH),
            "write_protect_page_0h": bool(pp_cond & NXP_CMD_SYSTEM_INFO_FLAG_PPC_WH),
        }

        lock_bits = data[2]
        res["lock_bits"] = {
            "eas_locked": bool(lock_bits & NXP_CMD_SYSTEM_INFO_FLAG_LOCK_EAS),
            "dsfid_locked": bool(lock_bits & NXP_CMD_SYSTEM_INFO_FLAG_LOCK_DSFID),
            "nfc_pp_area_0h_locked": bool(lock_bits & NXP_CMD_SYSTEM_INFO_FLAG_LOCK_NFC_PP_AREA_0H),
        }

        interface_lookup = {
            0x00: "only_nfc",
            0x01: "gpio",
            0x02: "rfu",
            0x03: "gpio_i2c"
        }

        b0, b1, b2, b3 = data[3:7]
        res["features"] = {
            # Byte 0
            "user_memory_protection": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_UM_PROT),
            "counter": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_COUNTER),
            "eas_id": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_EAS_ID),
            "eas_protection": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_EAS_PROT),
            "afi_protection": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_AFI_PROT),
            "inventory_read_ext": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_INV_READ_EXT),
            "eas_ir": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_EAS_IR),
            "cid": bool(b0 & NXP_CMD_SYSTEM_INFO_FLAG_CID),

            # Byte 1
            "persistent_quiet": bool(b1 & NXP_CMD_SYSTEM_INFO_FLAG_PERSISTENT_QUIET),
            "nfc_privacy": bool(b1 & NXP_CMD_SYSTEM_INFO_FLAG_NFC_PRIVACY),
            "destroy": bool(b1 & NXP_CMD_SYSTEM_INFO_FLAG_DESTROY),
            "write_cid": bool(b1 & NXP_CMD_SYSTEM_INFO_FLAG_WRITE_CID),
            "high_bitrates": bool(b1 & NXP_CMD_SYSTEM_INFO_FLAG_HIGH_BITRATES),

            # Byte 2
            "originality_signature": bool(b2 & NXP_CMD_SYSTEM_INFO_FLAG_ORIG_SIG),

            # Byte 3
            "extended_flags_present": bool(b3 & NXP_CMD_SYSTEM_INFO_FLAG_EXT_FLAG),
            "interface": interface_lookup.get(
                ((b3 & NXP_CMD_SYSTEM_INFO_FLAG_INTERFACE_MASK) >> NXP_CMD_SYSTEM_INFO_FLAG_INTERFACE_SHIFT), 
                "unknown"),
            "num_keys": b3 & NXP_CMD_SYSTEM_INFO_FLAG_NUM_KEYS_MASK
        }

        if res["features"]["extended_flags_present"]:
            res["extended_feature_flags_raw"] = data[7:11]

        return res

    def read_config_block(self, address, num_blocks = 1):
        # The base command always reads one block more than specified
        if(num_blocks < 1):
            raise Exception("Must read at least one block")
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, NXP_CMD_READ_CONFIG, NXP_CMD_MANUF_CODE_NXP, 
                address, num_blocks - 1]))
        return data

    def get_config_info(self):
        config = self.read_config_block(NXP_CONFIG_ADDR_CONFIG)

        b0, b1, b2 = config[:3]
        res = {} 
       
        # Byte 0
        res["auto_standby_mode_enabled"] = bool(b0 & NXP_CONFIG_0_AUTO_STANDBY_MODE_EN)
        res["lock_session_register"] = bool(b0 & NXP_CONFIG_0_LOCK_SESSION_REG)

        eh_mode = b0 & NXP_CONFIG_0_EH_MODE_HIGH_FIELD_STRENGTH # mask includes all eh mode bits
        if eh_mode == NXP_CONFIG_0_EH_MODE_LOW_FIELD_STRENGTH:
            res["energy_harvesting_mode"] = "low_field_strength"
        elif eh_mode == NXP_CONFIG_0_EH_MODE_HIGH_FIELD_STRENGTH:
            res["energy_harvesting_mode"] = "high_field_strength"
        elif eh_mode == NXP_CONFIG_0_EH_MODE_RFU0:
            res["energy_harvesting_mode"] = "rfu0"
        elif eh_mode == NXP_CONFIG_0_EH_MODE_RFU1:
            res["energy_harvesting_mode"] = "rfu1"
        
        res["sram_copy_enabled"] = bool(b0 & NXP_CONFIG_0_SRAM_COPY_EN)

        # Byte 1
        res["pt_transfer_direction"] = "reader_to_tag" if (b1 & NXP_CONFIG_1_PT_TRANSFER_DIR) else "tag_to_reader"
        res["sram_enabled"] = bool(b1 & NXP_CONFIG_1_SRAM_ENABLE)

        arbiter_mode = b1 & NXP_CONFIG_1_ARBITER_MODE_SRAM_PHDC # mask includes all arbiter bits
        arbiter_map = {
            NXP_CONFIG_1_ARBITER_MODE_NORMAL: "normal",
            NXP_CONFIG_1_ARBITER_MODE_SRAM_MIRROR: "sram_mirror",
            NXP_CONFIG_1_ARBITER_MODE_SRAM_PASSTHROUGH: "sram_passthrough",
            NXP_CONFIG_1_ARBITER_MODE_SRAM_PHDC: "sram_phdc",
        }
        res["arbiter_mode"] = arbiter_map.get(arbiter_mode, "unknown")

        use_case = b1 & NXP_CONFIG_1_USE_CASE_CONF_TRISTATE # mask includes all use case bits
        use_case_map = {
            NXP_CONFIG_1_USE_CASE_CONF_I2C_SLAVE: "i2c_slave",
            NXP_CONFIG_1_USE_CASE_CONF_I2C_MASTER: "i2c_master",
            NXP_CONFIG_1_USE_CASE_CONF_GPIO_PWM: "gpio_pwm",
            NXP_CONFIG_1_USE_CASE_CONF_TRISTATE: "tristate",
        }
        res["use_case"] = use_case_map.get(use_case, "unknown")
        res["eh_arbiter_mode_enabled"] = bool(b1 & NXP_CONFIG_1_EH_ARBITER_MODE_EN)

        # Byte 2
        res["gpio0_slew_rate"] = "fast" if (b2 & NXP_CONFIG_2_GPIO0_SLEW_RATE) else "normal"
        res["gpio1_slew_rate"] = "fast" if (b2 & NXP_CONFIG_2_GPIO1_SLEW_RATE) else "normal"
        res["lock_block_command_supported"] = bool(b2 & NXP_CONFIG_2_LOCK_BLOCK_COMMAND_SUPPORTED)
        res["extended_commands_supported"] = bool(b2 & NXP_CONFIG_2_EXTENDED_COMMANDS_SUPPORTED)

        gpio0_pad = b2 & NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN_PULLDOWN # full mask for GPIO0 pad
        gpio0_pad_map = {
            NXP_CONFIG_2_GPIO0_PAD_IN_DISABLED: "disabled",
            NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN_PULLUP: "plain_pullup",
            NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN: "plain",
            NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN_PULLDOWN: "plain_pulldown",
        }
        res["gpio0_pad_in"] = gpio0_pad_map.get(gpio0_pad, "unknown")

        gpio1_pad = b2 & NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN_PULLDOWN # full mask for GPIO1 pad
        gpio1_pad_map = {
            NXP_CONFIG_2_GPIO1_PAD_IN_DISABLED: "disabled",
            NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN_PULLUP: "plain_pullup",
            NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN: "plain",
            NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN_PULLDOWN: "plain_pulldown",
        }
        res["gpio1_pad_in"] = gpio1_pad_map.get(gpio1_pad, "unknown")

        return res

    def get_eh_ed_config_info(self):
        config = self.read_config_block(NXP_CONFIG_ADDR_EH_CONFIG)

        res = {}

        i_sel_lookup = {
            NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4: "0.4",
            NXP_EH_CONFIG_EH_VOUT_I_SEL_0_6: "0.6",
            NXP_EH_CONFIG_EH_VOUT_I_SEL_1_4: "1.4",
            NXP_EH_CONFIG_EH_VOUT_I_SEL_2_7: "2.7",
            NXP_EH_CONFIG_EH_VOUT_I_SEL_4_0: "4.0",
            NXP_EH_CONFIG_EH_VOUT_I_SEL_6_5: "6.5",
            NXP_EH_CONFIG_EH_VOUT_I_SEL_9_0: "9.0",
            NXP_EH_CONFIG_EH_VOUT_I_SEL_12_5: "12.5"
        }

        res["eh_vout_i_sel"] = i_sel_lookup.get(config[0] & NXP_EH_CONFIG_EH_VOUT_I_SEL_12_5, "unknown") # Full mask for EH_VOUT_I_SEL
        res["disable_power_check"] = bool(config[0] & NXP_EH_CONFIG_DISABLE_POWER_CHECK)
        
        v_sel_lookup = {
            NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8: "1.8",
            NXP_EH_CONFIG_EH_VOUT_V_SEL_2_4: "2.4",
            NXP_EH_CONFIG_EH_VOUT_V_SEL_3_0: "3.0",
            NXP_EH_CONFIG_EH_VOUT_V_SEL_RFU: "RFU"
        }
        
        res["eh_vout_v_sel"] = v_sel_lookup.get(config[0] & NXP_EH_CONFIG_EH_VOUT_V_SEL_RFU, "unknown") # Full mask for EH_VOUT_V_SEL
        res["eh_enable"] = bool(config[0] & NXP_EH_CONFIG_EH_ENABLE)

        ed_config_lookup = {
            NXP_ED_CONFIG_DISABLE: "disable",
            NXP_ED_CONFIG_NFC_FIELD_DETECT: "nfc_field_detect",
            NXP_ED_CONFIG_PWM: "pwm",
            NXP_ED_CONFIG_I2C_TO_NFC_PASS_THROUGH: "i2c_to_nfc_pass_through",
            NXP_ED_CONFIG_NFC_TO_I2C_PASS_THROUGH: "nfc_to_i2c_pass_through",
            NXP_ED_CONFIG_ARBITER_LOCK: "arbiter_lock",
            NXP_ED_CONFIG_NDEF_MSG_TLV_LENGTH: "ndef_msg_tlv_length",
            NXP_ED_CONFIG_STANDBY_MODE: "standby_mode",
            NXP_ED_CONFIG_WRITE_CMD_INDICATION: "write_cmd_indication",
            NXP_ED_CONFIG_READ_CMD_INDICATION: "read_cmd_indication",
            NXP_ED_CONFIG_START_OF_COMMAND_INDICATION: "start_of_command_indication",
            NXP_ED_CONFIG_READ_FROM_SYNCH_BLOCK: "read_from_synch_block",
            NXP_ED_CONFIG_WRITE_TO_SYNCH_BLOCK: "write_to_synch_block",
            NXP_ED_CONFIG_SOFTWARE_INTERRUPT: "software_interrupt",
            NXP_ED_CONFIG_RFU1: "rfu1",
            NXP_ED_CONFIG_RFU2: "rfu2"
        }

        res["ed_config"] = ed_config_lookup.get(config[2] & NXP_ED_CONFIG_RFU2, "unknown") # Full mask for ED_CONFIG

        return res

    def write_config_block(self, address, block_data):
        if(len(block_data) != 4):
            raise Exception("Block data must be four bytes")
        self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, NXP_CMD_WRITE_CONFIG, NXP_CMD_MANUF_CODE_NXP, 
                address]) + block_data)

    def write_config0(self, auto_standby_mode_en = False, lock_session_reg = False,
            eh_mode = NXP_CONFIG_0_EH_MODE_LOW_FIELD_STRENGTH, sram_copy_en = False):
        # Read the existing config page
        config = list(self.read_config_block(NXP_CONFIG_ADDR_CONFIG))
        # Construct new CONFIG_0 and update page
        config[0] = (
            (NXP_CONFIG_0_AUTO_STANDBY_MODE_EN if auto_standby_mode_en else 0x00) |
            (NXP_CONFIG_0_LOCK_SESSION_REG if lock_session_reg else 0x00) |
            eh_mode |
            (NXP_CONFIG_0_SRAM_COPY_EN if sram_copy_en else 0x00)
        )
        self.write_config_block(NXP_CONFIG_ADDR_CONFIG, bytes(config))

    def write_config1(self, transfer_dir_inverse = False, sram_enable = False, 
            arbiter_mode = NXP_CONFIG_1_ARBITER_MODE_NORMAL, use_case = NXP_CONFIG_1_USE_CASE_CONF_I2C_SLAVE, 
            arbiter_mode_en = False):
        # Read the existing config page
        config = list(self.read_config_block(NXP_CONFIG_ADDR_CONFIG))
        # Construct new CONFIG_1 and update page
        config[1] = (
            (NXP_CONFIG_1_PT_TRANSFER_DIR if transfer_dir_inverse else 0x00) |
            (NXP_CONFIG_1_SRAM_ENABLE if sram_enable else 0x00) |
            arbiter_mode |
            use_case |
            (NXP_CONFIG_1_EH_ARBITER_MODE_EN if arbiter_mode_en else 0x00)
        )
        self.write_config_block(NXP_CONFIG_ADDR_CONFIG, bytes(config))

    def write_config2(self, gpio0_slew_rate_fast=True, gpio1_slew_rate_fast=True,
            lock_block_supported=True, extended_commands_supported=True,
            gpio0_in=NXP_CONFIG_2_GPIO0_PAD_IN_PLAIN_PULLDOWN, gpio1_in=NXP_CONFIG_2_GPIO1_PAD_IN_PLAIN_PULLDOWN):
        # Read the existing config block
        config = list(self.read_config_block(NXP_CONFIG_ADDR_CONFIG))
        # Construct new CONFIG_2 byte
        config[2] = (
            (NXP_CONFIG_2_GPIO0_SLEW_RATE if gpio0_slew_rate_fast else 0x00) |
            (NXP_CONFIG_2_GPIO1_SLEW_RATE if gpio1_slew_rate_fast else 0x00) |
            (NXP_CONFIG_2_LOCK_BLOCK_COMMAND_SUPPORTED if lock_block_supported else 0x00) |
            (NXP_CONFIG_2_EXTENDED_COMMANDS_SUPPORTED if extended_commands_supported else 0x00) |
            gpio0_pad_in |
            gpio1_pad_in
        )
        self.write_config_block(NXP_CONFIG_ADDR_CONFIG, bytes(config))

    def write_eh_ed_config(self, enable = False, disable_power_check = False, 
            current = NXP_EH_CONFIG_EH_VOUT_I_SEL_0_4, voltage = NXP_EH_CONFIG_EH_VOUT_V_SEL_1_8,
            ed_config = NXP_ED_CONFIG_DISABLE):
        # Construct EH_CONFIG
        eh_config = (NXP_EH_ENABLE if enable else 0x00) | \
            (NXP_EH_CONFIG_DISABLE_POWER_CHECK if disable_power_check else 0x00) | \
            voltage | current
        self.write_config_block(NXP_CONFIG_ADDR_EH_CONFIG, bytes([eh_config, 0x00, ed_config, 0x00]))

    def read_sram(self, address = 0x00, num_blocks = 1):
        # The base command always reads one block more than specified
        if(num_blocks < 1):
            raise Exception("Must read at least one block")
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, NXP_CMD_READ_SRAM, NXP_CMD_MANUF_CODE_NXP, 
                address, num_blocks - 1]))
        return data

    def read_i2c(self, slave_address, num_bytes, stop_condition = True):
        # The base command always reads one block more than specified
        if(num_bytes < 1):
            raise Exception("Must read at least one byte")
        param = (slave_address & 0x7F) | (0x00 if stop_condition else 0x80)
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, NXP_CMD_READ_I2C, NXP_CMD_MANUF_CODE_NXP, 
                param, num_bytes - 1]))
        return data

    def write_i2c(self, slave_address, data, stop_condition = True):
        # The base command always writes one byte more than specified
        if(len(data) < 1):
            raise Exception("Must write at least one byte")
        param = (slave_address & 0x7F) | (0x00 if stop_condition else 0x80)
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, NXP_CMD_WRITE_I2C, NXP_CMD_MANUF_CODE_NXP, 
                param, len(data) - 1]) + data)
        return data

    def check_i2c_write_result(self):
        status = self.read_config_block(NXP_CONFIG_ADDR_I2C_M_STATUS_REG)
        status = status[0]
        if(status & NXP_I2C_M_WDT_EXPIRED_MASK != 0x00):
            raise Exception("WDT expired in last transaction")
        trans_status = status & NXP_I2C_M_TRANS_STATUS_MASK
        if(trans_status == NXP_I2C_M_TRANS_STATUS_RESET):
            raise Exception("Transaction status has been reset")
        if(trans_status == NXP_I2C_M_TRANS_STATUS_ADDRESS_NAK):
            raise Exception("Address was not acknowledged")
        elif(trans_status == NXP_I2C_M_TRANS_STATUS_DATA_NAK):
            raise Exception("Data was not acknowledged")
        elif(trans_status == NXP_I2C_M_TRANS_STATUS_SUCCESS):
            return True
        return False
    
    def check_i2c_busy(self):
        status = self.read_config_block(NXP_CONFIG_ADDR_I2C_M_STATUS_REG)
        status = status[0]
        return (status & NXP_I2C_M_BUSY_MASK != 0x00)

    def eh_control(self, trigger = True, enable = True):
        flags = 0x00
        if(trigger):
            flags |= NXP_EH_TRIGGER
        if(enable):
            flags |= NXP_EH_ENABLE
        self.write_config_block(NXP_CONFIG_ADDR_EH_CONFIG_REG, bytes([
            flags, 0x00, 0x00, 0x00
        ]))

    def check_eh_load_ok(self):
        status = self.read_config_block(NXP_CONFIG_ADDR_EH_CONFIG_REG)
        status = status[0]
        return (status & NXP_EH_LOAD_OK == NXP_EH_LOAD_OK)
