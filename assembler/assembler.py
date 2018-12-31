# -*- coding: utf-8 -*- 

"""
Assembler reads a text file - such as filename.asm - containing an assembly program, 
and produces as output a text file - filename.hack - containing the translated machine code. 

The name of the input file is supplied as a command-line argument: prompt> python -m assembler filename.asm
To run all files in data/input/ directory: prompt> python -m assembler run_all
"""

import sys, os
from .parser import Parser
 
 
def main():
    if sys.argv[1] == 'run_all':
        for root, dirs, files in os.walk('data/input/'):
            for file in files:
                if file.endswith('.asm'):
                    fname = os.path.join(root, file)
                    Parser(fname, auto_run=True)
    
    else:
        fname = 'data/input/' + sys.argv[1]
        Parser(fname, auto_run=True)