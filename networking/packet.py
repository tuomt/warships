import struct

class Packet():
    # How many items are in the header
    HEADER_LEN = 2
    # How many bytes are in the header
    HEADER_BYTES = 4 * HEADER_LEN
    # Header indices in unpacked data
    I_LEN  = 0
    I_TYPE = 1
    # Packet types
    T_CLOSE            = 0
    T_READY            = 1
    T_SHIP_POSITIONS   = 2
    T_STRIKE           = 3
    T_STRIKE_RESULT    = 4

    def __init__(self, data, packet_type=None):
        # For incoming packets the type is initally unknown
        # but when creating a new packet, a packet_type should be provided
        # If packet_type is not provided the data is assumed to be in bytes format
        self.__data = None
        self.type = None

        if packet_type == None:
            unpacked_data = self.unpack_data(data)
            self.type = unpacked_data[self.I_TYPE]
            self.__data = unpacked_data
        else:
            self.type = packet_type
            self.set_data(data)

    def get_data(self, include_header=True):
        if include_header:
            return self.__data
        else:
            return self.__data[self.HEADER_LEN:]

    def set_data(self, data):
        """
        Set the data for the packet.
        A header will be put in front of the data.

        :param list data: the data to be set
        :return: nothing
        :rtype: None
        """
        header = [None] * self.HEADER_LEN
        header[self.I_LEN] = self.HEADER_LEN + len(data)
        header[self.I_TYPE] = self.type
        full_data = header
        full_data.extend(data)
        self.__data = full_data

    def pack_data(self):
        """
        Convert the data into bytes.
        
        :return: the packed data
        :rtype: bytes
        """

        #length = self.HEADER_LEN + len(self.get_data()
        #full_data = [length, self.type]
        #full_data.extend(self.get_data())
        length = len(self.__data)
        packed_data = struct.pack(">{}i".format(length), *self.__data)
        return packed_data

    def unpack_data(self, data):
        """
        Convert the data into a tuple of integers.
        
        :param bytes data: the data to be unpacked
        :return: the unpacked data
        :rtype: tuple
        """
        # Read the size of the data from the header
        size = int.from_bytes(data[:4], byteorder='big')
        print("unpacking:", data)
        print("packet size", size)
        # Unpack
        unpacked = struct.unpack(">{}i".format(size), data)
        return unpacked

