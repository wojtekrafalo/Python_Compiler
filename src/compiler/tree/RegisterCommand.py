from enum import Enum
from src.compiler.RegisterManager import parse_register_to_str
from src.compiler.RegisterManager import register_manager


class RegisterParametersError(Exception):
    message = "You typed arguments to register command in wrong order."


class RegisterCommandType(Enum):
    GET = "GET"
    PUT = "PUT"
    LOAD = "LOAD"
    STORE = "STORE"
    INC = "INC"
    DEC = "DEC"
    HALF = "HALT"
    COPY = "COPY"
    ADD = "ADD"
    SUB = "SUB"
    JUMP = "JUMP"
    JZERO = "JZERO"
    JODD = "JODD"
    HALT = "HALT"

    def __str__(self):
        return str(self.value)


class RegisterCommand:
    value: str = ""
    command_type: RegisterCommandType
    command_arg_1: str
    command_arg_2: str

    def __init__(self, command_type: RegisterCommandType, command_arg_1=None, command_arg_2=None):
        # Valid types: (Register, Register)
        #              (Register, None)
        #              (Register, int)
        #              (Register, str)
        #              (int, None)
        #              (str, None)
        #              (None, None)
        # TODO: Signature of this constructor is clearly for multiple types. But probably this have to stay.

        if not command_arg_1 and command_arg_2:
            raise RegisterParametersError()

        if command_type == RegisterCommandType.GET or command_type == RegisterCommandType.PUT or \
                command_type == RegisterCommandType.LOAD or command_type == RegisterCommandType.STORE or \
                command_type == RegisterCommandType.INC or command_type == RegisterCommandType.DEC or \
                command_type == RegisterCommandType.HALF or command_type == RegisterCommandType.COPY or \
                command_type == RegisterCommandType.ADD or command_type == RegisterCommandType.SUB or \
                command_type == RegisterCommandType.JZERO or command_type == RegisterCommandType.JODD:
            command_arg_1 = command_arg_1.name_str
            # command_arg_1 = parse_register_to_str(int(command_arg_1))

        if command_type == RegisterCommandType.COPY or command_type == RegisterCommandType.ADD or \
                command_type == RegisterCommandType.SUB:
            command_arg_2 = command_arg_2.name_str
            # command_arg_2 = parse_register_to_str(command_arg_2)

        if command_arg_1:
            command_arg_1 = " " + str(command_arg_1)
        if command_arg_2:
            command_arg_2 = " " + str(command_arg_2)
        self.value = str(command_type) + str(command_arg_1) + str(command_arg_2) + "\n"
        self.command_arg_1 = str(command_arg_1)
        self.command_arg_2 = str(command_arg_2)

    def __str__(self):
        return self.value


def connect_all_commands(commands: [RegisterCommand]) -> ([RegisterCommand], str):
    index = 0
    output_str = ""

    while index < len(commands):
        command = commands[index]
        if command.command_type == RegisterCommandType.JUMP:
            commands[index].value = str(command.command_type) + " " + str(int(command.command_arg_1) + index) + "\n"
        elif command.command_type == RegisterCommandType.JODD or command.command_type == RegisterCommandType.JZERO:
            commands[index].value = str(command.command_type) + " " + command.command_arg_1 + str(int(command.command_arg_1) + index) + "\n"
        output_str += command.value
        index += 1
    return commands, output_str


def concat_commands(commands_1: [RegisterCommand], commands_2: [RegisterCommand]) -> [RegisterCommand]:
    for comm in commands_2:
        commands_1.append(comm)
    return commands_1
