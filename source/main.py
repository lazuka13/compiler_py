from yacc import parse_program

import syntax_tree as ast
import symbol_table as st

if __name__ == '__main__':
    # строим абстрактное синтаксическое дерево
    program = parse_program("tests/file.txt")

    # распечатываем абстрактное синтаксическое дерево
    printer = ast.Printer('tests/out.gv')
    printer.visit(program)
    printer.print_to_file()

    # отображаем символьную таблицу
    table = st.Table()
    filler = st.TableFiller(table)
    filler.parse_program(program, print_table=True)
