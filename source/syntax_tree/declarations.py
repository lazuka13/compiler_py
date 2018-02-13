from .base import Visitable, Position
from .types import Type
from .statements import StatementList

"""
Тут описаны все типы деклараций в языке MiniJava

Отметим, что классы типа SomethingList в итоговом дереве не присутствуют - они нужны только для работы правил yacc
В дереве же список классов, например, будет храниться в Program.class_decl_list
"""


class ArgDecl(Visitable):
    """
    Декларация аргумента функции
    """

    def __init__(self, type_of: Type, id: str, position: Position):
        Visitable.__init__(self, position)
        self.type_of = type_of
        self.id = id


class ArgDeclList:
    """
    Список деклараций аргументов
    """

    def __init__(self, arg_decl: ArgDecl, prev: 'ArgDeclList' = None):
        if prev is None:
            self.arg_decl_list = []
        else:
            self.arg_decl_list = prev.arg_decl_list
        if id is None:
            return
        self.arg_decl_list.append(arg_decl)


class VarDecl(Visitable):
    """
    Декларация переменной
    """

    def __init__(self, type_of, id, position):
        Visitable.__init__(self, position)
        self.type_of = type_of
        self.id = id
        self.position = position


class VarDeclList:
    """
    Список деклараций переменных
    """

    def __init__(self, var_decl, prev=None):
        if prev is None:
            self.var_decl_list = []
        else:
            self.var_decl_list = prev.var_decl_list
        self.var_decl_list.append(var_decl)


class MethodDecl(Visitable):
    """
    Декларация метода
    """

    def __init__(self, access_modifier: str, type_of: Type, id: str, args: ArgDeclList, vars: VarDeclList,
                 statements: StatementList, result: Type, position: Position):
        Visitable.__init__(self, position)
        self.access_modifier = access_modifier
        self.type_of = type_of
        self.id = id
        self.arg_decl_list = args.arg_decl_list if args is not None else []
        self.var_decl_list = vars.var_decl_list if vars is not None else []
        self.statement_list = statements.statement_list if statements is not None else []
        self.result = result


class MethodDeclList:
    """
    Список деклараций методов
    """

    def __init__(self, method_decl: MethodDecl, prev: 'MethodDeclList' = None):
        if prev is None:
            self.method_decl_list = []
        else:
            self.method_decl_list = prev.method_decl_list
        self.method_decl_list.append(method_decl)


class ClassDecl(Visitable):
    """
    Декларация класса (не главного)
    """

    def __init__(self, id: str = None, extends: str = None, vars: VarDeclList = None, methods: MethodDeclList = None,
                 position: Position = None):
        Visitable.__init__(self, position)
        self.id = id
        self.extends = extends
        self.var_decl_list = vars.var_decl_list if vars is not None else []
        self.method_decl_list = methods.method_decl_list if methods is not None else []


class ClassDeclList:
    """
    Список деклараций классов (без главного)
    """

    def __init__(self, class_decl: ClassDecl, prev: 'ClassDeclList' = None):
        if prev is None:
            self.class_decl_list = []
        else:
            self.class_decl_list = prev.class_decl_list
        self.class_decl_list.append(class_decl)


class MainClass(Visitable):
    """
    Декларация главного класса (с функцией main)
    """

    def __init__(self, id: str, param_id: str, statements: StatementList, position):
        Visitable.__init__(self, position)
        self.id = id
        self.param_id = param_id
        self.statement_list = statements.statement_list if statements is not None else []
