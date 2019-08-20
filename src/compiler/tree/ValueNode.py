from enum import Enum


class ValueType(Enum):
    NUMBER = 0
    IDENTIFIER = 1


class ValueNode:

    def __init__(self, value_type: ValueType, value_data):
        pass

    def command_get(self, context):
        pass
