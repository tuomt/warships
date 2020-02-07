class Packet():
    ENCODING = "utf-8"
    # Packet types
    T_READY = 0
    T_SETTINGS = 1

    def __init__(self, packet_type, msg):
        self.type = packet_type
        self.__msg = ''
        self.__data = 'INIT'
        self.msg = msg

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, value):
        self.__msg = value
        self.data = value

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = self.type.to_bytes(2, byteorder='big', signed=False)
        self.__data += bytes(value, self.ENCODING)
        
    def from_bytes(data):
        packet_type = int.from_bytes(data[:2], byteorder='big', signed = False)
        return Packet(packet_type, data[2:].decode(Packet.ENCODING))
