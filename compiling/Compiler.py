from pandas import DataFrame


class Compiler:
    """
    Deals with  Writing to files using Information gained from crawling
    """

    @staticmethod
    def decompile(data: DataFrame, load_file: str, save_file_path: str, prefix: str):
        """
        Saves data given in data frames as a new file each to the given file_path.
        :param data: The dataframe of the crawled files. Expects a format (start byte, end byte, size, confidence, file_type)
        :param save_file_path: The path to where the file should be saved.
        :param load_file: The file path for the file which contents should be decompiled
        :param prefix: The prefix of the file to be saved.
        :return:
        """
        with open(load_file, 'rb') as load_file:
            for index, row in data.iterrows():
                start_byte = row["start_byte"]
                size = row["size"]
                file_type = row["file_type"]
                load_file.seek(start_byte)
                bytes = load_file.read(size)
                with open(f"{save_file_path}\\{prefix}_{index}.{file_type}", "wb") as save_file:
                    save_file.write(bytes)

    @staticmethod
    def decompile_to_single_file(data: DataFrame, load_file: str, save_file_path: str, prefix: str, separation: bytearray=None):
        """
        Decompilrs a frame to a single file, using a seperation bytearray between each segment.
        :param data: The dataframe of the crawled files. Expects a format (start byte, end byte, size, confidence, file_type)
        :param save_file_path: The path to where the file should be saved.
        :param load_file: The file path for the file which contents should be decompiled
        :param prefix: The prefix of the file to be saved.
        :param separation: The separation bytearray that is pasted between each data point defined in data.
        :return:
        """
        if separation is None:
            separation = bytearray()
        else:
            separation = bytearray(separation)
        with open(load_file, 'rb') as load_file:
            with open(f"{save_file_path}\\{prefix}_all.dat", "wb") as save_file:
                for index, row in data.iterrows():
                    start_byte = row["start_byte"]
                    size = row["size"]
                    load_file.seek(start_byte)
                    data_bytes = load_file.read(size)
                    save_file.write(data_bytes)
                    save_file.write(separation)

    @staticmethod
    def decompile_to_data_frame(data: DataFrame, load_file: str):
        """
        Decompiles the data into a given data frame, as a new data column.
        :param data: The dataframe to load and save to
        :param load_file: The file to load the data from.
        :return:
        """
        all_vals = []
        with open(load_file, 'rb') as load_file:
            for index, row in data.iterrows():
                start_byte = row["start_byte"]
                size = row["size"]
                load_file.seek(start_byte)
                all_vals.append(load_file.read(size))

        data["data"] = all_vals
        return data

