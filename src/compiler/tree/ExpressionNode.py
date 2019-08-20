from enum import Enum


class ExpressionType(Enum):
    NONE = 0
    ADDITION = 1
    SUBSTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    MODULATION = 5
    FOR_DOWNTO = 6
    READ = 7
    WRITE = 8


class ExpressionNode:

    def __init__(self, command_type: ExpressionType, expression_data):
        pass
