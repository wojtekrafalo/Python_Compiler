from enum import Enum


class OperationType(Enum):
    MEMORY_ADDRESS = 0
    STORING = 1
    ADDITION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    MODULATION = 5
    STORING_FOR_INDEX = 6
    ASSIGNMENT = 7
    IS_FREE = 8


class Register:
    is_free: bool
    operation_type: OperationType
    value: int

    def __init__(self, value: int = 0):
        self.value = value
        self.free()

    def free(self):
        self.is_free = True
        self.operation_type = OperationType.IS_FREE


class RegisterManager:
    free_registers: [Register]
    registers: [Register]

    def __init__(self, number_of_registers=8):
        for i in range(number_of_registers):
            self.registers.append(Register(i))

    def get_free_registers(self):
        free_registers = [Register]
        for reg in self.registers:
            if reg.is_free:
                free_registers.append(reg)
        return free_registers


def parse_register_to_str(reg: int) -> str:
    if reg == 0:
        return "A"
    if reg == 1:
        return "B"
    if reg == 2:
        return "C"
    if reg == 3:
        return "D"
    if reg == 4:
        return "E"
    if reg == 5:
        return "F"
    if reg == 6:
        return "G"
    if reg == 7:
        return "H"


def parse_register_to_int(reg: str) -> int:
    if reg == "A":
        return 0
    if reg == "B":
        return 1
    if reg == "C":
        return 2
    if reg == "D":
        return 3
    if reg == "E":
        return 4
    if reg == "F":
        return 5
    if reg == "G":
        return 6
    if reg == "H":
        return 7
