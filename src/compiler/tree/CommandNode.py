from enum import Enum

from src.compiler.tree.RegisterCommand import RegisterCommand


class CommandType(Enum):
    ASSIGNMENT = "ASSIGNMENT"
    IF = "IF"
    IF_ELSE = "IF_ELSE"
    WHILE = "WHILE"
    DO_WHILE = "DO_WHILE"
    FOR_TO = "FOR_TO"
    FOR_DOWNTO = "FOR_DOWNTO"
    READ = "READ"
    WRITE = "WRITE"
    NONE = "NONE"

    def __str__(self):
        return self.value


class CommandNode:
    commands: [RegisterCommand] = []

    def __init__(self, command_type: CommandType, command_data):
        self.command_type = command_type
        self.command_data = command_data

    def __str__(self):
        return "Comm: << " + str(self.command_type) + ", " + str(self.command_data) + " >>\n"


# TODO: building all commands based on specific objects.
def build_commands(commands: [CommandNode]):
    for comm in commands:
        print(str(comm))
