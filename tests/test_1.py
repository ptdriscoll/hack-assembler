# -*- coding: utf-8 -*- 

"""
Assember tests for .asm files without symbols.
To run tests in command line, i.e. for test_1 tests: prompt> python -m tests.test_1
To run a specific test, note addition of unittest: prompt> python -m unittest tests.test_1.Add.test_init
To run all tests in the tests package: prompt> python -m unittest
"""

from .context import assembler 
from assembler import parser
from assembler import code 
import unittest
import filecmp

class Code(unittest.TestCase):
    """
    Check code module
    """
    
    print('\nRUNNING code module')       

    def test_run(self):
        for key,value in code.comp.items():
            self.assertEqual(len(value), 7)                    

class Add(unittest.TestCase):
    """
    Check Add.asm.
    """
    
    print('\nRUNNING Add.asm through Parser')
    
    def setUp(self):
        self.parser = parser.Parser('./data/input/Add.asm')
       
    def test_init(self):
        #print(self.parser)
        more_commands = self.parser.has_more_commands()
        #print(self.parser)
        self.assertTrue(more_commands)
        
    def test_run(self):
        self.parser.has_more_commands()
        current_command = self.parser.advance()
        #print(self.parser)      
        self.assertEqual(current_command, 7)
        self.assertEqual(self.parser.command_type(), 'A_COMMAND')
        self.assertEqual(self.parser.symbol(), '2') 
        self.assertEqual(self.parser.translate(), '0000000000000010')        
        
        self.parser.has_more_commands()
        current_command = self.parser.advance()
        #print(self.parser)
        self.assertEqual(current_command, 8)                
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')
        self.assertEqual(self.parser.dest(), 'D')
        self.assertEqual(self.parser.comp(), 'A')
        self.assertEqual(self.parser.jump(), 'null') 
        self.assertEqual(self.parser.translate(), '1110110000010000')         

        self.parser.has_more_commands()
        self.assertEqual(self.parser.advance(), 9)       
        self.assertEqual(self.parser.command_type(), 'A_COMMAND')         
        self.assertEqual(self.parser.symbol(), '3')
        self.assertEqual(self.parser.translate(), '0000000000000011') 
        
        self.parser.has_more_commands()                 
        self.assertEqual(self.parser.advance(), 10) 
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')  
        self.assertEqual(self.parser.dest(), 'D')  
        self.assertEqual(self.parser.comp(), 'D+A')        
        self.assertEqual(self.parser.jump(), 'null') 
        self.assertEqual(self.parser.translate(), '1110000010010000') 
        
        self.parser.has_more_commands() 
        self.assertEqual(self.parser.advance(), 11)
        self.assertEqual(self.parser.command_type(), 'A_COMMAND')          
        self.assertEqual(self.parser.symbol(), '0') 
        self.assertEqual(self.parser.translate(), '0000000000000000')         
         
        self.parser.has_more_commands() 
        self.assertEqual(self.parser.advance(), 12) 
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')        
        self.assertEqual(self.parser.dest(), 'M')
        self.assertEqual(self.parser.comp(), 'D')
        self.assertEqual(self.parser.jump(), 'null') 
        self.assertEqual(self.parser.translate(), '1110001100001000')
        
        self.parser.has_more_commands() 
        self.assertEqual(self.parser.advance(), 12) 
        #print(self.parser)


class MaxL(unittest.TestCase):
    """
    Check MaxL.asm.
    """
    
    print('\nRUNNING MaxL.asm through Parser')       

    def setUp(self):
        self.parser = parser.Parser('./data/input/MaxL.asm')    
    
    def test_run(self):
        #print(self.parser)
        
        for x in range(5):
            self.parser.has_more_commands() 
            self.parser.advance() 
       
        self.parser.has_more_commands() 
        self.assertEqual(self.parser.advance(), 12) 
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')  
        self.assertEqual(self.parser.dest(), 'null')  
        self.assertEqual(self.parser.comp(), 'D')        
        self.assertEqual(self.parser.jump(), 'JGT')     

class RectL(unittest.TestCase):
    """
    Check RectL.asm.
    """
    
    print('\nRUNNING RectL.asm through Parser')       

    def setUp(self):
        self.parser = parser.Parser('./data/input/RectL.asm')    
    
    def test_run(self):
        #print(self.parser)

        for x in range(20):
            self.parser.has_more_commands() 
            self.parser.advance() 
       
        self.parser.has_more_commands() 
        self.parser.advance()
        self.assertEqual(self.parser.advance(), 27) 
        self.assertEqual(self.parser.command_type(), 'C_COMMAND')  
        self.assertEqual(self.parser.dest(), 'MD')  
        self.assertEqual(self.parser.comp(), 'M-1')        
        self.assertEqual(self.parser.jump(), 'null')  
        self.assertEqual(self.parser.translate(), '1111110010011000')  

class Compare(unittest.TestCase):
    """
    Compare outputs with correct versions
    """
    
    print('\nCOMPARING OUTPUTS')       

    def test_run(self):
        self.assertTrue(filecmp.cmp('./data/output/Add.hack', './data/compare/Add.hack'))          
        self.assertTrue(filecmp.cmp('./data/output/MaxL.hack', './data/compare/MaxL.hack'))
        self.assertTrue(filecmp.cmp('./data/output/PongL.hack', './data/compare/PongL.hack'))
        self.assertTrue(filecmp.cmp('./data/output/RectL.hack', './data/compare/RectL.hack'))        

        
if __name__=='__main__':
    unittest.main()     











