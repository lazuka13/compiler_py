import os
from pathlib import Path

import syntax_tree as ast
import symbol_table as st
import type_checker as tc
import activation_records as ar
from yacc import parse_program


def run_ast_tests():
    """
    Прогоняет тесты построения AST для всех программ
    в папках samples/good и samples/bad
    :return:
    """
    print("### Тесты AST ###")
    print()

    if not os.path.exists('../samples/good'):
        raise FileNotFoundError("Не найдена папка с примерами хорошего кода!")

    if not os.path.exists('../tests/ast'):
        os.mkdir('../tests/ast')

    if not os.path.exists('../tests/ast/good'):
        os.mkdir('../tests/ast/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))
        printer = ast.Printer(Path('../tests/ast/good') / Path(sample.replace('.java', '.gv')))
        printer.visit(program)
        printer.print_to_file()
        print()

    if not os.path.exists('../samples/bad'):
        raise FileNotFoundError("Не найдена папка с примерами плохого кода!")

    if not os.path.exists('../tests/ast/bad'):
        os.mkdir('../tests/ast/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))
            printer = ast.Printer(Path('../tests/ast/bad') / Path(sample.replace('.java', '.gv')))
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

    if not os.path.exists('../samples/good'):
        raise FileNotFoundError("Не найдена папка с примерами хорошего кода!")

    if not os.path.exists('../tests/st'):
        os.mkdir('../tests/st')

    if not os.path.exists('../tests/st/good'):
        os.mkdir('../tests/st/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))

        table = st.Table()
        filler = st.TableFiller(table)
        filler.parse_program(program, print_table=True)
        print()

    if not os.path.exists('../samples/bad'):
        raise FileNotFoundError("Не найдена папка с примерами плохого кода!")

    if not os.path.exists('../tests/st/bad'):
        os.mkdir('../tests/st/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))

            table = st.Table()
            filler = st.TableFiller(table)
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

    if not os.path.exists('../samples/good'):
        raise FileNotFoundError("Не найдена папка с примерами хорошего кода!")

    if not os.path.exists('../tests/st'):
        os.mkdir('../tests/st')

    if not os.path.exists('../tests/st/good'):
        os.mkdir('../tests/st/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))

        table = st.Table()

        type_checker = tc.TypeChecker()
        type_checker.check_ast_st(program, table)
        print()

    if not os.path.exists('../samples/bad'):
        raise FileNotFoundError("Не найдена папка с примерами плохого кода!")

    if not os.path.exists('../tests/st/bad'):
        os.mkdir('../tests/st/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))

            table = st.Table()

            type_checker = tc.TypeChecker()
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

    if not os.path.exists('../samples/good'):
        raise FileNotFoundError("Не найдена папка с примерами хорошего кода!")

    if not os.path.exists('../tests/st'):
        os.mkdir('../tests/st')

    if not os.path.exists('../tests/st/good'):
        os.mkdir('../tests/st/good')

    good_samples = os.listdir('../samples/good')
    for sample in good_samples:
        print(f'Разбираем хорошую программу {sample} ...')
        program = parse_program(Path('../samples/good') / Path(sample))

        table = st.Table()

        frame_filler = ar.FrameFiller(table)
        frame_filler.fill()
        print()

    if not os.path.exists('../samples/bad'):
        raise FileNotFoundError("Не найдена папка с примерами плохого кода!")

    if not os.path.exists('../tests/st/bad'):
        os.mkdir('../tests/st/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        try:
            program = parse_program(Path('../samples/bad') / Path(sample))

            table = st.Table()

            frame_filler = ar.FrameFiller(table)
            frame_filler.fill()
        except SyntaxError as error:
            print(error)
        print()


def run_tests():  # TODO сделать через CLICK с параметром теста
    if not os.path.exists('../tests'):
        os.mkdir('../tests')

    #run_ast_tests()
    #run_st_tests()
    run_tc_tests()
    run_ar_tests()


if __name__ == '__main__':
    run_tests()
