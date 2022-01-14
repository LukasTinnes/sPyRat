from pandas import DataFrame


class Compiler:
    """
    Deals with  Writing to files using Information gained from crawling
    """

    def decompile(self, data: DataFrame, lod_file:str, save_file_path:str, prefix:str):
        """
        Saves data given in data frames as a new file each to the given file_path.
        :param data: The dataframe of the crawled files. Expects a format (start byte, end byte, size, confidence, file_type)
        :param file_path: The path to where the file should be saved.
        :param prefix: The prefix of the file to be saved.
        :return:
        """
        ...
