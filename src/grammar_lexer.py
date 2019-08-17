import ply.lex as lex

tokens = [
    'IDENTIFIER',
    'NUMBER',
    'COMMENT',
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
    'GREATER_THAN',
    'END_LINE'
]

t_COMMENT = r'(\[[^\]]*\])'
t_ignore = r' \t\r\n\f\v'


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_IDENTIFIER(t):
    r'[_a-z]+'
    t.type = 'IDENTIFIER'
    return t


t_DECLARE = r'DECLARE'
t_IN = r'IN'
t_END = r'END'
t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'
t_WHILE = r'WHILE'
t_DO = r'DO'
t_ENDWHILE = r'ENDWHILE'
t_ENDDO = r'ENDDO'
t_FOR = r'FOR'
t_FROM = r'FROM'
t_TO = r'TO'
t_ENDFOR = r'ENDFOR'
t_DOWNTO = r'DOWNTO'
t_READ = r'READ'
t_WRITE = r'WRITE'

t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'
t_BRACKET_LEFT = r'\('
t_BRACKET_RIGHT = r'\)'
t_EQUALS = r'\='
t_NOT = r'\!'
t_LESS_THAN = r'\<'
t_GREATER_THAN = r'\>'
t_END_LINE = r'\n'


def t_error(t):
    # print("Syntax error")
    t.lexer.skip(1)
    return 'ERROR'


lexer = lex.lex()
