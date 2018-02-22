# Пример полного разбора программы Factorial.exe
import os

from activation_records.frame_filler import FrameFiller

from ir_tree.translate.ir_builder import IRBuilder
from ir_tree.translate.ir_printer import IRPrinter

from symbol_table.table import Table
from symbol_table.table_filler import TableFiller

from syntax_tree import Printer

from type_checker.type_checker import TypeChecker

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
    printer = Printer('../tests/ast_tree.gv')
    printer.visit(program)
    printer.print_to_file()
    print()

    # отображаем символьную таблицу
    print('### Символьная таблица ###')
    table = Table()
    filler = TableFiller(table, verbose=True)
    filler.fill_table(program)
    table = filler.table
    print()

    # проверка тайпчекером
    print('### Проверка типов тайпчекером ###')
    type_checker = TypeChecker(table)
    type_checker.check_ast_st(program)
    print()

    # заполняем class_struct-ы
    filler.fill_class_struct()
    table = filler.table

    # записи активаций
    print('### Записи активаций ###')
    frame_filler = FrameFiller(table, verbose=True)
    frame_filler.fill()
    print()

    # строим IR дерево
    print('### Построение IR дерева ###')
    builder = IRBuilder(table)
    builder.parse(program)
    trees = builder.trees
    print()

    # распечатываем IR дерево
    print('### Печать IR дерева ###')
    printer = IRPrinter('../tests/ir_tree.gv')
    printer.create_graph(trees)
    printer.print_to_file()
    print()
