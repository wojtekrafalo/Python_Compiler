from enum import Enum

from src.compiler.tree.RegisterCommand import RegisterCommand, RegisterCommandType, concat_commands
from src.compiler.tree.ValueNode import make_number_commands


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
        self.data = [identifier_name, array_index]

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
            return "Id: < " + str(self.identifier_type) + ": " + str(self.identifier_name) + "(" + str(self.array_index) + ") >"
        else:
            return "Id: < " + str(self.identifier_type) + ": " + str(self.identifier_name) + " >"

    # TODO: Definitely to be corrected. variables should be typed.
    def get_commands(self, setting: bool):
        arr_tup = memory_manager.is_declared(self.identifier_type, self.data)

        if self.identifier_type == IdentifierType.ARRAY_VALUE:
            memory_idx = arr_tup.mem_fst + self.array_index - arr_tup.idx_fst

            reg = register_manager.get_free_registers()
            if setting:
                result: [RegisterCommand] = make_number_commands(memory_idx, reg)
                register_manager.release_registers(reg)
                arr_tup.initialize(self.array_index)
                return result
            else:
                result: [RegisterCommand] = make_number_commands(memory_idx, reg)

                result.append(RegisterCommand(RegisterCommandType.COPY, register_manager.get_reg_a, reg))
                result.append(RegisterCommand(RegisterCommandType.LOAD, reg))
                register_manager.release_registers(reg)
                return result
        elif self.identifier_type == IdentifierType.ARRAY_VARIABLE:
            reg = register_manager.get_free_registers()
            reg_help = register_manager.get_free_registers()

            idx_fst = arr_tup.idx_fst
            mem_fst = arr_tup.mem_fst

            if setting:
                reg_number = register_manager.get_free_registers()

                result: [RegisterCommand] = RegisterCommand(RegisterCommandType.LOAD, reg, reg_help)
                result = concat_commands(result, make_number_commands(reg_number, mem_fst, reg_help))

                result.append(RegisterCommand(RegisterCommandType.ADD, reg, reg_number))
                result = concat_commands(result, make_number_commands(reg_number, idx_fst, reg_help))
                result.append(RegisterCommand(RegisterCommandType.SUB, reg, reg_number))

                register_manager.release_registers(reg_number, reg_help)
                return result
            else:
                reg_a = register_manager.get_reg_a()

                result: [RegisterCommand] = RegisterCommand(RegisterCommandType.LOAD, reg_a, reg_help)
                result = concat_commands(result, make_number_commands(reg, mem_fst, reg_help))

                result.append(RegisterCommand(RegisterCommandType.ADD, reg_a, reg))
                result = concat_commands(result, make_number_commands(reg, idx_fst, reg_help))

                result.append(RegisterCommand(RegisterCommandType.SUB, reg_a, reg))
                result.append(RegisterCommand(RegisterCommandType.LOAD, reg))
                return result
        elif self.identifier_type == IdentifierType.VARIABLE:
            reg = register_manager.get_free_registers()
            mem = arr_tup.memory_idx
            if setting:
                res = make_number_commands(reg, mem)
                register_manager.release_registers(reg)
                arr_tup.initialize()
                return res
            else:
                result = make_number_commands(reg, mem)
                result.append(RegisterCommandType.COPY, register_manager.get_reg_a(), reg)
                result.append(RegisterCommandType.LOAD, reg)
                return result
