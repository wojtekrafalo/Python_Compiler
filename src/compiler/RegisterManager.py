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
    # is_free: bool
    # operation_type: OperationType
    # name_int: int
    # name_str: str
    # value: int

    # TODO: Add to constructor type of the operation.
    def __init__(self, name: int, operation_type: OperationType = None):
        self.name_int = name
        self.name_str = parse_register_to_str(name)
        self.value = 0
        self.free()
        self.is_free = True
        self.operation_type = operation_type

    def free(self) -> None:
        self.is_free = True
        self.operation_type = OperationType.IS_FREE


class NotEnoughRegistersError(Exception):
    message = "Not enough registers."


class RegisterManager:
    registers: [Register] = []
    main_reg_name = "A"

    def __init__(self, number_of_registers: int = 8):
        for i in range(number_of_registers):
            self.registers.append(Register(i))

    def get_free_registers(self, how_many: int = 1) -> [Register]:
        free_registers: [Register] = []
        number: int = 0
        for reg in self.registers:
            if reg.is_free and not reg.name_str == self.main_reg_name:
                free_registers.append(reg)
                number += 1
                if how_many == number:
                    for reg_f in free_registers:
                        reg_f.is_free = False
                    if how_many == 1:
                        return free_registers[0]
                    else:
                        return free_registers
        raise NotEnoughRegistersError()

    # TODO: I think if I can add some [registered_registers] field at RegisterManager class and in this method delete this registers.
    def release_registers(self, *regs: [Register]) -> None:
        for r in regs:
            r.free()

    # TODO: some validation if A register is released or not.
    def get_reg_a(self) -> Register:
        for r in self.registers:
            if r.name_str == self.main_reg_name:
                return r
        raise NotARegisterError


class NotARegisterError(Exception):
    # message = "Register \'A\' is required."
    message = "Register \'" + RegisterManager.main_reg_name + "\' is required."


# TODO: Probably unnecessary
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


# TODO: Probably unnecessary
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
