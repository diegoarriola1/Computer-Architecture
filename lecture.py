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
PUSH = 7  # takes in reg and stores value in reg on top of stack
POP = 8  # takes in reg and stores topmost element in stack in reg


def load_memory():
    program = [
        PRINT_HI,
        SAVE,  # SAVE value 65 into reg 2
        65,
        2,
        SAVE,  # SAVE value 20 in reg 3
        20,
        3,
        PUSH,
        2,
        PUSH,
        3,
        POP,
        4,
        POP,
        0,
        HALT
    ]

    space_for_stack = 128 - len(program)
    memory = program + ([0] * space_for_stack)
    return memory


memory = load_memory()
program_counter = 0  # points to the current instruction
running = True
registers = [0] * 8
stack_pointer_register = 7  # reg num contains address of stack pointer
registers[stack_pointer_register] = len(memory) - 1

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
    elif command_to_execute == PUSH:
        registers[stack_pointer_register] -= 1
        register_to_get_value_in = memory[program_counter + 1]
        value_in_register = registers[register_to_get_value_in]
        memory[registers[stack_pointer_register]] = value_in_register
        program_counter += 2
    elif command_to_execute == POP:
        register_to_pop_value_in = memory[program_counter + 1]
        registers[register_to_pop_value_in] = memory[
                                                registers[
                                                    stack_pointer_register]]
        registers[stack_pointer_register] += 1
        program_counter += 2
    else:
        print(f"Unknown instuction {command_to_execute}")
        sys.exit(1)

print(f"registers: {registers}")
print(f"memory: {memory}")
