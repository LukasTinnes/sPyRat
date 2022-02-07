class ByteArrayOperations:

    @staticmethod
    def bytearray_to_bit_list(bytes_obj: bytes) -> list:
        """
        Creates a list ob bits (1,0 integers) from bytes
        :param bytes_obj: The bytes to transform into a list
        :return:
        """
        bits = []
        for i in range(len(bytes_obj)):
            for j in range(8):
                bits.append((bytes_obj[i] >> j) % 2)
        return bits

    @staticmethod
    def bytes_crossings(bytes_obj: bytes) -> int:
        """
        Counts the number of 0,1 and 1,0 sequences.
        :param bytes_obj: The bytes to count the crossings in
        :return:
        """
        crossings = 0
        last = -1
        for x in ByteArrayOperations.bytearray_to_bit_list(bytes_obj):
            if last == -1:
                last = x
            else:
                if not x == last:
                    last = x
                    crossings += 1

        return crossings

    @staticmethod
    def are_bits_grouped(bytes_obj: bytes, bit: int) -> int:
        """
        Determibnes wther all values either 0,1, are next to each other.
        :return:
        """
        last = -1

        groups_0 = 0
        groups_1 = 0
        for x in ByteArrayOperations.bytearray_to_bit_list(bytes_obj):
            if not x == last:
                if x == 0:
                    groups_0 += 1
                else:
                    groups_1 += 1
            last = x

        if bit == 0:
            return groups_0 == 1
        else:
            return groups_1 == 1
