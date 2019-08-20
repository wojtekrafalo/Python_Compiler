# import ply.yacc as yacc
# import ply.lex as lex
import sys
from src.compiler.compiler import run_compiler

run_compiler('..\\test_files\\test_1.txt')
print("BYE WORLD")

# def p_error(self, p):
#     if not p:
#         logging.info("Info - syntactic step parser - parsed.")
#         return
#
#     # http://www.dabeaz.com/ply/ply.html#ply_nn26 6.8.2
#     # Read ahead looking for a closing ';'
#
#     logging.warning(
#         'Warning - syntactic step parser - unexpected token type="{}" with value="{}" at position {}. Search an error before this point.'.format(
#             p.type, p.value, p.lexer.lexpos))
#     while True:
#         tok = self.parser.token()  # Get the next token
#         if not tok:
#             break
#     self.parser.restart()
