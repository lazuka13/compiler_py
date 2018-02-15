# Пример полного разбора программы Factorial.exe
import os

from activation_records.FrameFiller import FrameFiller
from symbol_table.Table import Table
from symbol_table.TableFiller import TableFiller
from syntax_tree import Printer
from type_checker.TypeChecker import TypeChecker
from yacc import parse_program

if __name__ == '__main__':
    if not os.path.exists('../tests'):
        os.mkdir('../tests')

    # строим абстрактное синтаксическое дерево
    print('### Построение абстрактного синтаксического дерева ###')
    program = parse_program("../samples/good/Factorial.java")
    print()

    # распечатываем абстрактное синтаксическое дерево
    print('### Печать абстрактного синтаксического дерева ###')
    printer = Printer('../tests/out.gv')
    printer.visit(program)
    printer.print_to_file()
    print()

    # отображаем символьную таблицу
    print('### Символьная таблица ###')
    table = Table()
    filler = TableFiller(table)
    filler.fill_table(program, print_table=True)
    table = filler.table
    print()

    # проверка тайпчекером
    print('### Проверка типов тайпчекером ###')
    type_checker = TypeChecker()
    type_checker.check_ast_st(program, table)
    print()

    # заполняем class struct
    filler.fill_class_struct()
    table = filler.table

    # записи активаций
    print('### Записи активаций ###')
    frame_filler = FrameFiller(table)
    frame_filler.fill()
    print()
