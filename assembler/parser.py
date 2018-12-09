# -*- coding: utf-8 -*- 

"""
Parser class to to break each assembly command into 
its underlying components (fields and symbols).
"""

from assembler import code
from assembler import symbol_table


class Parser:
    """
    Accepts file.asm, reads assembly language command, parses it and provides convenient access 
    to command's components (fields and symbols). In addition, removes all white space and comments.  
    
    With auto_run flag set to false, manually run class methods in loop such as open(file.hack, 'w').
    Or set auto_run flag to true to let object instantiation run and save file.hack to data/output/ folder.
    """    
    
    def __init__(self, fname, auto_run=False):
        self._parsing_file = fname        
        with open(fname) as f:
            self._content = [line.strip() for line in f.readlines()]
            
        self._current_command = 0 #index for opened content               
        self._next_command = 0        
        self._symbols = symbol_table.SymbolTable()
        self._variable_symbols = 16
        self._next_translated_command = 0 #next index for translated text
        self._translation = '' 

        #this runs if auto_run flag is set to True
        if auto_run:
            self.run()        
        
    def __str__(self):        
        to_print = '          File to parse: ' + self._parsing_file + '\n' 
        to_print += '             First line: ' + self._content[0] + '\n'
        to_print += '    Current line number: ' + str(self._current_command) + '\n'
        to_print += '           Current line: ' + self._content[self._current_command] + '\n'
        to_print += '      Next command line: ' + str(self._next_command) + '\n'
        to_print += '           Next command: ' + self._content[self._next_command] + '\n'
        to_print += 'Current translated line: '+ str(self._next_translated_command - 1) + '\n'
        return to_print        

    def has_more_commands(self, first_pass=True):
        """
        Checks to see if there are any more commands in input.
        Sets line index of next command, if there is one, and returns Boolean.        
        """
        
        #if current command has already run once, then increment by 1  
        start = 0
        if self._current_command:
            start = self._current_command + 1
        end = len(self._content)  
        
        labels_found = []
 
        for index in range(start, end):
            line = self._content[index]  

            if not len(line) or line.replace(' ','').startswith('//'):
                continue            
            
            elif line.startswith('('):
                if first_pass:
                    labels_found.append(line[1 : line.find(')')].strip())
                continue
                
            else:      
                if first_pass and labels_found:
                    for label in labels_found: 
                        self._symbols.add_entry(label, self._next_translated_command)                   
                self._next_command = index    
                return True            

        return False
        
    def advance(self):
        """
        Reads the next command from input and makes it the current command. 
        Should be called only if hasMoreCommands() is true. 
        Initially there is no current command.
        """    
        
        #advance commands for both content index and translated text index 
        self._current_command = self._next_command        
        self._next_translated_command += 1        
        return self._current_command    

    def command_type(self):
        """
        Returns type of current command:
        - A_COMMAND for @Xxx where Xxx is either a symbol or a decimal
        - C_COMMAND for dest=comp;jump
        - L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.
        """
        
        command = self._content[self._current_command]
        if command.startswith('@'):
            return 'A_COMMAND'
        elif command.startswith('('):
            return 'L_COMMAND'        
        else:
            return 'C_COMMAND'        

    def symbol(self):
        """
        Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). 
        Should be called only when command_type() is A_COMMAND or L_COMMAND.
        """         
        
        return self._content[self._current_command].split(' ')[0][1:]        

    def dest(self):
        """
        Returns the dest mnemonic in the current C-command (8 possibilities).
        Should be called only when command_type() is C_COMMAND.
        """    
        
        command = self._content[self._current_command]
        
        if '=' in command:
            return command.split('=')[0].replace(' ','') 
        else:
            return 'null'        
        
    def comp(self):
        """
        Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when command_type() is C_COMMAND.
        """    
        
        command = self._content[self._current_command]
        
        if '=' in command:
            command = command.split('=')[1]
            
        return command.split(';')[0].strip().split(' ')[0].replace(' ','')     
        
    def jump(self): 
        """
        Returns the jump mnemonic in the current C-command (8 possibilities).
        Should be called only when command_type() is C_COMMAND.
        """    
        
        command = self._content[self._current_command]
        
        if ';' in command:
            return command.split(';')[1].strip().split(' ')[0].replace(' ','') 
        else:
            return 'null'
            
    def translate(self):
        if self.command_type() == 'A_COMMAND':
            value = self.symbol()
            
            #number variables
            if value.isdigit():
                address = int(int(value)) 
            
            #symbol variables            
            elif self._symbols.contains(value):
                address = self._symbols.get_address(value)   
            
            #new symbol variables - start adding these at address 16            
            else:
                address = self._variable_symbols
                self._symbols.add_entry(value, self._variable_symbols)
                self._variable_symbols += 1
                
            binary = '0' + bin(((1 << 15) - 1) & address)[2:].zfill(15)
            
        else:
            binary = '111' + code.comp[self.comp()] + code.dest[self.dest()] + code.jump[self.jump()]       
        
        return binary
        
    def run_first_pass(self):
        while self.has_more_commands():
            self.advance()
            
        #reset command lines for opened content and translated text    
        self._current_command = 0                
        self._next_command = 0
        self._next_translated_command = 0        

    def run_second_pass(self):       
        translation_file = self._parsing_file.split('.')[0].replace('input','output') + '.hack'
        with open(translation_file, 'w') as f:
            while self.has_more_commands(first_pass=False):
                self.advance()
                f.write(self.translate() + '\n')   
                
        print('\n' + translation_file.split('/')[-1] + ' translation file saved to folder at data/output/')                
        
    def run(self):
        self.run_first_pass()
        self.run_second_pass()        