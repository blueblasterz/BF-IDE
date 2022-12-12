"""
BF-IDE
https://github.com/blueblasterz
"""

import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import numpy as np

from BFMemory import BFMemory
from BFIO import BFInput, BFOutput

 
# number of cells in the memory (default is 30000)
MEM_SIZE = 30000

# datatype for each cells (default is 1 byte ie 0-255)
CELL_TYPE = np.uint8

# bf interpreter
class Interpreter:
    """
    The Interpreter loads and executes BF code
    It is NOT a Tkinter widget
    However:
    * if a BFMemory widget is given in the constructor, then it will be updated
    * if a BFInput widget is given, then instead of asking the user for input in command line,
      it will ask visually with the BFINPUT
    * if a BFOutput widget is given, then instead of printing the result to the terminal,
      it will print it in the BFInput
    """
    def __init__(self, mem_size: int = MEM_SIZE, cell_size: type = CELL_TYPE, w_mem: BFMemory = None, w_in: BFInput = None, w_out: BFOutput = None ) -> None :
        self.mem = np.zeros(mem_size, dtype=cell_size)
        self.mem_size = mem_size
        self.pc = 0
        self.cursor = 0
        self.input = []
        self.output = []
        self.code = [] # list of instructions = the brainfuck code
        self.jump_table = {} # jump table for the [ an ] instructions, pre computed when the bf code is loaded

        self.code_length = 0

    def set_input(self, input, ascii=True):
        """
        sets the input for the bf program
        ascii == True:
            input should be a string or a list of chars
            the values set in self.input will be ord(c) for c in input (ie ascii values)
        ascii == False:
            input should be a list of ints 
            the values set in self.input will be CELL_TYPE(i) for i in input (ie decimal values fitting in cell type)
            if the decimal value is too large for CELL_TYPE, it just overflows (ex: np.uint8(257) -> 1 )
        """
        if ascii:
            self.input = [ ord(c) for c in input ]
        else:
            self.input = [ CELL_TYPE(i) for i in input ]
    
    def request_input(self):
        """
        if self.input is empty and the program executes ','
        then directly ask the user for a single input
        if the user types several digits, input is interpretted as decimal
        else: ord(input[0]) is returned
        """
        a = input("Value : ")
        if a.isdecimal():
            return CELL_TYPE(int(a))
        return ord(a[0]) if len(a) != 0 else 0
    
    def get_next_input(self):
        if self.input:
            return self.input.pop(0)
        # return self.request_input()
        return 0

    def output_current(self):
        self.output.append( chr(self.mem[self.cursor]) )
    
    def load_code_from_path(self, path):
        with open(path,'r') as f:
            c = f.read(1)
            # instr_count = 0 
            char_count = 0
            depth = 0 # to verify the ONLY possible syntax error : mismatched []
            while c:
                if c in "+-><.,[]":
                    self.code += c
                    if c == '[':
                        depth += 1
                    elif c == ']':
                        depth -=1
                        if depth < 0:
                            print(f"Error while loading code '{path}' at {char_count}: unmatched ']'")
                    # instr_count += 1
                char_count += 1
                c = f.read(1)
            f.close()
        self.code_length = len(self.code)
        self.compute_jump_table()

    def compute_jump_table(self):
        self.jump_table = {}
        stack = []
        for i,c in enumerate(self.code):
            if c == '[':
                stack.append(i)
            elif c == ']':
                if stack:
                    corresp = stack.pop()
                    self.jump_table[i] = corresp
                    self.jump_table[corresp] = i
                else:
                    print(f"Error while generating jump table for current code: at instruction {i}: unmatched ']'")


    def optimize(self):
        """
        simple optimization to the bf code that is currently loaded
        optimization made are :
        * removing '><' and '<>'
        * removing '+-' and '-+'
        * TODO : replace sequences of only + - < > with special instructions 
                 in order to execute all of them in one operation (instead of doing 1 at a time)
        """
        i=0
        while i < len(self.code)-1:
            if (self.code[i] == '>' and self.code[i+1] == '<') \
            or (self.code[i] == '<' and self.code[i+1] == '>') \
            or (self.code[i] == '+' and self.code[i+1] == '-') \
            or (self.code[i] == '-' and self.code[i+1] == '+'):
                self.code[i:i+2] = []
                i -= 1
            i += 1
        self.code_length = len(self.code)
        self.compute_jump_table()

    def step(self, n=1):
        """
        executes n instructions from the code
        if end of code is reached, it stops
        """
        # print("coucou")
        for i in range(n):
            match self.code[self.pc]:
                case '+':
                    self.mem[self.cursor] += 1
                case '-':
                    self.mem[self.cursor] -= 1
                case '>':
                    self.cursor += 1
                    if self.cursor == self.mem_size:
                        self.cursor = 0
                case '<':
                    self.cursor -= 1
                    if self.cursor == -1:
                        self.cursor = self.mem_size-1
                case '.':
                    self.output_current()
                case ',':
                    self.mem[self.cursor] = self.get_next_input()
                case '[':
                    if self.mem[self.cursor] == 0:
                        self.pc = self.jump_table[self.pc]
                case ']':
                    if self.mem[self.cursor] != 0:
                        self.pc = self.jump_table[self.pc]
            self.pc += 1
            if self.pc >= self.code_length:
                return
    
    def step_until(self, target=-1):
        """
        executes code until program counter reaches target, then stops
        if target is -1, executes code until the end of the code
        """
        if target == -1: target = self.code_length
        while self.pc < target:
            self.step(1)

class IDE(tk.Frame):
    """
    the IDE widget contains :
    * a text zone for the current code to edit
    * a memory (+display) for the BF execution
        > when the BF code is executed (not debugged), the memory will only update at the end of the execution
        > when debugging, each step will update memory
    * an input text zone (with a checkbox for wether to consider ascii or decimal values)
    * an output text zone (with a checkbox for wether to show ascii or decimal values)
    * a menu bar with :
        * File
            * open file
            * save file
            * save file to ...
            * recent files ? requieres storage
        * options
            * memory size
            * cell size
    * toolbar with buttons for ;
        * run 
        * run to cursor (then debug)
        * debug
        * step
    """

    def __init__(self,root):
        super().__init__(root, width=500, height=500, relief=tk.RIDGE,borderwidth=1) 
        self.codeZone = scrolledtext.ScrolledText(self, width=80, height=30, font='TkFixedFont')
        self.codeZone.grid(column=0,row=0,padx=10,pady=10)

        self.mem = BFMemory(self, MEM_SIZE, CELL_TYPE)

        self.mem.grid(column=1,row=0,padx=10,pady=10)

        
class App:
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.title("BF-IDE")

        self.ide = IDE(self.tk)

        self.ide.pack(padx=10,pady=10)

        self.tk.bind_all("<KeyPress>", self.kbdevt)

        self.tk.mainloop()


    def kbdevt(self,e):
        k = e.keysym
        # print(f"from App : {k}")
        if k == "q" or k == "Escape":
            self.tk.destroy()

if __name__ == '__main__':

    # interpreter = Interpreter()
    # interpreter.load_code_from_path("./decimal_ascii_to_decimal_value.bf")
    # interpreter.load_code_from_path("./test.bf")

    # print(interpreter.code)
    # interpreter.optimize()
    # print(interpreter.code)

    # interpreter.set_input("125")

    # print("going to execute : ")
    # print("".join(interpreter.code))
    # print("with input : ", " ".join( [f"{e}('{chr(e)}')" for e in interpreter.input] ) )

    # interpreter.step_until()

    # print("done.\n")
    # print(f"memoire[0..10] : {interpreter.mem[0:10]}, cursor : {interpreter.cursor}")

    app = App()
