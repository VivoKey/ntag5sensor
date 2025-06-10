import smartcard
from smartcard.System import readers
from smartcard.CardRequest import CardRequest
from smartcard.CardType import AnyCardType
from smartcard.CardConnection import CardConnection


class PCSCReader():
    def __init__(self):
        super().__init__()
        self.card = None
        self.atr = None

    @classmethod
    def list_readers(cls):
        return readers()

    def connect(self, reader_name):
        request = CardRequest(timeout=None, newcardonly=False, readers=[reader_name], cardType=AnyCardType())
        self.card = request.waitforcard()
        self.card.connection.connect()
        self.atr = bytes(self.card.connection.getATR())

    def disconnect(self):
        self.card.connection.disconnect()
        self.card = None
        self.atr = None

    def transmit_pcsc(self, data):
        if(not self.card):
            raise Exception("Not connected to a card")
        res, sw1, sw2 = self.card.connection.transmit(list(data))
        if(sw1 != 0x90 or sw2 != 0x00):
            raise Exception(f"Unexpected PC/SC response code 0x{sw1:02x}{sw2:02x}")
        return bytes(res)
