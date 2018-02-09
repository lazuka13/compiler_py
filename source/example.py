# Пример полного разбора программы Factorial.exe

import symbol_table as st
import syntax_tree as ast
import type_checker as tc
from yacc import parse_program

if __name__ == '__main__':
    # строим абстрактное синтаксическое дерево
    print('### Построение абстрактного синтаксического дерева ###')
    program = parse_program("../samples/good/Factorial.java")
    print()

    # распечатываем абстрактное синтаксическое дерево
    print('### Печать абстрактного синтаксического дерева ###')
    printer = ast.Printer('out.gv')
    printer.visit(program)
    printer.print_to_file()
    print()

    # отображаем символьную таблицу
    print('### Символьная таблица ###')
    table = st.Table()
    filler = st.TableFiller(table)
    filler.parse_program(program, print_table=True)
    print()

    # проверка тайпчекером
    print('### Проверка типов тайпчекером ###')
    type_checker = tc.TypeChecker()
    type_checker.check_ast_st(program, table)
    print()
