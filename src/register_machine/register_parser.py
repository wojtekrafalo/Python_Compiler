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
         |  COM_2 SPACE REG SPACE REG NEW_LINE
         |  JUMP_1 SPACE LABEL NEW_LINE
         |  JUMP_2 SPACE REG SPACE LABEL NEW_LINE
         |  HALT NEW_LINE
         |  ERROR
    """
    if len(p) == 7:
        # print("LONG_COMMAND")
        commands.append((p[1], p[3], p[5]))
    elif len(p) == 5:
        # print("MEDIUM_COMMAND")
        commands.append((p[1], p[3], ""))
    elif len(p) == 3:
        # print("SHORT_COMMAND")
        commands.append((p[1], "", ""))
    elif len(p) == 2:
        # print("IS_THAT_A_JOKE_COMMAND")
        p_error("Nierozpoznany symbol")
    elif len(p) == 1:
        # print("BAD_COUNTING")
        pass


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
