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
    name_int: int
    name_str: str
    value: int

    def __init__(self, name: int):
        self.name_int = name
        self.name_str = parse_register_to_str(name)
        self.value = 0
        self.free()

    # TODO: add to the RegisterManager a set of registered registers and in this method delete this register.
    def free(self):
        self.is_free = True
        self.operation_type = OperationType.IS_FREE


class NotEnoughRegistersError(Exception):
    message = "Not enough registers."


class RegisterManager:
    free_registers: [Register] = []
    registers: [Register] = []

    def __init__(self, number_of_registers=8):
        for i in range(number_of_registers):
            self.registers.append(Register(i))

    def get_free_registers(self, how_many: int):
        free_registers = []
        number = 0
        for reg in self.registers:
            if reg.is_free:
                free_registers.append(reg)
                number += 1
                if how_many == number:
                    for regis in free_registers:
                        regis.is_free = False
                    if how_many == 1:
                        return free_registers[0]
                    else:
                        return free_registers
        raise NotEnoughRegistersError()


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


register_manager = RegisterManager()
