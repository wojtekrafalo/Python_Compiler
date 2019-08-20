from enum import Enum
from src.compiler.RegisterManager import parse_register_to_str


class RegisterParametersError(Exception):
    pass


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

    def __init__(self, command_type: RegisterCommandType, command_data_1="", command_data_2=""):
        if command_data_1 == "" and command_data_2 != "":
            raise RegisterParametersError("You typed arguments to register command in wrong order.")

        if command_type == RegisterCommandType.GET or command_type == RegisterCommandType.PUT or \
                command_type == RegisterCommandType.LOAD or command_type == RegisterCommandType.STORE or \
                command_type == RegisterCommandType.INC or command_type == RegisterCommandType.DEC or \
                command_type == RegisterCommandType.HALF or command_type == RegisterCommandType.COPY or \
                command_type == RegisterCommandType.ADD or command_type == RegisterCommandType.SUB or \
                command_type == RegisterCommandType.JZERO or command_type == RegisterCommandType.JODD:
            command_data_1 = parse_register_to_str(int(command_data_1))

        if command_type == RegisterCommandType.COPY or command_type == RegisterCommandType.ADD or \
                command_type == RegisterCommandType.SUB:
            command_data_2 = parse_register_to_str(int(command_data_2))

        if command_data_1 != "":
            command_data_1 = " " + str(command_data_1)
        if command_data_2 != "":
            command_data_2 = " " + str(command_data_2)
        self.value = str(command_type) + str(command_data_1) + str(command_data_2) + "\n"
