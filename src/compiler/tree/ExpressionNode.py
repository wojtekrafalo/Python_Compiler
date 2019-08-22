from enum import Enum


class ExpressionType(Enum):
    NONE = "NONE"
    ADDITION = "+"
    SUBSTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
    MODULATION = "%"

    def __str__(self):
        return self.value


class ExpressionNode:

    def __init__(self, exp_type: ExpressionType, value_1, value_2=None):
        self.exp_type = exp_type
        self.value_1 = value_1
        self.value_2 = value_2

    def __str__(self):
        return "Exp: [ " + str(self.exp_type) + ": " + str(self.value_1) + ", " + str(self.value_2) + " ]"
