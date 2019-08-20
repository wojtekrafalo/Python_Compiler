from enum import Enum

from src.compiler.tree.RegisterCommand import RegisterCommand


class CommandType(Enum):
    ASSIGNMENT = 0
    IF = 1
    IF_ELSE = 2
    WHILE = 3
    DO_WHILE = 4
    FOR_TO = 5
    FOR_DOWNTO = 6
    READ = 7
    WRITE = 8
    NONE = 9


class CommandNode:
    commands = [RegisterCommand]

    def __init__(self, command_type: CommandType, command_data):
        pass
