from enum import Enum


class ConditionType(Enum):
    EQUALS = 0
    NOT_EQUALS = 1
    GREATER_THAN = 2
    LESS_THAN = 3
    GREATER_EQUALS_THAN = 4
    LESS_EQUALS_THAN = 5


class ConditionNode:

    def __init__(self, command_type: ConditionType, condition_data):
        pass
