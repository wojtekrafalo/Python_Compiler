from enum import Enum
from src.compiler.RegisterManager import register_manager, Register
from src.compiler.tree.RegisterCommand import RegisterCommand, RegisterCommandType


class ValueType(Enum):
    NUMBER = "Num"
    IDENTIFIER = "ID"

    def __str__(self):
        return self.value


class ValueNode:

    def __init__(self, value_type: ValueType, value_data):
        self.value_type = value_type
        self.value_data = value_data

        if value_type == ValueType.NUMBER:
            # TODO: This is ok. I just have to move it from constructor somewhere else.
            # self.reg = register_manager.get_free_registers(1)
            # self.commands = make_number_commands(self.reg, value_data)
            self.init = True

    def __str__(self):
        if self.value_type == ValueType.IDENTIFIER:
            return "Val: ( " + str(self.value_data) + ")"
        else:
            return "Val: ( " + str(self.value_type) + ": " + str(self.value_data) + ")"


def make_number_commands(reg: Register, number: int, reg_help=None):
    if not reg_help:
        reg_help = register_manager.get_free_registers()
    effect: [RegisterCommand] = [RegisterCommand(RegisterCommandType.SUB, reg, reg),
                                 RegisterCommand(RegisterCommandType.SUB, reg_help, reg_help),
                                 RegisterCommand(RegisterCommandType.INC, reg_help)]
    res = 0
    iq = 1

    while 2 * iq < number:
        iq = 2 * iq
        effect.append(RegisterCommand(RegisterCommandType.ADD, reg_help, reg_help))

    while res != number:
        while res + iq > number:
            iq = iq / 2
            effect.append(RegisterCommand(RegisterCommandType.HALF, reg_help))
        res += iq
    effect.append(RegisterCommand(RegisterCommandType.ADD, reg, reg_help))
    register_manager.release_registers(reg_help)
    return effect
