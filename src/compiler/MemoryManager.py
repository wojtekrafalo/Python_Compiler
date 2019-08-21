from enum import Enum


class Variable:
    def __init__(self, name: str, mem_idx: int):
        self.structure_type = DataStructure.VAR
        self.name = name
        self.memory_idx = mem_idx
        self.is_initialized = False
        self.used_register = None

    def is_held(self):
        if self.used_register:
            return self.used_register
        else:
            return False


class OutOfBoundError(Exception):
    message = "Index out of bound"
    pass


class VariableUndeclaredError(Exception):
    message = "Undeclared variable"
    pass


class Array:
    init = []
    used_registers = []

    def __init__(self, name: str, idx_fst: int, idx_snd: int, mem_fst: int):
        self.structure_type = DataStructure.ARR
        self.name = name
        self.idx_fst = idx_fst
        self.idx_snd = idx_snd
        self.mem_fst = mem_fst
        self.size = idx_snd - idx_fst + 1
        self.mem_snd = mem_fst + idx_snd - idx_fst

        for i in range(self.size):
            self.init.append(False)
            self.used_registers.append(False)

    def is_initialized(self, idx: int):
        if idx > self.idx_snd or idx < self.idx_fst:
            raise OutOfBoundError()
        else:
            return self.init[idx-self.idx_fst]

    def initialize(self, idx: int):
        if idx > self.idx_snd or idx < self.idx_fst:
            raise OutOfBoundError()
        else:
            self.init[idx - self.idx_fst] = True

    def is_held(self, idx: int):
        if self.used_registers[idx - self.idx_fst]:
            return self.used_registers[idx - self.idx_fst]
        else:
            return False

    def memory_idx(self, idx: int):
        if idx > self.idx_snd or idx < self.idx_fst:
            raise OutOfBoundError()
        else:
            return self.mem_fst + idx - self.idx_fst


class MemoryManager:
    next_free_cell: int
    arrays: [Array] = []
    variables: [Variable] = []

    def __init__(self):
        self.next_free_cell = 0

    def manage_declared(self, variable_list):
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

    def manage_for(self, variable_tuple):
        # TODO: declaring and managing memory for FOR(i... index.
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


class DataStructure(Enum):
    VAR = "var"
    ARR = "arr"

    def __str__(self):
        return self.value


def validate_declarations(variables_map):
    if variables_map[1]:
        for var in variables_map[1]:
            if variables_map[2] == var[0]:
                raise DeclarationError(DecError.DUPLICATED_NAME, [variables_map[2], var[0]])

            if len(variables_map) == 9:
                if variables_map[4] > variables_map[6]:
                    raise DeclarationError(DecError.ARRAY_NUMERATION, [variables_map[2], variables_map[4], variables_map[6]])


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
