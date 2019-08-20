from src.register_machine.register_parser import read_file
import random


def run_machine(file):
    commands = read_file(file)
    # print(commands)

    memory = []
    registers = [0, 0, 0, 0, 0, 0, 0, 0]
    comm_NO = 0
    time_of_processing = 0

    for i in range(8):
        registers[i] = random.randint(0, 100)

    command_tuple = commands[comm_NO]
    # print("HERE!!!")
    while command_tuple[0] != 'HALT':
        command_tuple = commands[comm_NO]

        if command_tuple[0] == "GET":
            print("? ", end='')
            registers[command_tuple[1]] = input()
            time_of_processing += 100
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "PUT":

            print("> " + str(registers[command_tuple[1]]) + ". shit: " + str(comm_NO))
            time_of_processing += 100
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "LOAD":
            registers[command_tuple[1]] = memory[registers[0]]
            time_of_processing += 50
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "STORE":
            mem_index = registers[0]
            if len(memory) <= mem_index:
                curr_index = len(memory)
                while curr_index <= mem_index:
                    memory.append(random.randint(0, 100000))
                    curr_index += 1
            else:
                memory[mem_index] = registers[command_tuple[1]]

            memory[mem_index] = registers[command_tuple[1]]
            time_of_processing += 50
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "COPY":
            registers[command_tuple[1]] = registers[command_tuple[2]]
            time_of_processing += 5
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "ADD":
            registers[command_tuple[1]] += registers[command_tuple[2]]
            time_of_processing += 5
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "SUB":
            if registers[command_tuple[1]] >= registers[command_tuple[2]]:
                registers[command_tuple[1]] -= registers[command_tuple[2]]
            else:
                registers[command_tuple[1]] = 0
            time_of_processing += 5
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "HALF":
            registers[command_tuple[1]] = int(registers[command_tuple[1]] / 2)
            time_of_processing += 1
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "INC":
            registers[command_tuple[1]] += 1
            time_of_processing += 1
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "DEC":
            registers[command_tuple[1]] += 1
            if registers[command_tuple[1]] > 0:
                registers[command_tuple[1]] -= 1
            time_of_processing += 1
            comm_NO = comm_NO + 1

        elif command_tuple[0] == "JUMP":
            comm_NO = command_tuple[1]
            time_of_processing += 1

        elif command_tuple[0] == "JZERO":
            if registers[command_tuple[1]] == 0:
                comm_NO = command_tuple[2]
            else:
                comm_NO += 1
            time_of_processing += 1

        elif command_tuple[0] == "JODD":
            if registers[command_tuple[1]] % 2 != 0:
                comm_NO = command_tuple[2]
            else:
                comm_NO += 1
            time_of_processing += 1
        if comm_NO < 0 or comm_NO >= len(commands):
            print("ERROR: An attempt to execute non-existing command no " + comm_NO + ".")
        # print(str(command_tuple[0]))
    # print("HERE!!!")
    print("Machine executing completed. Cost: " + str(time_of_processing) + ".")


run_machine('register_code.txt')
