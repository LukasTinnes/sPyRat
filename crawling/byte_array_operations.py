class ByteArrayOperations:

    @staticmethod
    def bytearray_to_bit_list(bytes_obj: bytearray):
        """
        Creates a list ob bits (1,0 integers) from bytes
        :param bytes_obj:
        :return:
        """
        bits = []
        for i in range(len(bytes_obj)):
            for j in range(8):
                bits.append((bytes_obj[i] >> j) % 2)
        return bits

    @staticmethod
    def bytes_crossings(bytes_obj: bytearray):
        """
        Counts the number of 0,1 and 1,0 sequences.
        :param bytes_obj:
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
