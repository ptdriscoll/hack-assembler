# -*- coding: utf-8 -*- 

"""
Assember tests for .asm files WITH symbols.
To run tests in command line, i.e. for phase1 tests: prompt> python -m tests.phase2
To run a specific test, note addition of unittest: prompt> python -m unittest tests.phase2.Parser.test_init
"""

from .context import assembler 
from assembler import parser
from assembler import symbol_table
import unittest
import filecmp

class SymbolTable(unittest.TestCase):
    """
    Check SymbolTable
    """
    
    print('\nRUNNING SymbolTable')       

    def test_run(self):
        symbols = symbol_table.SymbolTable()
        self.assertTrue(symbols.contains('R0')) 
        self.assertEqual(symbols.get_address('R0'), 0)        

        self.assertEqual(symbols.get_address('R15'), 15)
        self.assertEqual(symbols.get_address('SCREEN'), 16384)        
       
        symbols.add_entry('label', 16)
        self.assertTrue(symbols.contains('label'))
        self.assertEqual(symbols.get_address('label'), 16)
        
class Max(unittest.TestCase):
    """
    Check Max.asm.
    """
    
    print('\nRUNNING Max.asm through Parser')       

    def setUp(self):
        self.parser = parser.Parser('./data/input/Max.asm') 
        self.parser.run_first_pass()
        
    def test_run(self):    
        for x in range(2):
            self.parser.has_more_commands() 
            self.parser.advance() 
        self.assertEqual(self.parser._symbols.get_address('R1'), 1)    
            
        for x in range(2):
            self.parser.has_more_commands() 
            self.parser.advance()    
        self.assertEqual(self.parser._symbols.get_address('OUTPUT_FIRST'), 10) 
        
        for x in range(4):
            self.parser.has_more_commands() 
            self.parser.advance()        
        #print(self.parser)        
        self.assertEqual(self.parser._symbols.get_address('OUTPUT_D'), 12)         
        
        for x in range(2):
            self.parser.has_more_commands() 
            self.parser.advance()        
        #print(self.parser)        
        self.assertEqual(self.parser._symbols.get_address('OUTPUT_FIRST'), 10)     

        for x in range(2):
            self.parser.has_more_commands() 
            self.parser.advance()        
        #print(self.parser)        
        self.assertEqual(self.parser._symbols.get_address('OUTPUT_D'), 12) 

        for x in range(2):
            self.parser.has_more_commands() 
            self.parser.advance()        
        #print(self.parser)        
        self.assertEqual(self.parser._symbols.get_address('INFINITE_LOOP'), 14) 

class Rect(unittest.TestCase):
    """
    Check Rect.asm.
    """
    
    print('\nRUNNING Rect.asm through Parser')       

    def setUp(self):
        self.parser = parser.Parser('./data/input/Rect.asm') 
        self.parser.run_first_pass()

    def test_run(self):    
        for x in range(5):
            self.parser.has_more_commands() 
            self.parser.advance() 
            self.parser.translate()
        #print(self.parser)   
        self.assertEqual(self.parser._symbols.get_address('counter'), 16)  
        
        for x in range(4):
            self.parser.has_more_commands() 
            self.parser.advance() 
            self.parser.translate()
        #print(self.parser)   
        self.assertEqual(self.parser._symbols.get_address('address'), 17)
        
class Compare(unittest.TestCase):
    """
    Compare outputs with correct versions
    """
    
    print('\nCOMPARING OUTPUTS')       

    def test_run(self): 
        self.assertTrue(filecmp.cmp('./data/output/Max.hack', './data/compare/Max.hack'))
        #self.assertTrue(filecmp.cmp('./data/output/Pong.hack', './data/compare/Pong.hack'))
        self.assertTrue(filecmp.cmp('./data/output/Rect.hack', './data/compare/Rect.hack')) 

class PongPring(unittest.TestCase):
    """
    Compare and print lines between Pong output and compare files
    """
    
    print('\nCOMPARING PONG OUTPUTS BY LINE')       

    with open('./data/output/Pong.hack') as f:
        pong_output = f.readlines()  

    with open('./data/compare/Pong.hack') as f:
        pong_compare = f.readlines() 
    
    count = 0
    for x in range(100, max(len(pong_output), len(pong_compare))):
        if count == 5:
            break 
        if pong_output[x] != pong_compare[x]:
            count += 1            
            print(x, '\n', pong_output[x], pong_compare[x])              

class Pong(unittest.TestCase):
    """
    Check Pong.asm.
    """
    
    print('\nRUNNING Pong.asm through Parser')  

    def setUp(self):
        self.parser = parser.Parser('./data/input/Pong.asm') 
        self.parser.run_first_pass()                 
        
    def test_run(self):
        self.assertTrue(self.parser._symbols.contains('RET_ADDRESS_CALL0')) 
        self.assertTrue(self.parser._symbols.contains('ball.move$if_end1')) 
        self.assertTrue(self.parser._symbols.contains('ball.move$if_end3')) 
        self.assertTrue(self.parser._symbols.contains('ball.move$if_end6')) 
        self.assertTrue(self.parser._symbols.contains('ball.bounce$if_end1'))
        
        #print('\nPRINTING SYMBOLS')
        #print(self.parser._symbols.get_address('RET_ADDRESS_CALL0')) 
        #print(self.parser._symbols.get_address('ball.move$if_end1')) 
        #print(self.parser._symbols.get_address('ball.move$if_end3')) 
        #print(self.parser._symbols.get_address('ball.move$if_end6')) 
        #print(self.parser._symbols.get_address('ball.bounce$if_end1'))       
        
        self.assertEqual(self.parser._symbols.get_address('RET_ADDRESS_CALL0'), 145) 
        self.assertEqual(self.parser._symbols.get_address('ball.move$if_end1'), 1401) 
        self.assertEqual(self.parser._symbols.get_address('ball.move$if_end3'), 1401) 
        self.assertEqual(self.parser._symbols.get_address('ball.move$if_end6'), 1551) 
        self.assertEqual(self.parser._symbols.get_address('ball.bounce$if_end1'), 2086)         


if __name__=='__main__':
    unittest.main()          