from .base import Visitable


class ArgDecl(Visitable):
    def __init__(self, type_of, id, position):
        Visitable.__init__(self, position)
        self.type_of = type_of
        self.id = id


class ArgDeclList:
    def __init__(self, arg_decl, prev=None):
        if prev is None:
            self.arg_decl_list = []
        else:
            self.arg_decl_list = prev.arg_decl_list
        if id is None:
            return
        self.arg_decl_list.append(arg_decl)


class ClassDecl(Visitable):
    def __init__(self, id=None, extends=None, vars=None, methods=None, position=None):
        Visitable.__init__(self, position)
        self.id = id
        self.extends = extends
        self.var_decl_list = vars.var_decl_list if vars is not None else []
        self.method_decl_list = methods.method_decl_list if methods is not None else []


class ClassDeclList:
    def __init__(self, class_decl, prev=None):
        if prev is None:
            self.class_decl_list = []
        else:
            self.class_decl_list = prev.class_decl_list
        self.class_decl_list.append(class_decl)


class MainClass(Visitable):
    def __init__(self, id, param_id, statements, position):
        Visitable.__init__(self, position)
        self.id = id
        self.param_id = param_id
        self.statement_list = statements.statement_list if statements is not None else []


class MethodDecl(Visitable):
    def __init__(self, modifier, type_of, id, args, vars, statements, result, position):
        Visitable.__init__(self, position)
        self.modifier = modifier
        self.type_of = type_of
        self.id = id
        self.arg_decl_list = args.arg_decl_list if args is not None else []
        self.var_decl_list = vars.var_decl_list if vars is not None else []
        self.statement_list = statements.statement_list if statements is not None else []

        self.result = result


class MethodDeclList:
    def __init__(self, method_decl, prev=None):
        if prev is None:
            self.method_decl_list = []
        else:
            self.method_decl_list = prev.method_decl_list
        self.method_decl_list.append(method_decl)


class VarDecl(Visitable):
    def __init__(self, type_of, id, position):
        Visitable.__init__(self, position)
        self.type_of = type_of
        self.id = id
        self.position = position


class VarDeclList:
    def __init__(self, var_decl, prev=None):
        if prev is None:
            self.var_decl_list = []
        else:
            self.var_decl_list = prev.var_decl_list
        self.var_decl_list.append(var_decl)
