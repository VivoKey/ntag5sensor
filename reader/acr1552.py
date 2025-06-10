from ber_tlv.tlv import *

from . import pcscreader


# Wrapping APDU fields
CLA_PSEUDO =                                0xFF
INS_TRANS =                                 0xC2

# Function for transparent mode
TRANS_FUNC_MANAGE =                         0x00
TRANS_FUNC_EXCHANGE =                       0x01
TRANS_FUNC_SWITCH_PROTOCOL =                0x02

# Transparent session management commands
MANAGE_BEGIN_TRANSPARENT_SESSION =          bytes([0x81, 0x00])
MANAGE_END_TRANSPARENT_SESSION =            bytes([0x82, 0x00])

# Protocol switiching commands
SWITCH_PROTOCOL_ISO15693_L3 =               bytes([0x8F, 0x02, 0x02, 0x03])

# Wrapping response error code tag
TLV_TAG_ERROR =                             0xC0

# Wrapping command and response tags
TLV_TAG_CMD_DATA =                          0x95
TLV_TAG_CMD_TIMEOUT =                       0x5F46
TLV_TAG_CMD_FWTI =                          0xFF6E
TLV_TAG_RESP_STATUS =                       0x96
TLV_TAG_RESP_FRAMING =                      0x92
TLV_TAG_RESP_DATA =                         0x97

TLV_TAG_CMD_FWTI_PREFIX =                   bytes([0x03, 0x01])

# TLV response fields
TLV_TAG_RESP_STATUS_ERROR_CRC =             (1 << 0)
TLV_TAG_RESP_STATUS_ERROR_TRANSMISSION =    (1 << 1)
TLV_TAG_RESP_STATUS_ERROR_PARITY =          (1 << 2)
TLV_TAG_RESP_STATUS_ERROR_FRAMING =         (1 << 3)
TLV_TAG_RESP_STATUS_ERROR_RFU =             0xF0

TLV_TAG_RESP_FRAMING_FIELD_NBITS_MASK =     0x07

# PCSC error code
PCSC_SUCCESS =                              (0x90, 0x00)
PCSC_ERROR_UNAVAILABLE_INFORMATION =        (0x62, 0x82)
PCSC_ERROR_NO_INFORMATION =                 (0x63, 0x00)
PCSC_FAILURE_IN_OTHER_DATA_OBJECT =         (0x63, 0x01)
PCSC_UNSUPPORTED_DATA_OBJECT =              (0x6A, 0x81)
PCSC_UNEXPECTED_LENGTH =                    (0x67, 0x00)
PCSC_UNEXPECTED_VALUE =                     (0x6A, 0x80)
PCSC_EXECUTION_ERROR_IFD =                  (0x64, 0x00)
PCSC_EXECUTION_ERROR_ICC =                  (0x64, 0x01)
PCSC_DATA_OBJECT_FAILED =                   (0x6F, 0x00)

# ISO15693 flags
ISO_FLAG_ERROR =                            (1 << 0)

# ISO15693 error codes 
ISO_ERROR_UNSUPPORTED_CMD =                 0x01
ISO_ERROR_UNRECOGNIZED_CMD =                0x02
ISO_ERROR_UNSUPPORTED_OPTION =              0x03
ISO_ERROR_UNKNOWN =                         0x0F
ISO_ERROR_UNAVAILABLE_BLOCK =               0x10
ISO_ERROR_ALREADY_LOCKED_BLOCK =            0x11
ISO_ERROR_LOCKED_BLOCK =                    0x12
ISO_ERROR_UNSUCCESSFUL_PROGRAMMING =        0x13
ISO_ERROR_UNSUCCESSFUL_LOCKING =            0x14


class ACR1552(pcscreader.PCSCReader):
    def __init__(self):
        super().__init__()

    @classmethod
    def list_readers(cls):
        readers = super().list_readers()
        return [reader.name for reader in readers if reader.name.startswith("ACS ACR1552")]

    def connect(self, reader_name):
        super().connect(reader_name)
        # Begin transparent NFC session
        self._transmit_pseudo(TRANS_FUNC_MANAGE, MANAGE_BEGIN_TRANSPARENT_SESSION)
        # Switch reader into ISO15693 layer 3 mode
        self._transmit_pseudo(TRANS_FUNC_SWITCH_PROTOCOL, SWITCH_PROTOCOL_ISO15693_L3)

    @staticmethod
    def cli_create_connect(args):
        readers = ACR1552.list_readers()
        readers.sort(key=str)
        if(args.listreaders):
            if(len(readers) == 0):
                print("warning: No ACR1552 readers found")
                exit(0)
            print("info: Available ACR1552 readers (" + str(len(readers)) + "):")
            for i, reader in enumerate(readers):
                print(str(i) + ": " + str(reader))
            exit(0)
        if(args.reader < 0 or args.reader >= len(readers)):
            print("error: Reader index is out of range")
            exit(1)
        reader = ACR1552()
        print(f"info: Waiting for card ... ", end="", flush=True)
        reader.connect(readers[args.reader])
        print(f"found card with ATR: {reader.atr.hex()}")
        return reader

    def disconnect(self):
        # End transparent NFC session
        self._transmit_pseudo(TRANS_FUNC_MANAGE, MANAGE_END_TRANSPARENT_SESSION)

    def _check_pseudo_error(self, error):
        # Check the inner response of the pseudo APDU
        bad_data, sw1, sw2 = error
        code = (sw1, sw2)
        if bad_data == 0x00 and code == PCSC_SUCCESS:
            return
        messages = {
            PCSC_ERROR_UNAVAILABLE_INFORMATION: "Data object XX warning, requested information not available",
            PCSC_ERROR_NO_INFORMATION: "No information",
            PCSC_FAILURE_IN_OTHER_DATA_OBJECT: "Execution stopped due to failure in other data object",
            PCSC_UNSUPPORTED_DATA_OBJECT: "Data object XX not supported",
            PCSC_UNEXPECTED_LENGTH: "Data object XX with unexpected length",
            PCSC_UNEXPECTED_VALUE: "Data object XX with unexpected value",
            PCSC_EXECUTION_ERROR_IFD: "Data object XX execution error (no response from IFD)",
            PCSC_EXECUTION_ERROR_ICC: "Data object XX execution error (no response from ICC)",
            PCSC_DATA_OBJECT_FAILED: "Data object XX failed, no precise diagnosis",
        }
        message = messages.get(code)
        if message:
            raise Exception(message.replace("XX", str(bad_data)))
        else:
            raise Exception(f"Unknown error: 0x{error.hex()}")

    def _transmit_pseudo(self, function, data):
        # Send command data TLV as pseudo PCSC APDU
        res = self.transmit_pcsc(bytes([CLA_PSEUDO, INS_TRANS, 
            0x00, function, 
            len(data)]) + data + bytes([ 0x00 ]))
        # Parse PCSC response as TLV
        tlv = dict(Tlv.parse(res))
        error = tlv[TLV_TAG_ERROR]
        self._check_pseudo_error(error)
        return tlv

    def _check_transmit_error(self, status):
        # Check the response status field
        if(status & TLV_TAG_RESP_STATUS_ERROR_CRC):
           raise Exception("CRC check failed")
        if(status & TLV_TAG_RESP_STATUS_ERROR_TRANSMISSION):
            raise Exception("Collision detected")
        if(status & TLV_TAG_RESP_STATUS_ERROR_PARITY):
            raise Exception("Parity error detected")
        if(status & TLV_TAG_RESP_STATUS_ERROR_FRAMING):
            raise Exception("Framing error detected")
        if(status & TLV_TAG_RESP_STATUS_ERROR_RFU):
            raise Exception(f"RFU error detected {status:02x}")

    def _check_transmit_framing(self, framing):
        # Check number of valid bits in response, encoded in bits [2:0]
        # Zero means all are valid
        if((framing & TLV_TAG_RESP_FRAMING_FIELD_NBITS_MASK) != 0x00):
            raise Exception(f"Invalid bits in response, framing {framing:02x}")

    def _check_iso15693_error(self, data):
        if(not (data[0] & ISO_FLAG_ERROR)):
            return
        error_map = {
            ISO_ERROR_UNSUPPORTED_CMD: "The command is not supported (request code not recognized).",
            ISO_ERROR_UNRECOGNIZED_CMD: "The command is not recognized (format error or similar).",
            ISO_ERROR_UNSUPPORTED_OPTION: "The option is not supported.",
            ISO_ERROR_UNKNOWN: "Unknown error.",
            ISO_ERROR_UNAVAILABLE_BLOCK: "The specified block is not available (doesn't exist).",
            ISO_ERROR_ALREADY_LOCKED_BLOCK: "The specified block is already locked and cannot be locked again.",
            ISO_ERROR_LOCKED_BLOCK: "The specified block is locked and its content cannot be changed.",
            ISO_ERROR_UNSUCCESSFUL_PROGRAMMING: "The specified block was not successfully programmed.",
            ISO_ERROR_UNSUCCESSFUL_LOCKING: "The specified block was not successfully locked.",
        }
        if 0xA0 <= data[1] <= 0xDF:
            raise Exception(f"Custom command error code {data[1]:02x}.")
        elif code in error_map:
            raise Exception(error_map[code])
        else:
            raise Exception(f"Reserved for future use (RFU) code {data[1]:02x}")

    def transmit_iso15693(self, data):
        # Transmit data in transparent NFC session with 1 second timeout
        # FWTI: 0 ~ 15, FWT/Timeout = 302.07 x 2FWTI us
        tlv = self._transmit_pseudo(TRANS_FUNC_EXCHANGE, Tlv.build([
            (TLV_TAG_CMD_TIMEOUT, (1000000).to_bytes(4, "big")), 
            (TLV_TAG_CMD_FWTI, TLV_TAG_CMD_FWTI_PREFIX + bytes([ 15 ])),
            (TLV_TAG_CMD_DATA, bytes(data))]))
        # Byte 0 is response status code, byte 1 is RFU
        self._check_transmit_error(tlv[TLV_TAG_RESP_STATUS][0])
        self._check_transmit_framing(tlv[TLV_TAG_RESP_FRAMING][0])
        data = tlv[TLV_TAG_RESP_DATA]
        # Check for inner protocol errors
        self._check_iso15693_error(data)
        # Strip flags
        return data[1:]
