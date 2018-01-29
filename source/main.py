from source.syntax_tree import Printer
from source.yacc import parse_program

if __name__ == '__main__':
    # parsing source code
    program = parse_program("tests/file.txt")

    # printing syntax tree
    printer = Printer('tests/out.gv')
    printer.visit(program)
    printer.print_to_file()
