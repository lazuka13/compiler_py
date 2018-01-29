from .base import Visitable


class Expr(Visitable):
    def __init__(self, label, place):
        self.label = label
        Visitable.__init__(self, place)


class ExprList():
    def __init__(self, expr, prev=None):
        if prev is None:
            self.expr_list = []
        else:
            self.expr_list = prev.expr_list
        self.expr_list.append(expr)


class BinaryExpr(Expr):
    def __init__(self, left, kind_of, right, place):
        Expr.__init__(self, kind_of, place)
        self.left = left
        self.right = right
        self.id = right


class BooleanExpr(Expr):
    def __init__(self, value, place):
        Expr.__init__(self, value, place)


class CallMethodExpr(Expr):
    def __init__(self, expr, id, params, place):
        Expr.__init__(self, expr.label, place)
        self.expr = expr
        self.id = id
        self.expt_list = params.expr_list if params is not None else None


class FalseExpr(Expr):
    def __init__(self, place):
        Expr.__init__(self, 'False', place)


class TrueExpr(Expr):
    def __init__(self, place):
        Expr.__init__(self, 'True', place)


class Id(Expr):
    def __init__(self, name, place):
        Expr.__init__(self, "name", place)
        self.name = name


class IntegerExpr(Expr):
    def __init__(self, value, place):
        Expr.__init__(self, str(value), place)
        self.value = value


class LengthExpr(Expr):
    def __init__(self, obj, place):
        Expr.__init__(self, "Length", place)
        self.obj = obj


class NewIntArrExpr(Expr):
    def __init__(self, size, place):
        Expr.__init__(self, 'NewIntArrExpr', place)
        self.size = size


class NewObjectExpr(Expr):
    def __init__(self, id, place):
        Expr.__init__(self, "NewObjectExpr", place)
        self.id = id


class NotExpr(Expr):
    def __init__(self, right, place):
        Expr.__init__(self, "NotExpr", place)
        self.right = right


class RandomAccessExpr(Expr):
    def __init__(self, object, position, place):
        Expr.__init__(self, "RandomAccessExpr", place)
        self.object = object
        self.position = position


class ThisExpr(Expr):
    def __init__(self, place):
        Expr.__init__(self, "ThisExpr", place)
