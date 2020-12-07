"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = False
        self.ram = [00000000] * 256
        self.pc = 0
        self.reg = [0] * 8

        #Commands - these come from the list below
        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.LDI = 0b10000010
        self.MUL = 0b10100010
        self.NOP = 0b00000000
        pass

    def load(self, f):
        """Load a program into memory."""

        file_path = f
        program = open(f"{file_path}", "r")
        address = 0
        for line in program:
            if line[0] ==  "0" or line[0] == "1":
                command = line.split('#', 1)[0]
                self.ram[address] = int(command, 2)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[self.ram[reg_a]] *= self.reg[self.ram[reg_b]]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, MAR):    #MAR = Memory Address Register
        MDR = self.ram[MAR]     #MDR = Memory Data Register
        return MDR
        
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        self.running = True
        self.pc = 0
        self.trace()

        while self.running:
            ir = self.ram_read(self.pc)
            print("This is IR:", ir)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.LDI:
                reg = operand_a
                val = operand_b
                self.reg[reg] = val
                self.pc += 3
            
            elif ir == self.PRN:
                reg = self.ram[self.pc + 1]
                print(self.reg[reg])
                self.pc += 2
            
            elif ir == self.HLT:
                self.running = False 
                self.pc += 1

            elif ir == self.MUL:
                self.alu('MUL', self.pc+1, self.pc+2)
                self.pc += 3
            
            elif ir == self.NOP:
                self.pc += 1

            else:
                # self.pc += 1
                print("Wrong instruction or address: ", ir, self.pc)
                raise ValueError

        

    
