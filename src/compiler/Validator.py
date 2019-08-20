from enum import Enum


# TODO: Add line enumeration at code.
def validate_declarations(p):
    if p[1]:
        for var in p[1]:
            if p[2] == var[0]:
                # TODO: Add here number of line with error
                raise DeclarationError(DecError.DUPLICATED_NAME, [p[2], var[0]])

            if len(p) == 9:
                if p[4] > p[6]:
                    # TODO: Add here number of line with error
                    raise DeclarationError(DecError.ARRAY_NUMERATION, [p[2], p[4], p[6]])


class DeclarationError(Exception):
    message = "None message"

    def __init__(self, decl_error, data_tuple):
        if decl_error == DecError.ARRAY_NUMERATION:
            # TODO: Add number of line
            self.message = "Bad array enumeration. Beginning index cannot be greater than final index."
        elif decl_error == DecError.DUPLICATED_NAME:
            self.message = "Name of variable already reserved."


class DecError(Enum):
    DUPLICATED_NAME = 1,
    ARRAY_NUMERATION = 2
