import ply.yacc as yacc
from src.compiler.grammar_lexer import lexer
from src.compiler.compiler_token_list import tokens, TokensEnum
from src.compiler.tree.ConditionNode import ConditionType, ConditionNode
from src.compiler.tree.ExpressionNode import ExpressionNode, ExpressionType
from src.compiler.tree.IdentifierNode import IdentifierType, IdentifierNode
from src.compiler.tree.MemoryManager import MemoryManager
from src.compiler.tree.ProgramNode import ProgramNode
from src.compiler.tree.MemoryManager import DeclarationError
from src.compiler.RegisterManager import RegisterManager
from src.compiler.tree.CommandNode import CommandNode, CommandType
from src.compiler.tree.ValueNode import ValueType, ValueNode

tokens = tokens
register_manager = RegisterManager
memory_manager = MemoryManager()


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
    memory_manager.manage_declared(p[2])
    p[0] = p[4].commands


def p_declarations(p):
    """
    declarations : declarations IDENTIFIER SEMICOLON
                 | declarations IDENTIFIER BRACKET_LEFT NUMBER COLON NUMBER BRACKET_RIGHT SEMICOLON
                 | empty
    """
    try:
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
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[1].add_command(p[2])
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
    if p[2] == TokensEnum.COLON and p[3] == TokensEnum.EQUALS and p[5] == TokensEnum.SEMICOLON:
        p[0] = CommandNode(CommandType.ASSIGNMENT, [p[1], p[4]])

    if p[1] == TokensEnum.IF and p[3] == TokensEnum.THEN and p[5] == TokensEnum.ELSE and p[7] == TokensEnum.ENDIF:
        p[0] = CommandNode(CommandType.IF_ELSE, [p[2], p[4], p[6]])
    if p[1] == TokensEnum.IF and p[3] == TokensEnum.THEN and p[5] == TokensEnum.ELSE and p[7] == TokensEnum.ENDIF and p[5] == TokensEnum.ENDIF:
        p[0] = CommandNode(CommandType.IF, [p[2], p[4]])

    if p[1] == TokensEnum.WHILE and p[3] == TokensEnum.DO and p[5] == TokensEnum.ENDWHILE:
        p[0] = CommandNode(CommandType.WHILE, [p[2], p[4]])

    if p[1] == TokensEnum.DO and p[3] == TokensEnum.WHILE and p[5] == TokensEnum.ENDDO:
        p[0] = CommandNode(CommandType.DO_WHILE, [p[2], p[4]])

    if p[1] == TokensEnum.FOR and p[3] == TokensEnum.FROM and p[7] == TokensEnum.DO and p[9] == TokensEnum.ENDFOR:
        tup = [p[2], p[4], p[6], p[8]]
        if p[5] == TokensEnum.TO:
            p[0] = CommandNode(CommandType.FOR_TO, tup)
        elif p[5] == TokensEnum.DOWNTO:
            p[0] = CommandNode(CommandType.FOR_DOWNTO, tup)

    if p[1] == TokensEnum.READ and p[3] == TokensEnum.SEMICOLON:
        p[0] = CommandNode(CommandType.READ, p[2])

    if p[1] == TokensEnum.WRITE and p[3] == TokensEnum.SEMICOLON:
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
        data = [p[1], p[3]]
        if p[2] == TokensEnum.PLUS:
            p[0] = ExpressionNode(ExpressionType.ADDITION, data)
        if p[2] == TokensEnum.MINUS:
            p[0] = ExpressionNode(ExpressionType.SUBSTRACTION, data)
        if p[2] == TokensEnum.MULTIPLY:
            p[0] = ExpressionNode(ExpressionType.MULTIPLICATION, data)
            print("DUPA. Miao WYPRINTOWAC")
        if p[2] == TokensEnum.DIVIDE:
            p[0] = ExpressionNode(ExpressionType.DIVISION, data)
        if p[2] == TokensEnum.MODULO:
            p[0] = ExpressionNode(ExpressionType.MODULATION, data)


def p_condition(p):
    """
    condition : value EQUALS value
              | value NOT EQUALS value
              | value LESS_THAN value
              | value GREATER_THAN value
              | value LESS_THAN EQUALS value
              | value GREATER_THAN EQUALS value
    """
    data = [p[1], p[3]]
    if p[2] == TokensEnum.EQUALS:
        p[0] = ConditionNode(ConditionType.EQUALS, data)
    if p[2] == TokensEnum.NOT and p[3] == TokensEnum.EQUALS:
        p[0] = ConditionNode(ConditionType.NOT_EQUALS, [p[1], p[4]])
    if p[2] == TokensEnum.LESS_THAN:
        p[0] = ConditionNode(ConditionType.LESS_THAN, data)
    if p[2] == TokensEnum.GREATER_THAN:
        p[0] = ConditionNode(ConditionType.GREATER_THAN, data)
    if p[2] == TokensEnum.LESS_THAN and p[3] == TokensEnum.EQUALS:
        p[0] = ConditionNode(ConditionType.LESS_EQUALS_THAN, [p[1], p[4]])
    if p[2] == TokensEnum.GREATER_THAN and p[3] == TokensEnum.EQUALS:
        p[0] = ConditionNode(ConditionType.GREATER_EQUALS_THAN, [p[1], p[4]])


def p_value(p):
    """
    value : NUMBER
          | IDENTIFIER
    """
    if p[1].type == TokensEnum.NUMBER:
        p[0] = ValueNode(ValueType.NUMBER, p[1])
    elif p[1].type == TokensEnum.IDENTIFIER:
        p[0] = ValueNode(ValueType.IDENTIFIER, p[1])


def p_identifier(p):
    """
    identifier : IDENTIFIER
               | IDENTIFIER BRACKET_LEFT IDENTIFIER BRACKET_RIGHT
               | IDENTIFIER BRACKET_LEFT NUMBER BRACKET_RIGHT
    """
    if len(p) == 2:
        p[0] = IdentifierNode(IdentifierType.VARIABLE, p[1])
    elif len(p) == 5 and p[3].type == TokensEnum.IDENTIFIER:
        p[0] = IdentifierNode(IdentifierType.ARRAY_VARIABLE, [p[1], p[3]])
    elif len(p) == 5 and p[3].type == TokensEnum.NUMBER:
        p[0] = IdentifierNode(IdentifierType.ARRAY_VALUE, [p[1], p[3]])


def p_empty(p):
    """
    empty :
    """
    p[0] = None


parser = yacc.yacc()


def print_error_message(err):
    print("Error at line: " + str(lexer.lineno) + "\n" + err.message.format(err))
    exit(-1)
