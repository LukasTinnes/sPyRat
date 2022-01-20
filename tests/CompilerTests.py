from unittest import TestCase
from compiling.Compiler import Compiler
from pandas import DataFrame


class CompilerTests(TestCase):

    def test_txt(self):
        data = DataFrame({"start_byte": [0], "end_byte": [9], "size": [10], "file_type": "txt"})
        load_file = "files\\test.txt"
        save_file_path = "output\\"
        prefix = "test"
        Compiler.decompile(data, load_file, save_file_path, prefix)

        with open(save_file_path + prefix + "_0.txt") as file:
            export = file.read(10)
            self.assertEqual(export, "ABCDEFGHIJ")

    def test_bytes(self):
        data = DataFrame({"start_byte": [0], "end_byte": [9], "size": [10], "file_type": "bytes"})
        load_file = "files\\test_bytes"
        save_file_path = "output\\"
        prefix = "test"
        Compiler.decompile(data, load_file, save_file_path, prefix)

        with open(save_file_path + prefix + "_0.bytes","rb") as file:
            export = file.read(10)
            self.assertEqual(export, bytes(list(range(10))))
