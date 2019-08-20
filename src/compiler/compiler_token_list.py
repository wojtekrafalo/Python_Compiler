from enum import Enum

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'DECLARE',
    'IN',
    'END',
    'IF',
    'THEN',
    'ELSE',
    'ENDIF',
    'WHILE',
    'DO',
    'ENDWHILE',
    'ENDDO',
    'FOR',
    'FROM',
    'TO',
    'ENDFOR',
    'DOWNTO',
    'READ',
    'WRITE',
    'SEMICOLON',
    'COLON',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MODULO',
    'BRACKET_LEFT',
    'BRACKET_RIGHT',
    'EQUALS',
    'NOT',
    'LESS_THAN',
    'GREATER_THAN'
]


class TokensEnum(Enum):
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    DECLARE = "DECLARE"
    IN = "IN"
    END = "END"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    ENDIF = "ENDIF"
    WHILE = "WHILE"
    DO = "DO"
    ENDWHILE = "ENDWHILE"
    ENDDO = "ENDDO"
    FOR = "FOR"
    FROM = "FROM"
    TO = "TO"
    ENDFOR = "ENDFOR"
    DOWNTO = "DOWNTO"
    READ = "READ"
    WRITE = "WRITE"
    SEMICOLON = ";"
    COLON = ":"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    BRACKET_LEFT = "("
    BRACKET_RIGHT = ")"
    EQUALS = "="
    NOT = "!"
    LESS_THAN = "<"
    GREATER_THAN = ">"
