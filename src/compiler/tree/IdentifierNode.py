from enum import Enum


class IdentifierType(Enum):
    VARIABLE = "VAR"
    ARRAY_VARIABLE = "ARR_VAR"
    ARRAY_VALUE = "ARR_VAL"

    def __str__(self):
        return self.value


from src.compiler.RegisterManager import register_manager
from src.compiler.MemoryManager import memory_manager


class IdentifierNode:

    def __init__(self, identifier_type: IdentifierType, identifier_name, array_index=None):
        self.identifier_type = identifier_type
        self.identifier_name = identifier_name
        self.array_index = array_index

        # var_tuple = memory_manager.is_declared(identifier_type, identifier_name)
        if identifier_type == IdentifierType.VARIABLE:
            # self.commands = make_number_commands(identifier_data)
            pass
        elif identifier_type == IdentifierType.ARRAY_VALUE:
            pass
        elif identifier_type == IdentifierType.ARRAY_VARIABLE:
            pass

    def __str__(self):
        if self.array_index:
            return "ID: < " + str(self.identifier_type) + ": " + str(self.identifier_name) + "(" + str(self.array_index) + ") >"
        else:
            return "ID: < " + str(self.identifier_type) + ": " + str(self.identifier_name) + " >"

# def make_number_commands(self, number: int):
#     set_0 = number
#     return None
