# -*- coding: utf-8 -*- 

"""
Assembler reads a text file - such as filename.asm - containing an assembly program, 
and produces as output a text file - filename.hack - containing the translated machine code. 

The name of the input file is supplied as a command-line argument: prompt> python -m assembler filename.asm
"""

import sys
from .parser import Parser
 
 
def main():
    fname = 'data/input/' + sys.argv[1]
    Parser(fname, auto_run=True)