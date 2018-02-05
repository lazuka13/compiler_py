from source.syntax_tree import Printer
from source.yacc import parse_program
from source.symbol_table import Table, TableFiller

if __name__ == '__main__':
    # строим абстрактное синтаксическое дерево
    program = parse_program("tests/file.txt")

    # распечатываем абстрактное синтаксическое дерево
    printer = Printer('tests/out.gv')
    printer.visit(program)
    printer.print_to_file()

    # отображаем символьную таблицу
    table = Table()
    filler = TableFiller(table)
    filler.parse_program(program, print_table=True)
