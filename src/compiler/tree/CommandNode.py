from enum import Enum

from src.compiler.tree.RegisterCommand import RegisterCommand


class CommandType(Enum):
    IF = "IF"
    IF_ELSE = "IF_ELSE"
    ASSIGNMENT = "ASSIGNMENT"
    WHILE = "WHILE"
    DO_WHILE = "DO_WHILE"
    FOR_TO = "FOR_TO"
    FOR_DOWNTO = "FOR_DOWNTO"
    READ = "READ"
    WRITE = "WRITE"
    NONE = "NONE"

    def __str__(self):
        return self.value


def str_comms(comms):
    ret = ""
    for comm in comms:
        ret += str(comm)
    return ret


class CommandNode:
    commands: [RegisterCommand] = []

    def __init__(self, command_type: CommandType, command_data):
        self.command_type = command_type
        self.command_data = command_data

    def __str__(self):
        res = "\nComm: << " + str(self.command_type) + ": "
        if self.command_type == CommandType.IF:
            res += str(self.command_data[0]) + "; Then: " + str_comms(self.command_data[1])

        elif self.command_type == CommandType.IF_ELSE:
            res += str(self.command_data[0]) + "; Then: " + str_comms(self.command_data[1]) + "; Else: " + str_comms(self.command_data[2])

        elif self.command_type == CommandType.ASSIGNMENT:
            res += str(self.command_data[0]) + " := " + str(self.command_data[1])

        elif self.command_type == CommandType.WHILE:
            res += str(self.command_data[0]) + " DO " + str_comms(self.command_data[1]) + " EndWHILE"

        elif self.command_type == CommandType.DO_WHILE:
            res += str_comms(self.command_data[0]) + "While: " + str(self.command_data[1]) + " EndDO"

        elif self.command_type == CommandType.FOR_TO or self.command_type == CommandType.FOR_DOWNTO:
            res += str(self.command_data[0]) + " = {" + str(self.command_data[1]) + ":" + str(self.command_data[2]) + "} DO: " + str_comms(self.command_data[3]) + " EndFOR"

        elif self.command_type == CommandType.READ or self.command_type == CommandType.WRITE:
            res += str(self.command_data)
        else:
            return "SHIT"
        return res + " >>"
