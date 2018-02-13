from .base import Visitable, Position


class Expr(Visitable):
    def __init__(self, label: str, position: Position):
        self.label = label
        Visitable.__init__(self, position)


class ExprList():
    def __init__(self, expr: Expr, prev: 'ExprList' = None):
        if prev is None:
            self.expr_list = []
        else:
            self.expr_list = prev.expr_list
        self.expr_list.append(expr)


class BinaryExpr(Expr):
    def __init__(self, left: Expr, kind_of: str, right: Expr, position: Position):  # TODO переделать на Enum
        Expr.__init__(self, kind_of, position)
        self.left = left
        self.right = right
        self.id = right


class CallMethodExpr(Expr):
    def __init__(self, expr: Expr, id: str, params: ExprList, position: Position):
        Expr.__init__(self, expr.label, position)
        self.expr = expr
        self.id = id
        self.expr_list = params.expr_list if params is not None else []


class FalseExpr(Expr):
    def __init__(self, position: Position):
        Expr.__init__(self, 'False', position)


class TrueExpr(Expr):
    def __init__(self, position: Position):
        Expr.__init__(self, 'True', position)


class Id(Expr):
    def __init__(self, name, position: Position):
        Expr.__init__(self, "name", position)
        self.name = name


class IntegerExpr(Expr):  # TODO подумать про структуру
    def __init__(self, value, position):
        Expr.__init__(self, str(value), position)
        self.value = value


class LengthExpr(Expr):
    def __init__(self, obj, position):
        Expr.__init__(self, "Length", position)
        self.obj = obj


class NewIntArrExpr(Expr):
    def __init__(self, size, position):
        Expr.__init__(self, 'NewIntArrExpr', position)
        self.size = size


class NewObjectExpr(Expr):
    def __init__(self, id, position):
        Expr.__init__(self, "NewObjectExpr", position)
        self.id = id


class NotExpr(Expr):
    def __init__(self, right, position):
        Expr.__init__(self, "NotExpr", position)
        self.right = right


class RandomAccessExpr(Expr):
    def __init__(self, object, position_in_arr, position):
        Expr.__init__(self, "RandomAccessExpr", position)
        self.object = object
        self.position_in_arr = position_in_arr


class ThisExpr(Expr):
    def __init__(self, position):
        Expr.__init__(self, "ThisExpr", position)
