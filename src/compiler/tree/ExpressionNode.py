from enum import Enum

from src.compiler.RegisterManager import register_manager, Register
from src.compiler.tree.RegisterCommand import RegisterCommand, RegisterCommandType
from src.compiler.tree.ValueNode import ValueNode


class ExpressionType(Enum):
    NONE = "(NONE)"
    ADDITION = "(+)"
    SUBTRACTION = "(-)"
    MULTIPLICATION = "(*)"
    DIVISION = "(/)"
    MODULATION = "(%)"

    def __str__(self):
        return self.value


class ExpressionNode:

    def __init__(self, exp_type: ExpressionType, value_1: ValueNode, value_2: ValueNode = None):
        self.exp_type = exp_type
        self.value_1 = value_1
        self.value_2 = value_2

    def __str__(self):
        if self.value_2:
            return "Exp: [ " + str(self.exp_type) + ": " + str(self.value_1) + ", " + str(self.value_2) + " ]"
        else:
            return "Exp: [ " + str(self.exp_type) + ": " + str(self.value_1) + " ]"


# TODO: To the constructor of ExpressionNode will be passed ValueNode objects. I have to use these functions in constructor with unpacked registers from ValueNode objects.
def addition_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    register_manager.release_registers(reg_2)
    return [RegisterCommand(RegisterCommandType.ADD, reg_1, reg_2)]


def subtraction_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    register_manager.release_registers(reg_2)
    return [RegisterCommand(RegisterCommandType.SUB, reg_1, reg_2)]


def multiplication_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    result: [RegisterCommand] = []
    regs = register_manager.get_free_registers(3)
    reg_3 = regs[0]
    reg_4 = regs[1]
    reg_5 = regs[2]
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_4, reg_4))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 32))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_2, 31))

    result.append(RegisterCommand(RegisterCommandType.SUB, reg_3, reg_3))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_3))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_5, reg_2))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_2))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_2, reg_3))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_2, 7))

    result.append(RegisterCommand(RegisterCommandType.DEC, reg_2))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_2, 7))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_2, reg_5))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_1, reg_1))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_3, reg_3))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -9))

    result.append(RegisterCommand(RegisterCommandType.HALF, reg_3))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_1))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_2, reg_5))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_2, reg_3))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_4, reg_1))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_2, 13))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_5, reg_2))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_2))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_2, reg_3))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_2, 5))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_2, reg_5))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_2, reg_3))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_4, reg_1))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -8))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_2, reg_5))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_3))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_1))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -11))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_4))

    register_manager.release_registers(reg_2, reg_3, reg_4, reg_5)
    return result


def division_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    result: [RegisterCommand] = []
    regs = register_manager.get_free_registers(3)
    reg_3 = regs[0]
    reg_4 = regs[1]
    reg_5 = regs[2]

    result.append(RegisterCommand(RegisterCommandType.SUB, reg_4, reg_4))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 31))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_2, 30))

    result.append(RegisterCommand(RegisterCommandType.SUB, reg_3, reg_3))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_3))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_5, reg_1))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_1, reg_2))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 7))

    result.append(RegisterCommand(RegisterCommandType.DEC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 7))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_5))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_2, reg_2))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_3, reg_3))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -9))

    result.append(RegisterCommand(RegisterCommandType.HALF, reg_3))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_2))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_5))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_2, reg_2))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_4, reg_3))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_3, 12))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_5, reg_1))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_1, reg_2))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 4))

    result.append(RegisterCommand(RegisterCommandType.DEC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_4, reg_3))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -7))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_5))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_3))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_2))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -10))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_4))

    register_manager.release_registers(reg_2, reg_3, reg_4, reg_5)
    return result


def modulation_commands(reg_1: Register, reg_2: Register) -> [RegisterCommand]:
    result: [RegisterCommand] = []
    regs = register_manager.get_free_registers(3)
    reg_3 = regs[0]
    reg_4 = regs[1]
    reg_5 = regs[2]

    result.append(RegisterCommand(RegisterCommandType.SUB, reg_4, reg_4))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 31))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_2, 30))

    result.append(RegisterCommand(RegisterCommandType.SUB, reg_3, reg_3))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_3))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_5, reg_1))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_1, reg_2))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_4, reg_5))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 7))

    result.append(RegisterCommand(RegisterCommandType.DEC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 20))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_5))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_2, reg_2))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_3, reg_3))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -9))

    result.append(RegisterCommand(RegisterCommandType.HALF, reg_3))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_2))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_5))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_3, 13))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_5, reg_1))
    result.append(RegisterCommand(RegisterCommandType.INC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.SUB, reg_1, reg_2))
    result.append(RegisterCommand(RegisterCommandType.JZERO, reg_1, 4))

    result.append(RegisterCommand(RegisterCommandType.DEC, reg_1))
    result.append(RegisterCommand(RegisterCommandType.ADD, reg_4, reg_2))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -6))

    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_5))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_3))
    result.append(RegisterCommand(RegisterCommandType.HALF, reg_2))
    result.append(RegisterCommand(RegisterCommandType.JUMP, -11))

    result.append(RegisterCommand(RegisterCommandType.SUB, reg_4, reg_4))
    result.append(RegisterCommand(RegisterCommandType.COPY, reg_1, reg_4))

    register_manager.release_registers(reg_2, reg_3, reg_4, reg_5)
    return result
