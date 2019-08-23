from enum import Enum

from src.compiler.RegisterManager import Register, register_manager
from src.compiler.tree.RegisterCommand import RegisterCommand, RegisterCommandType, concat_commands
from src.compiler.tree.ValueNode import ValueNode


class ConditionType(Enum):
    EQUALS = "="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUALS_THAN = ">="
    LESS_EQUALS_THAN = "<="

    def __str__(self):
        return self.value


class ConditionNode:

    def __init__(self, cond_type: ConditionType, value_1: ValueNode, value_2: ValueNode):
        self.cond_type = cond_type
        self.value_1 = value_1
        self.value_2 = value_2

    def __str__(self):
        return "Cond: [ " + str(self.cond_type) + ": " + str(self.value_1) + ", " + str(self.value_2) + " ]"


def negate_commands(reg_1: Register, reg_2: Register):
    res: [RegisterCommand] = [RegisterCommand(RegisterCommandType.SUB, reg_2, reg_2),
                              RegisterCommand(RegisterCommandType.INC, reg_2),
                              RegisterCommand(RegisterCommandType.SUB, reg_2, reg_1),
                              RegisterCommand(RegisterCommandType.COPY, reg_1, reg_2)]
    return res


def equals_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    reg_help = register_manager.get_free_registers()

    res: [RegisterCommand] = [RegisterCommand(RegisterCommandType.COPY, reg_help, reg_1),
                              RegisterCommand(RegisterCommandType.SUB, reg_help, reg_2),
                              RegisterCommand(RegisterCommandType.JZERO, reg_help, 2),
                              RegisterCommand(RegisterCommandType.JUMP, 4),
                              RegisterCommand(RegisterCommandType.COPY, reg_help, reg_2),
                              RegisterCommand(RegisterCommandType.SUB, reg_help, reg_1),
                              RegisterCommand(RegisterCommandType.JZERO, reg_help, 4),
                              RegisterCommand(RegisterCommandType.SUB, reg_1, reg_1),
                              RegisterCommand(RegisterCommandType.INC, reg_1),
                              RegisterCommand(RegisterCommandType.JUMP, 2),
                              RegisterCommand(RegisterCommandType.SUB, reg_1, reg_1)]

    # register_manager.release_registers(reg_2, reg_help)
    return res


def not_equals_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    res: [RegisterCommand] = equals_commands(reg_1, reg_2)
    res = concat_commands(res, negate_commands(reg_1, reg_2))
    return res


def smaller_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    res: [RegisterCommand] = greater_equals_commands(reg_1, reg_2)
    res = concat_commands(res, negate_commands(reg_1, reg_2))
    return res


def greater_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    res: [RegisterCommand] = smaller_equals_commands(reg_1, reg_2)
    res = concat_commands(res, negate_commands(reg_1, reg_2))
    return res


def smaller_equals_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    res: [RegisterCommand] = [RegisterCommand(RegisterCommandType.SUB, reg_1, reg_2),
                              RegisterCommand(RegisterCommandType.JZERO, reg_1, 3),
                              RegisterCommand(RegisterCommandType.SUB, reg_1, reg_1),
                              RegisterCommand(RegisterCommandType.INC, reg_1),
                              ]
    # register_manager.release_registers(reg_1, reg_2)
    return res


def greater_equals_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    res: [RegisterCommand] = [RegisterCommand(RegisterCommandType.SUB, reg_2, reg_1),
                              RegisterCommand(RegisterCommandType.JZERO, reg_2, 4),
                              RegisterCommand(RegisterCommandType.SUB, reg_1, reg_1),
                              RegisterCommand(RegisterCommandType.INC, reg_1),
                              RegisterCommand(RegisterCommandType.JUMP, 2),
                              RegisterCommand(RegisterCommandType.SUB, reg_1, reg_1),
                              ]
    # register_manager.release_registers(reg_1, reg_2)
    return res
