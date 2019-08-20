import ply.yacc as yacc
from src.register_machine import register_lexer
from src.register_machine.register_token_list import tokens as tokens

tokens = tokens
commands = []


def p_input(p):
    """
    input : input line
          | empty
    """


def p_line(p):
    """
    line :  COM_1 SPACE REG NEW_LINE
         |  COM_1 SPACE REG SPACE NEW_LINE
         |  COM_1 SPACE REG SPACE COMMENT
         |  COM_1 SPACE REG COMMENT
         |  COM_2 SPACE REG SPACE REG NEW_LINE
         |  COM_2 SPACE REG SPACE REG SPACE NEW_LINE
         |  COM_2 SPACE REG SPACE REG SPACE COMMENT
         |  COM_2 SPACE REG SPACE REG COMMENT
         |  JUMP_1 SPACE LABEL NEW_LINE
         |  JUMP_1 SPACE LABEL SPACE NEW_LINE
         |  JUMP_1 SPACE LABEL SPACE COMMENT
         |  JUMP_1 SPACE LABEL COMMENT
         |  JUMP_2 SPACE REG SPACE LABEL NEW_LINE
         |  JUMP_2 SPACE REG SPACE LABEL SPACE NEW_LINE
         |  JUMP_2 SPACE REG SPACE LABEL SPACE COMMENT
         |  JUMP_2 SPACE REG SPACE LABEL COMMENT
         |  HALT SPACE COMMENT
         |  HALT SPACE NEW_LINE
         |  HALT NEW_LINE
         |  HALT COMMENT
         |  HALT SPACE
         |  HALT
         |  COMMENT
         |  ERROR
    """

    if p[1] == "COPY" or p[1] == "ADD" or p[1] == "SUB" or p[1] == "JZERO" or p[1] == "JODD":
        # print("LONG_COMMAND")
        commands.append((p[1], p[3], p[5]))
    elif p[1] == "GET" or p[1] == "PUT" or p[1] == "LOAD" \
            or p[1] == "STORE" or p[1] == "HALF" or p[1] == "INC" \
            or p[1] == "DEC" or p[1] == "JUMP":
        # print("MEDIUM_COMMAND")
        commands.append((p[1], p[3], ""))
    elif p[1] == "HALT":
        # print("SHORT_COMMAND")
        commands.append((p[1], "", ""))


def p_empty(p):
    """
    empty :
    """


def p_error(p):
    print("Syntax error:" + str(p))
    exit(-1)


parser = yacc.yacc()


def read_file(file):
    try:
        with open(file, 'r') as file:
            data = file.read()
        s = data
        parser.parse(s)
    except FileNotFoundError:
        print("File not found")
    except EOFError:
        exit(-1)
    print("END_OF_PARSER. # OF COMMANDS: " + str(len(commands)))
    return commands
