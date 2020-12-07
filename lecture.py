# lecture.py

import sys

# a machine that simply executes an instruction

# op-code - represent instruction that is supposed to be executed
PRINT_HI = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4  # save value in given register
PRINT_REGISTER = 5
ADD = 6  # takes in 2 registers and adds both and stores in A

memory = [
    PRINT_HI,
    SAVE,  # SAVE value 65 into reg 2
    65,
    2,
    SAVE,  # SAVE value 20 in reg 3
    20,
    3,
    ADD,  # ADD values stored in 2, 3 and store in reg 2
    2,
    3,
    PRINT_REGISTER,  # PRINT_REGISTER print value stored in reg 2
    2,
    HALT
]

program_counter = 0  # points to the current instruction
running = True
registers = [0] * 8

# keep looping while not halted
while running:
    command_to_execute = memory[program_counter]

    if command_to_execute == PRINT_HI:
        print("hi")
        program_counter += 1
    elif command_to_execute == PRINT_NUM:
        number_to_print = memory[program_counter + 1]
        print(f"{number_to_print}")
        program_counter += 2
    elif command_to_execute == HALT:
        running = False
    elif command_to_execute == SAVE:
        value_to_save = memory[program_counter + 1]
        register_to_save_it_in = memory[program_counter + 2]
        registers[register_to_save_it_in] = value_to_save
        program_counter += 3
    elif command_to_execute == PRINT_REGISTER:
        register_to_print = memory[program_counter + 1]
        print(f"{registers[register_to_print]}")
        program_counter += 2
    elif command_to_execute == ADD:
        register_a = memory[program_counter + 1]
        register_b = memory[program_counter + 2]
        sum_of_registers = registers[register_a] + registers[register_b]
        registers[register_a] = sum_of_registers
        program_counter += 3
    else:
        print(f"Unknown instuction {command_to_execute}")
        sys.exit(1)
