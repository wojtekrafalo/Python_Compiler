import ply.yacc as yacc
import ply.lex as lex
import sys
from src.compiler import grammar_lexer
from src.compiler.compiler_token_list import tokens as tokens
tokens = tokens


def p_error(p):
    # """
    # error : ERROR
    # """
    print("SYNTAX ERROR: " + str(p.value))
    # print("SYNTAX ERROR.")
    exit(-1)


def p_program(p):
    """
    program : DECLARE declarations IN commands END
    """
    print(p[1])


def p_declarations(p):
    """
    declarations : declarations IDENTIFIER SEMICOLON
                 | declarations IDENTIFIER BRACKET_LEFT NUMBER COLON NUMBER BRACKET_RIGHT SEMICOLON
                 | empty
    """


def p_commands(p):
    """
    commands : commands command
             | command
    """


def p_command(p):
    """
    command : identifier COLON EQUALS expression SEMICOLON
            | IF condition THEN commands ELSE commands ENDIF
            | IF condition THEN commands ENDIF
            | WHILE condition DO commands ENDWHILE
            | DO commands WHILE condition ENDDO
            | FOR IDENTIFIER FROM value TO value DO commands ENDFOR
            | FOR IDENTIFIER FROM value DOWNTO value DO commands ENDFOR
            | READ identifier SEMICOLON
            | WRITE value SEMICOLON
    """


def p_expression(p):
    """
    expression : value
               | value PLUS value
               | value MINUS value
               | value MULTIPLY value
               | value DIVIDE value
               | value MODULO value
    """


def p_condition(p):
    """
    condition : value EQUALS value
              | value NOT EQUALS value
              | value LESS_THAN value
              | value GREATER_THAN value
              | value LESS_THAN EQUALS value
              | value GREATER_THAN EQUALS value
    """


def p_value(p):
    """
    value : NUMBER
          | IDENTIFIER
    """


def p_identifier(p):
    """
    identifier : IDENTIFIER
               | IDENTIFIER BRACKET_LEFT IDENTIFIER BRACKET_RIGHT
               | IDENTIFIER BRACKET_LEFT NUMBER BRACKET_RIGHT
    """


def p_empty(p):
    """
    empty :
    """
    p[0] = None


parser = yacc.yacc()

# TODO: Make a normal ignoring whitespaces in both grammars ;)
try:
    with open('..\\test_files\\test_1.txt', 'r') as file:
        data = file.read()
        data = data.replace('\n', '')
        data = data.replace('\t', '')
    s = data
    parser.parse(s)
except FileNotFoundError:
    print("File not found")
except EOFError:
    exit(-1)
print("END_OF_PARSER")
