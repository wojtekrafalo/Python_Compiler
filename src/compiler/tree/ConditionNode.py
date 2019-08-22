from enum import Enum


class ConditionType(Enum):
    EQUALS = "="
    NOT_EQUALS = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUALS_THAN = ">="
    LESS_EQUALS_THAN = "<="

    def __str__(self):
        return self.value


class ConditionNode:

    def __init__(self, cond_type: ConditionType, value_1, value_2):
        self.cond_type = cond_type
        self.value_1 = value_1
        self.value_2 = value_2

    def __str__(self):
        return "Cond: [ " + str(self.cond_type) + ": " + str(self.value_1) + ", " + str(self.value_2) + " ]"
