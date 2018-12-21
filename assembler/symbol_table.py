# -*- coding: utf-8 -*- 

"""
SymbolTable class to keep correspondence between symbolic labels and numeric addresses. 
A new instance is needed for each file translation.
"""


class SymbolTable:
    """
    Creates and maintains correspondence between symbols and their meaning (RAM and ROM addresses).
    """
    
    def __init__(self):
        """
        Initializes symbol table with all predefined symbols - symbols, labels and variables - 
        and their pre-allocated RAM addresses.  
        """
        
        self._table = {
            'SP': 0, 
            'LCL': 1, 
            'ARG': 2, 
            'THIS': 3, 
            'THAT': 4, 
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SCREEN': 16384,
            'KBD': 24576
        }
        
    def add_entry(self, symbol, address):
        """
        Adds pair (symbol, address) to table. 
        Symbol is a string. Address is an integer. No return.
        """
        
        self._table[symbol] = address
        
    def contains(self, symbol):
        """
        Does the symbol table contain the given symbol?
        Symbol is a string. Returns Boolean.
        """
        
        return symbol in self._table
    
    def get_address(self, symbol):
        """
        Returns address associated with the symbol.
        Symbol is a string. Address in an integer.
        """
        
        return self._table[symbol]