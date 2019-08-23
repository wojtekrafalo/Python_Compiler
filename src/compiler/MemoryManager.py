from enum import Enum

from src.compiler.RegisterManager import Register
from src.compiler.tree.CommandNode import CommandType
from src.compiler.tree.IdentifierNode import IdentifierType


class Variable:
    def __init__(self, name: str, mem_idx: int):
        self.name = name
        self.memory_idx = mem_idx
        self.is_initialized = False
        self.used_register = None

    def is_held(self) -> Register or False:
        if self.used_register:
            return self.used_register
        else:
            return False

    def initialize(self) -> None:
        self.is_initialized = True


class Array:
    init: [bool] = []
    used_registers: [Register or False] = []

    def __init__(self, name: str, idx_fst: int, idx_snd: int, mem_fst: int):
        self.name = name
        self.idx_fst = idx_fst
        self.idx_snd = idx_snd
        self.mem_fst = mem_fst
        self.size = idx_snd - idx_fst + 1
        self.mem_snd = mem_fst + idx_snd - idx_fst

        for i in range(self.size):
            self.init.append(False)
            self.used_registers.append(False)

    def is_initialized(self, idx: int) -> bool:
        if not self.is_in_bound(idx):
            raise OutOfBoundError()
        else:
            return self.init[idx-self.idx_fst]

    def initialize(self, idx: int) -> None:
        if not self.is_in_bound(idx):
            raise OutOfBoundError()
        else:
            self.init[idx - self.idx_fst] = True

    def is_held(self, idx: int) -> Register or False:
        return self.used_registers[idx - self.idx_fst]

    def memory_idx(self, idx: int) -> int:
        if not self.is_in_bound(idx):
            raise OutOfBoundError()
        else:
            return self.mem_fst + idx - self.idx_fst

    def is_in_bound(self, idx: int) -> bool:
        return self.idx_fst <= idx <= self.idx_snd


class MemoryManager:
    arrays: [Array] = []
    variables: [Variable] = []

    def __init__(self):
        self.next_free_cell = 0

    def manage_declared(self, variable_list: list) -> None:
        validate_declarations(variable_list)
        for var in variable_list:
            if len(var) == 1:
                self.variables.append(Variable(var[0], self.next_free_cell))
                self.next_free_cell += 1
            elif len(var) == 3:
                first_idx = var[1]
                second_idx = var[2]
                array = Array(var[0], first_idx, second_idx, self.next_free_cell)
                self.arrays.append(array)
                self.next_free_cell = array.mem_snd + 1

        # It is debugging
        # print(self)
    # TODO: The problem is that methods like this are called before declared variables. Calling methods before tokens in parser fit is required. It is quite difficult to go around
    def is_declared(self, identifier_type: IdentifierType, data):
        print("Check: " + data + "\n" + self.__str__())
        if identifier_type == IdentifierType.VARIABLE:
            for var in self.variables:
                if var.name == data:
                    return var
            for arr in self.arrays:
                if arr.name == data:
                    raise ArrayUsedAsVariableError()
            raise VariableUndeclaredError()
        elif identifier_type == IdentifierType.ARRAY_VALUE:
            for arr in self.arrays:
                if arr.name == data[0]:
                    if not arr.is_in_bound(data[1]):
                        raise OutOfBoundError()
                    else:
                        return arr
            for var in self.variables:
                if var.name == data[0]:
                    raise VariableUsedAsArrayError()
            raise ArrayUndeclaredError()
        elif identifier_type == IdentifierType.ARRAY_VARIABLE:
            for arr in self.arrays:
                if arr.name == data[0]:
                    return arr
            for var in self.variables:
                if var.name == data[0]:
                    raise VariableUsedAsArrayError()
            raise ArrayUndeclaredError()

    def is_initialized(self, identifier_type: IdentifierType, data):
        var_tup = self.is_declared(identifier_type, data)
        if identifier_type == IdentifierType.VARIABLE:
            return var_tup.is_initialized
        elif identifier_type == IdentifierType.ARRAY_VALUE:
            return var_tup.is_initialized(data[1])

    def initialize(self, identifier_type: IdentifierType, data):
        var_tup = self.is_declared(identifier_type, data)
        if identifier_type == IdentifierType.VARIABLE:
            return var_tup.is_initialized
        elif identifier_type == IdentifierType.ARRAY_VALUE:
            return var_tup.is_initialized(data[1])

    def manage_for_block(self, block_type: CommandType, variable_tuple):
        # TODO: declaring and managing memory for big blocks if there is not enough registers to hold loop iterator or block condition result.
        pass

    def __str__(self):
        sss = "Declared variables: << vars: ["
        for var in self.variables:
            sss += "(" + var.name + ", " + str(var.memory_idx) +\
                   ", " + str(var.is_initialized) + ", " + str(var.is_held()) + ") "

        sss += "];  arrs: {"
        for arr in self.arrays:
            sss += "(" + arr.name + ", " + str(arr.idx_fst) + ", " +\
                   str(arr.idx_snd) + ", " + str(arr.mem_fst) + ", " +\
                   str(arr.mem_snd) + ", " + str(arr.init) + ", " + str(arr.used_registers) + ") "
        return sss + "} >>  next_free_cell: " + str(self.next_free_cell)


def validate_declarations(variables_map):
    if variables_map[1]:
        for var in variables_map[1]:
            if variables_map[2] == var[0]:
                raise DeclarationError(DecError.DUPLICATED_NAME, [variables_map[2], var[0]])

            if len(variables_map) == 9:
                if variables_map[4] > variables_map[6]:
                    raise DeclarationError(DecError.ARRAY_NUMERATION, [variables_map[2], variables_map[4], variables_map[6]])


class VariableUsedAsArrayError(Exception):
    message = "Variable used as an array."


class ArrayUsedAsVariableError(Exception):
    message = "Index of array not specified."


class ArrayUndeclaredError(Exception):
    pass


class OutOfBoundError(Exception):
    message = "Index out of bound"
    pass


class VariableUndeclaredError(Exception):
    message = "Undeclared variable"
    pass


class DeclarationError(Exception):
    message = "None message"

    def __init__(self, decl_error, data_tuple):
        if decl_error == DecError.ARRAY_NUMERATION:
            self.message = "Bad array enumeration. Beginning index cannot be greater than final index."
        elif decl_error == DecError.DUPLICATED_NAME:
            self.message = "Name of variable already reserved."


class DecError(Enum):
    DUPLICATED_NAME = 1
    ARRAY_NUMERATION = 2


memory_manager = MemoryManager()
