# Command flags
ISO_FLAG_SUB_CARRIER =                      (1 << 0)
ISO_FLAG_DATA_RATE =                        (1 << 1)
ISO_FLAG_INVENTORY =                        (1 << 2)
ISO_FLAG_PROTOCOL_EXTENSION =               (1 << 3)

# Request flags when inventory flag is NOT set
ISO_FLAG_SELECT =                           (1 << 4)
ISO_FLAG_ADDRESS =                          (1 << 5)
ISO_FLAG_OPTION =                           (1 << 6)
ISO_FLAG_RFU =                              (1 << 7)

# Request flags when inventory flag is set. Bits 7 to 8 are the same as before.
ISO_FLAG_AFI =                              (1 << 4)
ISO_FLAG_NB_SLOTS =                         (1 << 5)

# Response flags
ISO_FLAG_ERROR =                            (1 << 0)

# Get system information flags
ISO_SYSTEM_INFO_FLAG_DSFID =                (1 << 0)
ISO_SYSTEM_INFO_FLAG_AFI =                  (1 << 1)
ISO_SYSTEM_INFO_FLAG_VICC_MEMORY_SIZE =     (1 << 2)
ISO_SYSTEM_INFO_FLAG_IC_REFERENCE =         (1 << 3)

# Get extended system information flags
ISO_EXTENDED_SYSTEM_INFO_MOI =              (1 << 4)
ISO_EXTENDED_SYSTEM_INFO_VICC_CMD_LIST =    (1 << 5)
ISO_EXTENDED_SYSTEM_INFO_CSI_INFO =         (1 << 6)
ISO_EXTENDED_SYSTEM_INFO_FLAG_LENGTH =      (1 << 7)

# Get system information response fields
ISO_SYSTEM_INFO_FIELD_BLOCKSIZE_MASK =      0x1F

# Extended System Info Command Constants
# Byte 1
ISO_EXTENDED_SYSTEM_INFO_CMD_READ_SINGLE_BLOCK =                            0x01
ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_SINGLE_BLOCK =                           0x02
ISO_EXTENDED_SYSTEM_INFO_CMD_LOCK_SINGLE_BLOCK =                            0x04
ISO_EXTENDED_SYSTEM_INFO_CMD_READ_MULTIPLE_BLOCKS =                         0x08
ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_MULTIPLE_BLOCKS =                        0x10
ISO_EXTENDED_SYSTEM_INFO_CMD_SELECT =                                       0x20
ISO_EXTENDED_SYSTEM_INFO_CMD_RESET_TO_READY =                               0x40
ISO_EXTENDED_SYSTEM_INFO_CMD_GET_MULTIPLE_BLOCK_SECURITY_STATUS =           0x80
# Byte 2
ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_AFI =                                    0x01
ISO_EXTENDED_SYSTEM_INFO_CMD_LOCK_AFI =                                     0x02
ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_DSFID =                                  0x04
ISO_EXTENDED_SYSTEM_INFO_CMD_LOCK_DSFID =                                   0x08
ISO_EXTENDED_SYSTEM_INFO_CMD_GET_SYSTEM_INFORMATION =                       0x10
ISO_EXTENDED_SYSTEM_INFO_CMD_CUSTOM_COMMANDS =                              0x20
ISO_EXTENDED_SYSTEM_INFO_CMD_FAST_READ_MULTIPLE_BLOCKS =                    0x40
# Byte 3
ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_READ_SINGLE_BLOCK =                   0x01
ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_WRITE_SINGLE_BLOCK =                  0x02
ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_LOCK_SINGLE_BLOCK =                   0x04
ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_READ_MULTIPLE_BLOCKS =                0x08
ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_WRITE_MULTIPLE_BLOCKS =               0x10
ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_GET_MULTIPLE_BLOCK_SECURITY_STATUS =  0x20
ISO_EXTENDED_SYSTEM_INFO_CMD_FAST_EXTENDED_READ_MULTIPLE_BLOCKS =           0x40
# Byte 4
ISO_EXTENDED_SYSTEM_INFO_CMD_READ_BUFFER =                                  0x01
ISO_EXTENDED_SYSTEM_INFO_CMD_SELECTED_SECURE_STATE =                        0x02
ISO_EXTENDED_SYSTEM_INFO_CMD_FINAL_RESPONSE_ALWAYS_INCLUDES_CRYPTO_RESULT = 0x04
ISO_EXTENDED_SYSTEM_INFO_CMD_AUTH_COMM_CRYPTO_FORMAT_SUPPORTED =            0x08
ISO_EXTENDED_SYSTEM_INFO_CMD_SECURE_COMM_CRYPTO_FORMAT_SUPPORTED =          0x10
ISO_EXTENDED_SYSTEM_INFO_CMD_KEY_UPDATE_SUPPORTED =                         0x20
ISO_EXTENDED_SYSTEM_INFO_CMD_CHALLENGE_SUPPORTED =                          0x40
ISO_EXTENDED_SYSTEM_INFO_CMD_FURTHER_BYTE_TRANSMISSION =                    0x80

# Crypto suite identifier classes
ISO_CSI_CLASS_29167 =                       0x00
ISO_CSI_CLASS_MANUFACTURER =                0xD0
ISO_CSI_CLASS_GS1 =                         0xE0

# Crypto suite 29167 identifiers
ISO_CSI_29167_10_AES_128 =                  0x00
ISO_CSI_29167_11_PRESENT_80 =               0x01
ISO_CSI_29167_12_ECC_DH =                   0x02
ISO_CSI_29167_13_GRAIN_128A =               0x03
ISO_CSI_29167_14_AES_OFB =                  0x04
ISO_CSI_29167_15_XOR =                      0x05
ISO_CSI_29167_16_ECDSA_ECDH =               0x06
ISO_CSI_29167_17_CRYPTO_GPS =               0x07
ISO_CSI_29167_18_HUMMINGBIRD2 =             0x08
ISO_CSI_29167_19_RAMON =                    0x09
ISO_CSI_29167_20_ALGEBRAIC_ERASER =         0x0A
ISO_CSI_29167_21_SIMON =                    0x0B
ISO_CSI_29167_22_SPECK =                    0x0C

# Block security status flags
ISO_FLAG_SECURITY_STATUS_LOCKED =           (1 << 0)

# Command codes
ISO_CMD_SYSTEM_INFO =                       0x2B
ISO_CMD_EXTENDED_SYSTEM_INFO =              0x3B
ISO_CMD_READ_SINGLE_BLOCK =                 0x20
ISO_CMD_READ_MULTIPLE_BLOCKS =              0x23
ISO_CMD_FAST_EXT_READ_MULTIPLE_BLOCKS =     0x3D


class ISO15693:
    def __init__(self, reader):
        self.reader = reader

    def get_system_info(self):
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, ISO_CMD_SYSTEM_INFO]))

        info_flags = data[0]
        # UID is field after info flags, in reverse byte order
        info = { "uid": data[1:9][::-1] }
        data_index = 9
        if(info_flags & ISO_SYSTEM_INFO_FLAG_DSFID):
            info["dsfid"] = data[data_index]
            data_index += 1
        if(info_flags & ISO_SYSTEM_INFO_FLAG_AFI):
            info["afi"] = {
                "family": (data[data_index] & 0xF0) >> 4,
                "sub_family": data[data_index] & 0x0F
            }
            data_index += 1
        if(info_flags & ISO_SYSTEM_INFO_FLAG_VICC_MEMORY_SIZE):
            # These fields store one less then the actual value
            info["numblocks"] = data[data_index] + 1
            data_index += 1
            # Blocksize is stored in low 5 bits, high bits are RFU
            info["blocksize"] = (data[data_index] & ISO_SYSTEM_INFO_FIELD_BLOCKSIZE_MASK) + 1
            data_index += 1
            info["memory"] = info["blocksize"] * info["numblocks"]
        if(info_flags & ISO_SYSTEM_INFO_FLAG_IC_REFERENCE):
            info["icref"] = data[data_index]
            data_index += 1
    
        return info

    def get_extended_system_info(self):
        # Request all possible info by setting all the flags, except the
        # "Get request System field Info length parameter" which is still 0 = one byte.
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, ISO_CMD_EXTENDED_SYSTEM_INFO, 0x7F])
        )

        info_flags = data[0]
        # Reject non-standard responses
        if(info_flags & ISO_EXTENDED_SYSTEM_INFO_FLAG_LENGTH):
            raise Exception("Extended response flags not supported")
        # UID is field after info flags, in reverse byte order
        info = { "uid": data[1:9][::-1] }
        data_index = 9
        if(info_flags & ISO_SYSTEM_INFO_FLAG_DSFID):
            info["dsfid"] = data[data_index]
            data_index += 1
        if(info_flags & ISO_SYSTEM_INFO_FLAG_AFI):
            info["afi"] = {
                "family": (data[data_index] & 0xF0) >> 4,
                "sub_family": data[data_index] & 0x0F
            }
            data_index += 1
        if(info_flags & ISO_SYSTEM_INFO_FLAG_VICC_MEMORY_SIZE):
            # These fields store one less then the actual value
            # In extended mode, number of blocks is two instead of one byte
            info["numblocks"] = int.from_bytes(data[data_index:data_index+2], byteorder="little") + 1
            data_index += 2
            # Blocksize is stored in low 5 bits, high bits are RFU
            info["blocksize"] = (data[data_index] & ISO_SYSTEM_INFO_FIELD_BLOCKSIZE_MASK) + 1
            data_index += 1
            info["memory"] = info["blocksize"] * info["numblocks"]
        if(info_flags & ISO_SYSTEM_INFO_FLAG_IC_REFERENCE):
            info["icref"] = data[data_index]
            data_index += 1
        if(info_flags & ISO_EXTENDED_SYSTEM_INFO_MOI):
            # MOI = 0 means one-byte addressing, MOI = 1 means two-byte addressing
            info["moi"] = data[data_index]
            data_index += 1
        if(info_flags & ISO_EXTENDED_SYSTEM_INFO_VICC_CMD_LIST):
            info["cmdlist"] = {
                "read_single_block": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_READ_SINGLE_BLOCK),
                "write_single_block": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_SINGLE_BLOCK),
                "lock_single_block": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_LOCK_SINGLE_BLOCK),
                "read_multiple_blocks": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_READ_MULTIPLE_BLOCKS),
                "write_multiple_blocks": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_MULTIPLE_BLOCKS),
                "select": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_SELECT),
                "reset_to_ready": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_RESET_TO_READY),
                "get_multiple_block_security_status": bool(data[data_index] & ISO_EXTENDED_SYSTEM_INFO_CMD_GET_MULTIPLE_BLOCK_SECURITY_STATUS),
                "write_afi": bool(data[data_index+1] & ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_AFI),
                "lock_afi": bool(data[data_index+1] & ISO_EXTENDED_SYSTEM_INFO_CMD_LOCK_AFI),
                "write_dsfid": bool(data[data_index+1] & ISO_EXTENDED_SYSTEM_INFO_CMD_WRITE_DSFID),
                "lock_dsfid": bool(data[data_index+1] & ISO_EXTENDED_SYSTEM_INFO_CMD_LOCK_DSFID),
                "get_system_information": bool(data[data_index+1] & ISO_EXTENDED_SYSTEM_INFO_CMD_GET_SYSTEM_INFORMATION),
                "custom_commands": bool(data[data_index+1] & ISO_EXTENDED_SYSTEM_INFO_CMD_CUSTOM_COMMANDS),
                "fast_read_multiple_blocks": bool(data[data_index+1] & ISO_EXTENDED_SYSTEM_INFO_CMD_FAST_READ_MULTIPLE_BLOCKS),
                "extended_read_single_block": bool(data[data_index+2] & ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_READ_SINGLE_BLOCK),
                "extended_write_single_block": bool(data[data_index+2] & ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_WRITE_SINGLE_BLOCK),
                "extended_lock_single_block": bool(data[data_index+2] & ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_LOCK_SINGLE_BLOCK),
                "extended_read_multiple_blocks": bool(data[data_index+2] & ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_READ_MULTIPLE_BLOCKS),
                "extended_write_multiple_blocks": bool(data[data_index+2] & ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_WRITE_MULTIPLE_BLOCKS),
                "extended_get_multiple_block_security_status": bool(data[data_index+2] & ISO_EXTENDED_SYSTEM_INFO_CMD_EXTENDED_GET_MULTIPLE_BLOCK_SECURITY_STATUS),
                "fast_extended_read_multiple_blocks": bool(data[data_index+2] & ISO_EXTENDED_SYSTEM_INFO_CMD_FAST_EXTENDED_READ_MULTIPLE_BLOCKS),
                "read_buffer": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_READ_BUFFER),
                "selected_secure_state": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_SELECTED_SECURE_STATE),
                "final_response_always_includes_crypto_result": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_FINAL_RESPONSE_ALWAYS_INCLUDES_CRYPTO_RESULT),
                "auth_comm_crypto_format_supported": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_AUTH_COMM_CRYPTO_FORMAT_SUPPORTED),
                "secure_comm_crypto_format_supported": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_SECURE_COMM_CRYPTO_FORMAT_SUPPORTED),
                "key_update_supported": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_KEY_UPDATE_SUPPORTED),
                "challenge_supported": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_CHALLENGE_SUPPORTED),
                "further_byte_transmission": bool(data[data_index+3] & ISO_EXTENDED_SYSTEM_INFO_CMD_FURTHER_BYTE_TRANSMISSION)
            }
            data_index += 4
        if(info_flags & ISO_EXTENDED_SYSTEM_INFO_CSI_INFO):
            csi_len = data[data_index]
            if(csi_len == 0):
                # It appears that if only one entry exists, no length is supplied, as it is assumed that
                # there is at least one entry in the list since the info flag is set. If there were zero entries,
                # the flag would not be set.
                csi_len = 1
            else:
                data_index += 1
            csi_list = []
            for i in range(csi_len):
                csi_raw = data[data_index + i]
                csi_class = "RFU"
                csi_value = hex(csi_raw)
                # Upper 2 or 4 bytes hold the CSI class
                if(csi_raw & 0xC0 == ISO_CSI_CLASS_29167):
                    csi_class = "ISO"
                    iso_csi_map = {
                        ISO_CSI_29167_10_AES_128: "29167-10 AES-128",
                        ISO_CSI_29167_11_PRESENT_80: "29167-11 PRESENT-80",
                        ISO_CSI_29167_12_ECC_DH: "29167-12 ECC-DH",
                        ISO_CSI_29167_13_GRAIN_128A: "29167-13 GRAIN-128A",
                        ISO_CSI_29167_14_AES_OFB: "29167-14 AES-OFB",
                        ISO_CSI_29167_15_XOR: "29167-15 XOR",
                        ISO_CSI_29167_16_ECDSA_ECDH: "29167-16 ECDSA-ECDH",
                        ISO_CSI_29167_17_CRYPTO_GPS: "29167-17 CRYPTO-GPS",
                        ISO_CSI_29167_18_HUMMINGBIRD2: "29167-18 HUMMINGBIRD2",
                        ISO_CSI_29167_19_RAMON: "29167-19 RAMON",
                        ISO_CSI_29167_20_ALGEBRAIC_ERASER: "29167-20 ALGEBRAIC-ERASER",
                        ISO_CSI_29167_21_SIMON: "29167-21 SIMON",
                        ISO_CSI_29167_22_SPECK: "29167-22 SPECK"
                    }
                    csi_value_key = csi_raw & 0x3F
                    csi_value = iso_csi_map.get(csi_value_key, f"29167-{(csi_value_key + 10)} UNKNOWN")
                elif(csi_raw & 0xF0 == ISO_CSI_CLASS_MANUFACTURER):
                    csi_class = "Tag manufacturer"
                    csi_value = hex(csi_raw & 0x0F)
                elif(csi_raw & 0xF0 == ISO_CSI_CLASS_GS1):
                    csi_class = "GS1 network"
                    csi_value = hex(csi_raw & 0x0F)
                csi_list.append({
                    "class": csi_class,
                    "id": csi_value
                })
            data_index += csi_len
            info["csi"] = csi_list

        return info

    def read_single_block(self, block_number):
        data = self.reader.transmit_iso15693(
            bytes([ISO_FLAG_DATA_RATE, ISO_CMD_READ_SINGLE_BLOCK, block_number]))
        locked = data[0] & ISO_FLAG_SECURITY_STATUS_LOCKED
        payload = data[1:]
        return data, locked

    def read_multiple_blocks(self, start_block, num_blocks):
        # The base command always reads one block more than specified
        if(num_blocks < 1):
            raise Exception("Must read at least one block")
        data = self.reader.transmit_iso15693(bytes([ISO_FLAG_DATA_RATE | ISO_FLAG_OPTION, 
            ISO_CMD_FAST_EXT_READ_MULTIPLE_BLOCKS]) + start_block.to_bytes(2, "big") +
            (num_blocks - 1).to_bytes(2, "big"))
        block_length = len(data) // num_blocks
        read_offset = 0
        blocks = []
        for i in range(num_blocks):
            locked = data[read_offset] & ISO_FLAG_SECURITY_STATUS_LOCKED
            blocks.append((data[read_offset + 1:read_offset + block_length], locked))
            read_offset += block_length
        return blocks
