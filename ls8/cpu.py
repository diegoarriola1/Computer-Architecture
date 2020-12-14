"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.halted = False
        self.sp = self.reg[7]
        self.flags = [0, 0, 0, 0, 0, 'L', 'G', 'E']

    def ram_read(self, address):
        """
        Read what is in the RAM
        """
        return self.ram[address]

    def ram_write(self, value, address):
        """
        Write to RAM
        """
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    if line[0].startswith('0') or line[0].startswith('1'):
                        num = line.split('#')[0]
                        num = num.strip()
                        self.ram[address] = int(num, 2)
                        address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} Not found")
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flags[7] = 1
            else:
                self.flags[7] = 0
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags[5] = 1
            else:
                self.flags[5] = 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flags[6] = 1
            else:
                self.flags[6] = 0
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print("TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == HLT:
                running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                # Decrement the SP
                self.sp -= 1
                # Get the value of the register
                value = self.reg[operand_a]
                # Store the value in memory at SP
                self.ram_write(self.sp, value)
                self.pc += 2
            elif IR == POP:
                # Reverse what we did in PUSH
                value = self.ram_read(self.sp)
                self.reg[operand_a] = value
                self.sp += 1
                self.pc += 2
            elif IR == CALL:
                # Store our return address
                return_address = self.pc + 2
                # Push to the stack
                self.sp -= 1
                self.ram[self.sp] = return_address
                # Set the PC to the subroutine address
                subroutine_address = self.reg[operand_a]
                self.pc = subroutine_address
            elif IR == RET:
                # Pop the return address off the stack
                return_address = self.ram[self.sp]
                self.sp += 1
                # Store the return address in the PC
                self.pc = return_address
            elif IR == CMP:
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3

            elif IR == JMP:
                self.pc = self.reg[operand_a]

            elif IR == JEQ:
                if self.flags[7] == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2

            elif IR == JNE:
                if self.flags[7] != 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            else:
                print('Error')
                sys.exit()
