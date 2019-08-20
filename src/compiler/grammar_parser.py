import ply.yacc as yacc
from src.compiler.grammar_lexer import lexer
from src.compiler.compiler_token_list import tokens as tokens
from src.compiler.tree.DeclarationsNode import DeclarationsNode
from src.compiler.tree.ProgramNode import ProgramNode
from src.compiler.Validator import validate_declarations, DeclarationError

tokens = tokens


def p_error(p):
    # """
    # error : ERROR
    # """
    print("Error at line: " + str(lexer.lineno) + "\nFound at: " + str(p.value))
    exit(-1)


def p_program(p):
    """
    program : DECLARE declarations IN commands END
    """
    print(p[2])
    decl = DeclarationsNode(p[2])


def p_declarations(p):
    """
    declarations : declarations IDENTIFIER SEMICOLON
                 | declarations IDENTIFIER BRACKET_LEFT NUMBER COLON NUMBER BRACKET_RIGHT SEMICOLON
                 | empty
    """
    try:
        validate_declarations(p)

        if len(p) == 4:
            p[1].append(p[2])
            p[0] = p[1]
        elif len(p) == 9:
            p[1].append((p[2], p[4], p[6]))
            p[0] = p[1]
        elif len(p) == 2:
            p[0] = []
    except DeclarationError as err:
        print_error_message(err)


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
    print("NUMBER:" + str(lexer.lineno))


def p_empty(p):
    """
    empty :
    """
    p[0] = None


parser = yacc.yacc()


def print_error_message(err):
    print("Error at line: " + str(lexer.lineno) + "\n" + err.message.format(err))
    exit(-1)
