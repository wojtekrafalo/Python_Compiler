from enum import Enum


class IdentifierType(Enum):
    VARIABLE = 0
    ARRAY_VARIABLE = 1
    ARRAY_VALUE = 2


class IdentifierNode:

    def __init__(self, identifier_type: IdentifierType, identifier_data):
        pass

    def command_get(self, context):
        pass
