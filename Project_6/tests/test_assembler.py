# test_assembler.py
import sys
import os
import unittest

# Add the src directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from assembler import symbol_table_manager, parser, decoder

initialSymbolTable = {
    'R0': '0', 
    'R1': '1', 
    'R2': '2', 
    'R3': '3', 
    'R4': '4', 
    'R5': '5', 
    'R6': '6', 
    'R7': '7', 
    'R8': '8', 
    'R9': '9', 
    'R10': '10', 
    'R11': '11', 
    'R12': '12', 
    'R13': '13', 
    'R14': '14', 
    'R15': '15', 
    'SCREEN': '16384', 
    'KBD': '24576', 
    'SP': '0', 
    'LCL': '1', 
    'ARG': '2', 
    'THIS': '3', 
    'THAT': '4'
}

class TestSymbolTableManager(unittest.TestCase):
    def test_symbol_table_manager(self):
        self.assertEqual(symbol_table_manager(initialize=True), initialSymbolTable)
        expectedST = initialSymbolTable.copy()
        expectedST['var1'] = 16
        self.assertEqual(symbol_table_manager(st=initialSymbolTable,k='var1',v=16),expectedST)
                         
class TestParser(unittest.TestCase):
    def test_initial_parse(self):
        self.assertEqual(parser(fn="test.asm",st={},i=0), "test.hack")

    def test_second_parse(self):
        self.assertEqual(parser(fn="test.asm.temp",st={},i=1), "test.hack")

class TestDecoder(unittest.TestCase):
    def test_decoder_a_instruction(self):
        self.assertEqual(decoder("@2", initialSymbolTable), '0000000000000010')

    def test_decoder_c_instruction(self):
        self.assertEqual(decoder("D=A", initialSymbolTable), '1110110000010000')
        self.assertEqual(decoder("0;JMP", initialSymbolTable), '1110101010000111')

if __name__ == "__main__":
    unittest.main()