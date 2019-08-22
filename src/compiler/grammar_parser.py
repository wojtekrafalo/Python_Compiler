import ply.yacc as yacc
from src.compiler.grammar_lexer import lexer
from src.compiler.compiler_token_list import tokens, TokensEnum
from src.compiler.tree.ConditionNode import ConditionNode, ConditionType
from src.compiler.tree.ExpressionNode import ExpressionNode, ExpressionType
from src.compiler.tree.IdentifierNode import IdentifierNode, IdentifierType
from src.compiler.MemoryManager import memory_manager
from src.compiler.MemoryManager import DeclarationError
from src.compiler.RegisterManager import register_manager
from src.compiler.tree.CommandNode import CommandNode, CommandType, build_commands
from src.compiler.tree.ValueNode import ValueNode, ValueType
from src.compiler.grammar_lexer import MyToken

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
    memory_manager.manage_declared(p[2])
    build_commands(p[4])
    # p[0] = p[4].commands


def p_declarations(p):
    """
    declarations : declarations IDENTIFIER SEMICOLON
                 | declarations IDENTIFIER BRACKET_LEFT NUMBER COLON NUMBER BRACKET_RIGHT SEMICOLON
                 | empty
    """
    try:
        if len(p) == 4:
            p[1].append(p[2].value)
            p[0] = p[1]
        elif len(p) == 9:
            p[1].append((p[2].value, p[4].value, p[6].value))
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
    # if len(p) == 2:
    #     print("COMM: " + str(p[1]))
    # else:
    #     print("COMMs: " + str(p[1]) + "COMM: " + str(p[2]))

    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]


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
    if str(p[2]) == str(TokensEnum.COLON) and str(p[3]) == str(TokensEnum.EQUALS) and str(p[5]) == str(
            TokensEnum.SEMICOLON):
        p[0] = CommandNode(CommandType.ASSIGNMENT, [p[1], p[4]])

    if str(p[1]) == str(TokensEnum.IF) and str(p[3]) == str(TokensEnum.THEN) and \
            str(p[5]) == str(TokensEnum.ELSE) and str(p[7]) == str(TokensEnum.ENDIF):
        p[0] = CommandNode(CommandType.IF_ELSE, [p[2], p[4], p[6]])

    if str(p[1]) == str(TokensEnum.IF) and str(p[3]) == str(TokensEnum.THEN) and \
            str(p[5]) == str(TokensEnum.ENDIF):
        p[0] = CommandNode(CommandType.IF, [p[2], p[4]])

    if str(p[1]) == str(TokensEnum.WHILE) and str(p[3]) == str(TokensEnum.DO) and str(p[5]) == str(TokensEnum.ENDWHILE):
        p[0] = CommandNode(CommandType.WHILE, [p[2], p[4]])

    if str(p[1]) == str(TokensEnum.DO) and str(p[3]) == str(TokensEnum.WHILE) and str(p[5]) == str(TokensEnum.ENDDO):
        p[0] = CommandNode(CommandType.DO_WHILE, [p[2], p[4]])

    if str(p[1]) == str(TokensEnum.FOR) and str(p[3]) == str(TokensEnum.FROM) and str(p[7]) == str(
            TokensEnum.DO) and str(p[9]) == str(TokensEnum.ENDFOR):
        tup = [p[2].value, p[4], p[6], p[8]]
        if str(p[5]) == str(TokensEnum.TO):
            p[0] = CommandNode(CommandType.FOR_TO, tup)
        elif str(p[5]) == str(TokensEnum.DOWNTO):
            p[0] = CommandNode(CommandType.FOR_DOWNTO, tup)

    if str(p[1]) == str(TokensEnum.READ) and str(p[3]) == str(TokensEnum.SEMICOLON):
        p[0] = CommandNode(CommandType.READ, p[2])

    if str(p[1]) == str(TokensEnum.WRITE) and str(p[3]) == str(TokensEnum.SEMICOLON):
        p[0] = CommandNode(CommandType.WRITE, p[2])


def p_expression(p):
    """
    expression : value
               | value PLUS value
               | value MINUS value
               | value MULTIPLY value
               | value DIVIDE value
               | value MODULO value
    """
    if len(p) == 2:
        p[0] = ExpressionNode(ExpressionType.NONE, p[1])
    else:
        if str(p[2]) == str(TokensEnum.PLUS):
            p[0] = ExpressionNode(ExpressionType.ADDITION, p[1], p[3])
        if str(p[2]) == str(TokensEnum.MINUS):
            p[0] = ExpressionNode(ExpressionType.SUBSTRACTION, p[1], p[3])
        if str(p[2]) == str(TokensEnum.MULTIPLY):
            p[0] = ExpressionNode(ExpressionType.MULTIPLICATION, p[1], p[3])
        if str(p[2]) == str(TokensEnum.DIVIDE):
            p[0] = ExpressionNode(ExpressionType.DIVISION, p[1], p[3])
        if str(p[2]) == str(TokensEnum.MODULO):
            p[0] = ExpressionNode(ExpressionType.MODULATION, p[1], p[3])


def p_condition(p):
    """
    condition : value EQUALS value
              | value NOT EQUALS value
              | value LESS_THAN value
              | value GREATER_THAN value
              | value LESS_THAN EQUALS value
              | value GREATER_THAN EQUALS value
    """
    if str(p[2]) == str(TokensEnum.EQUALS):
        p[0] = ConditionNode(ConditionType.EQUALS, p[1], p[3])
    if str(p[2]) == str(TokensEnum.NOT) and str(p[3]) == str(TokensEnum.EQUALS):
        p[0] = ConditionNode(ConditionType.NOT_EQUALS, p[1], p[4])
    if str(p[2]) == str(TokensEnum.LESS_THAN):
        p[0] = ConditionNode(ConditionType.LESS_THAN, p[1], p[3])
    if str(p[2]) == str(TokensEnum.GREATER_THAN):
        p[0] = ConditionNode(ConditionType.GREATER_THAN, p[1], p[3])
    if str(p[2]) == str(TokensEnum.LESS_THAN) and str(p[3]) == str(TokensEnum.EQUALS):
        p[0] = ConditionNode(ConditionType.LESS_EQUALS_THAN, p[1], p[4])
    if str(p[2]) == str(TokensEnum.GREATER_THAN) and str(p[3]) == str(TokensEnum.EQUALS):
        p[0] = ConditionNode(ConditionType.GREATER_EQUALS_THAN, p[1], p[4])


def p_value(p):
    """
    value : NUMBER
          | identifier
    """
    if isinstance(p[1], MyToken):
        p[0] = ValueNode(ValueType.NUMBER, p[1].value)
    if isinstance(p[1], IdentifierNode):
        p[0] = ValueNode(ValueType.IDENTIFIER, p[1])


def p_identifier(p):
    """
    identifier : IDENTIFIER
               | IDENTIFIER BRACKET_LEFT IDENTIFIER BRACKET_RIGHT
               | IDENTIFIER BRACKET_LEFT NUMBER BRACKET_RIGHT
    """
    if len(p) == 2:
        p[0] = IdentifierNode(IdentifierType.VARIABLE, p[1].value)
    elif len(p) == 5 and p[3].token_type == TokensEnum.IDENTIFIER:
        p[0] = IdentifierNode(IdentifierType.ARRAY_VARIABLE, p[1].value, p[3].value)
    elif len(p) == 5 and p[3].token_type == TokensEnum.NUMBER:
        p[0] = IdentifierNode(IdentifierType.ARRAY_VALUE, p[1].value, p[3].value)


def p_empty(p):
    """
    empty :
    """
    p[0] = None


parser = yacc.yacc()


def print_error_message(err):
    print("Error at line: " + str(lexer.lineno) + "\n" + err.message.format(err))
    exit(-1)


# def get_register_manager():
#     return register_manager
#
#
# def get_memory_manager():
#     return memory_manager
