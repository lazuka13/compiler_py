import os
from pathlib import Path

import syntax_tree as ast
from yacc import parse_program


def run_ast_tests():
    """
    Прогоняет тесты построения AST для всех программ
    в папках samples/good и samples/bad
    :return:
    """
    if not os.path.exists('../samples/good'):
        print("Не найдена папка с примерами хорошего кода!")
        return

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
        print("Не найдена папка с примерами плохого кода!")
        return

    if not os.path.exists('../tests/ast/bad'):
        os.mkdir('../tests/ast/bad')

    bad_samples = os.listdir('../samples/bad')
    for sample in bad_samples:
        print(f'Разбираем плохую программу {sample} ...')
        program = parse_program(Path('../samples/bad') / Path(sample))
        printer = ast.Printer(Path('../tests/ast/bad') / Path(sample.replace('.java', '.gv')))
        printer.visit(program)
        printer.print_to_file()
        print()


def run_tests():  # TODO сделать через CLICK с параметром теста
    if not os.path.exists('../tests'):
        os.mkdir('../tests')

    run_ast_tests()


if __name__ == '__main__':
    run_tests()
