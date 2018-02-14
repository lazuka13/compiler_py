import os
from pathlib import Path

import click

from activation_records.FrameFiller import FrameFiller
from symbol_table.Table import Table
from symbol_table.TableFiller import TableFiller
from syntax_tree import Printer
from type_checker.TypeChecker import TypeChecker
from yacc import parse_program


def run_ast_tests():
    """
    Прогоняет тесты построения AST для всех программ
    в папках samples/good и samples/bad
    :return:
    """
    print("### Тесты AST ###")
    print()

    if not os.path.exists('../tests/ast'):
        os.mkdir('../tests/ast')

    if not os.path.exists('../tests/ast/good'):
        os.mkdir('../tests/ast/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))
        printer = Printer(Path('../tests/ast/good') / Path(sample.replace('.java', '.gv')))
        printer.visit(program)
        printer.print_to_file()
        print()

    if not os.path.exists('../tests/ast/bad'):
        os.mkdir('../tests/ast/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))
            printer = Printer(Path('../tests/ast/bad') / Path(sample.replace('.java', '.gv')))
            printer.visit(program)
            printer.print_to_file()
        except SyntaxError as error:
            print(error)
        print()


def run_st_tests():
    """
    Прогоняет тесты получения символьной таблицы для всех программ
    в папках samples/good и samples/bad
    :return:
    """
    print("### Тесты ST ###")
    print()

    if not os.path.exists('../tests/st'):
        os.mkdir('../tests/st')

    if not os.path.exists('../tests/st/good'):
        os.mkdir('../tests/st/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))

        table = Table()
        filler = TableFiller(table)
        filler.parse_program(program, print_table=True)
        print()

    if not os.path.exists('../tests/st/bad'):
        os.mkdir('../tests/st/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))

            table = Table()
            filler = TableFiller(table)
            filler.parse_program(program, print_table=True)
        except SyntaxError as error:
            print(error)
        print()


def run_tc_tests():
    """
    Прогоняет тесты проверки типов тайпчекером для всех программ
    в папках samples/good и samples/bad
    :return:
    """
    print("### Тесты TC ###")
    print()

    if not os.path.exists('../tests/st'):
        os.mkdir('../tests/st')

    if not os.path.exists('../tests/st/good'):
        os.mkdir('../tests/st/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))

        table = Table()
        filler = TableFiller(table)
        filler.parse_program(program, print_table=False)

        type_checker = TypeChecker()
        type_checker.check_ast_st(program, table)
        print()

    if not os.path.exists('../tests/st/bad'):
        os.mkdir('../tests/st/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))

            table = Table()
            filler = TableFiller(table)
            filler.parse_program(program, print_table=False)

            type_checker = TypeChecker()
            type_checker.check_ast_st(program, table)
        except SyntaxError as error:
            print(error)
        print()


def run_ar_tests():
    """
    Прогоняет тесты записей активаций для всех программ
    в папках samples/good и samples/bad
    :return:
    """
    print("### Тесты AR ###")
    print()

    if not os.path.exists('../tests/st'):
        os.mkdir('../tests/st')

    if not os.path.exists('../tests/st/good'):
        os.mkdir('../tests/st/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))

        table = Table()
        filler = TableFiller(table)
        filler.parse_program(program, print_table=False)

        frame_filler = FrameFiller(table)
        frame_filler.fill()
        print()


@click.command()
@click.option('--test', '-t', default='all',
              help='What to test? (ast, st, tc, ar, all).')
def run_tests(test):
    if not os.path.exists('../tests'):
        os.mkdir('../tests')

    if not os.path.exists('../samples/good'):
        raise FileNotFoundError("Не найдена папка с примерами хорошего кода!")

    if not os.path.exists('../samples/bad'):
        raise FileNotFoundError("Не найдена папка с примерами плохого кода!")

    if test == 'ast' or test == 'all':
        run_ast_tests()

    if test == 'st' or test == 'all':
        run_st_tests()

    if test == 'tc' or test == 'all':
        run_tc_tests()

    if test == 'ar' or test == 'all':
        run_ar_tests()


if __name__ == '__main__':
    run_tests()
