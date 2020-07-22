"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        #initialize 
        self.ram = [0] * 256        #256 bytes of memory
        self.reg = [0] * 8      # 8 registers to store data
        self.pc = 0     #program counter acts as a pointer
    
    def ram_read(self, MAR):    # (MAR) Memory Address Register holds memory address/position we're reading from 
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):      
        self.ram[MAR] = MDR # (MDR) Memory Data Register is the data getting written into the MAR. LS8-spec.md file

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split("#",1)[0]
                        line = int(line, 10)  # int() is base 10 by default
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)


        

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):        #arithmetic logic unit- responsible for math
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        pass

        running = True

        instructions ={
             0b10000010: 'LDI',
             0b01000111: 'PRN',
             0b00000001: 'HLT'
        }

        while running: 
            i = self.ram[self.pc]       #single instruction that pc is pointing to in the ram(memory). Pc is pointing to the current instruction

            if instructions[i] == 'LDI':
                #set up register
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                #save value to register
                self.reg[reg_num] = value

                self.pc +=3
            
            elif instructions[i] == 'PRN':
                #print the register
                reg_num = self.ram[self.pc +1]
                print(self.reg[reg_num])

                self.pc +=2
            
            elif instructions[i] == 'HLT':
                #halt 
                running = False
            
            elif instructions[i] == 'MUL':
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu('MUL', reg_a, reg_b)

                self.pc +=3

            else: 
                print(f"Unknown instruction {i}")



testCPU = CPU()
testCPU.load()
testCPU.run()