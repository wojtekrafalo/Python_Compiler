from enum import Enum
from src.compiler.grammar_parser import register_manager
from src.compiler.tree.RegisterCommand import make_number_commands


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

    # TODO: I actually do not know, what I've meant here. Method is probably intended to delete
    def command_get(self, context):
        pass

    def __str__(self):
        return "Val: ( " + str(self.value_type) + ": " + str(self.value_data) + ")"
