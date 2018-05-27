# Пример полного разбора программы Factorial.exe
import os

from activation_records.frame_filler import FrameFiller
from ir_tree.translate.eseq_canonizer import EseqCanonizer
from ir_tree.translate.ir_builder import IRBuilder
from ir_tree.translate.ir_printer import IRPrinter
from ir_tree.translate.linearizer import Linearizer
from ir_tree.translate.no_jump_block import NoJumpBlocksForest, NoJumpTree
from reg_lifecycle.lifecycle_graph import LifecycleGraph
from reg_lifecycle.lifecycle_printer import LifecyclePrinter
from reg_lifecycle.variable_graph import VariableGraph, Temp
from reg_lifecycle.variable_graph_printer import VariableGraphPrinter
from symbol_table.table import Table
from symbol_table.table_filler import TableFiller
from syntax_tree import Printer
from type_checker.type_checker import TypeChecker
from x86.x86_code_generation import Muncher, RegMove
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
    type_checker = TypeChecker(table, verbose=True)
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

    # канонизируем IR дерево
    print('### Канонизация IR дерева ###')
    canonizer = EseqCanonizer()
    canonized_trees = dict()
    for key, tree in trees.items():
        canonized_tree = canonizer.canonize(tree)
        canonized_trees[key] = canonized_tree
    print()

    print('### Печать IR дерева ###')
    printer = IRPrinter('../tests/cir_tree.gv')
    printer.create_graph(canonized_trees)
    printer.print_to_file()
    print()

    # линеаризируем IR дерево
    print('### Линеаризация дерева ###')
    linearizer = Linearizer()
    linearized = dict()
    for tree_key, tree_value in canonized_trees.items():
        linearized[tree_key] = []
        linearized[tree_key] = linearizer.linearize(tree_value, linearized[tree_key])
    print()

    # распечатываем линеаризированное IR дерево
    print('### Печать линеаризированного IR дерева ###')
    printer = IRPrinter('../tests/linear_tree.gv')
    printer.create_linearized_graph(linearized)
    printer.print_to_file()
    print()

    # генерируем reblocked IR дерево
    print('### Генерация Reblocked IR дерева ###')
    no_jump_forest: NoJumpBlocksForest = dict()
    for tree_key, tree_value in linearized.items():
        no_jump_forest[tree_key] = NoJumpTree(tree_value)
    reblocked = dict()
    for tree_key, tree_value in no_jump_forest.items():
        reblocked[tree_key] = tree_value.build_tree()
    print()

    # распечатываем reblocked IR дерево
    print('### Печать Reblocked IR дерева ###')
    printer = IRPrinter('../tests/reblocked_tree.gv')
    printer.create_linearized_graph(reblocked)
    printer.print_to_file()
    print()

    # распечатываем инструкции

    with open('../tests/output.asm', 'w', encoding='utf-8') as file:
        graphs = []
        lifecycle_printer = LifecyclePrinter('../tests/lifecycle.gv')
        lifecycle_printer.print_prefix()
        variable_printer = VariableGraphPrinter('../tests/variables.gv')
        variable_printer.print_prefix()
        for tree_key, tree in reblocked.items():
            file.write(tree_key + '\n')
            file.write('-' * 10 + '\n')
            muncher = Muncher(tree)
            list = muncher.create_instructions_list()

            iteration = 0
            fp = Temp('my_fp')
            while True:
                lifecycle_graph = LifecycleGraph(list)
                lifecycle_graph.build_Lifecycle()
                variables_graph = VariableGraph(lifecycle_graph, fp)
                bad_node = variables_graph._bad_node

                if bad_node is None:
                    lifecycle_printer.print(lifecycle_graph.nodes_list)
                    variable_printer.print(variables_graph)
                    break
                else:
                    if iteration == 100:
                        lifecycle_printer.print(lifecycle_graph.nodes_list)
                        variable_printer.print(variables_graph)
                        print('100 iters')
                        break
                    iteration += 1
                    temp_read = 0
                    temp_push = 0
                    i = 0
                    while i < len(list.instructions):
                        for var in list.instructions[i].src:
                            if var == bad_node.reg:
                                list.instructions[i].remove_used(var)
                                list.registers.append(Temp("Temp read from stack: " + str(temp_read)))
                                temp_read += 1
                                list.instructions[i].add_used(list.registers[-1])
                                list.instructions = list.instructions[:i] + [
                                    RegMove('MOV %0 [%1]', fp, list.registers[-1])] + list.instructions[i:]
                                i += 1
                                break
                        for var in list.instructions[i].dst:
                            if var == bad_node.reg:
                                list.instructions[i].remove_defined(var)
                                list.registers.append(Temp("Temp push to stack: " + str(temp_push)))
                                temp_push += 1
                                list.instructions[i].add_defined(list.registers[-1])
                                list.instructions = list.instructions[:i] + [
                                    RegMove('MOV %0 [%1]', list.registers[-1], fp)] + list.instructions[i:]
                                i += 1
                                break
                        i += 1
            for l in list.instructions:
                file.write(l.format_long() + '\n')
            file.write('\n')
        lifecycle_printer.print_postfix()
        variable_printer.print_postfix()
    print()
