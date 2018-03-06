import os
import sys
from pathlib import Path

import click

from activation_records.frame_filler import FrameFiller
from ir_tree.translate.eseq_canonizer import EseqCanonizer
from ir_tree.translate.ir_builder import IRBuilder
from ir_tree.translate.ir_printer import IRPrinter
from ir_tree.translate.linearizer import Linearizer
from symbol_table.table import Table
from symbol_table.table_filler import TableFiller
from syntax_tree import Printer
from type_checker.type_checker import TypeChecker
from yacc import parse_program


# TODO обновить тесты с учетом example! Хотя нужно ли заполнение class struct сейчас?

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
        filler = TableFiller(table, verbose=True)
        filler.fill_table(program)
        print()

    if not os.path.exists('../tests/st/bad'):
        os.mkdir('../tests/st/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))

            table = Table()
            filler = TableFiller(table, verbose=True)
            filler.fill_table(program)
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
        filler.fill_table(program)

        type_checker = TypeChecker(table)
        type_checker.check_ast_st(program)
        print()

    if not os.path.exists('../tests/st/bad'):
        os.mkdir('../tests/st/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))

            table = Table()
            filler = TableFiller(table, verbose=False)
            filler.fill_table(program)

            type_checker = TypeChecker(table)
            type_checker.check_ast_st(program)
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
        filler = TableFiller(table, verbose=False)
        filler.fill_table(program)

        frame_filler = FrameFiller(table)
        frame_filler.fill()
        print()


def run_ir_tests():
    """
    Прогоняет тесты записей активаций для всех программ
    в папках samples/good и samples/bad
    :return:
    """
    print("### Тесты IR ###")
    print()

    if not os.path.exists('../tests/ir_tree'):
        os.mkdir('../tests/ir_tree')

    if not os.path.exists('../tests/ir_tree/good'):
        os.mkdir('../tests/ir_tree/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path("../samples/good") / Path(sample))
        print()

        table = Table()
        filler = TableFiller(table, verbose=False)
        filler.fill_table(program)
        table = filler.table

        type_checker = TypeChecker(table)
        type_checker.check_ast_st(program)

        filler.fill_class_struct()
        table = filler.table

        frame_filler = FrameFiller(table, verbose=False)
        frame_filler.fill()

        builder = IRBuilder(table)
        builder.parse(program)
        trees = builder.trees

        printer = IRPrinter(Path('../tests/ir_tree/good') / Path(sample.replace('.java', '.gv')))
        printer.create_graph(trees)
        printer.print_to_file()
        print()


def run_cir_tests():
    """
    Прогоняет тесты канонизации IR деревьев
    в папке samples/good
    :return:
    """
    sys.setrecursionlimit(1500)

    print("### Тесты CIR ###")
    print()

    if not os.path.exists('../tests/cir_tree'):
        os.mkdir('../tests/cir_tree')

    if not os.path.exists('../tests/cir_tree/good'):
        os.mkdir('../tests/cir_tree/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path("../samples/good") / Path(sample))
        print()

        table = Table()
        filler = TableFiller(table, verbose=False)
        filler.fill_table(program)
        table = filler.table

        type_checker = TypeChecker(table)
        type_checker.check_ast_st(program)

        filler.fill_class_struct()
        table = filler.table

        frame_filler = FrameFiller(table, verbose=False)
        frame_filler.fill()

        builder = IRBuilder(table)
        builder.parse(program)
        trees = builder.trees

        canonizer = EseqCanonizer()
        canonized_trees = dict()
        for key, tree in trees.items():
            canonized_tree = canonizer.canonize(tree)
            canonized_trees[key] = canonized_tree

        printer = IRPrinter(Path('../tests/cir_tree/good') / Path(sample.replace('.java', '.gv')))
        printer.create_graph(canonized_trees)
        printer.print_to_file()
        print()


def run_lir_tests():
    """
    Прогоняет тесты линеаризации канонических IR деревьев
    в папке samples/good
    :return:
    """
    sys.setrecursionlimit(1500)

    print("### Тесты LIR ###")
    print()

    if not os.path.exists('../tests/lir_tree'):
        os.mkdir('../tests/lir_tree')

    if not os.path.exists('../tests/lir_tree/good'):
        os.mkdir('../tests/lir_tree/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path("../samples/good") / Path(sample))
        print()

        table = Table()
        filler = TableFiller(table, verbose=False)
        filler.fill_table(program)
        table = filler.table

        type_checker = TypeChecker(table)
        type_checker.check_ast_st(program)

        filler.fill_class_struct()
        table = filler.table

        frame_filler = FrameFiller(table, verbose=False)
        frame_filler.fill()

        builder = IRBuilder(table)
        builder.parse(program)
        trees = builder.trees

        canonizer = EseqCanonizer()
        canonized_trees = dict()
        for key, tree in trees.items():
            canonized_tree = canonizer.canonize(tree)
            canonized_trees[key] = canonized_tree

        linearizer = Linearizer()
        linearized = dict()
        for tree_key, tree_value in canonized_trees.items():
            linearized[tree_key] = []
            linearized[tree_key] = linearizer.linearize(tree_value, linearized[tree_key])

        printer = IRPrinter(Path('../tests/lir_tree/good') / Path(sample.replace('.java', '.gv')))
        printer.create_linearized_graph(linearized)
        printer.print_to_file()
        print()


@click.command()
@click.option('--test', '-t', default='all',
              help='What to test? (ast, st, tc, ar, ir, cir, lir, all).')
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

    if test == 'ir' or test == 'all':
        run_ir_tests()

    if test == 'cir' or test == 'all':
        run_cir_tests()

    if test == 'lir' or test == 'all':
        run_lir_tests()


if __name__ == '__main__':
    run_tests()
