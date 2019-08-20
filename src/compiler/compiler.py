from src.compiler.grammar_parser import parser


def run_compiler(path):
    try:
        with open(path, 'r') as file:
            data = file.read()
            data = data.replace('\t', '')
        s = data
        parser.parse(s)
    except FileNotFoundError:
        print("File not found")
    except EOFError:
        exit(-1)
    print("END_OF_PARSER")
