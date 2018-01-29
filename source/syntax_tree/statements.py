from .base import Visitable


class Statement(Visitable):
    def __init__(self, place):
        Visitable.__init__(self, place)


class StatementList:
    def __init__(self, statement, prev=None):
        if prev is None:
            self.statement_list = []
        else:
            self.statement_list = prev.statement_list
        self.statement_list.append(statement)


class Statements:
    def __init__(self, statement_list):
        self.statements = statement_list.statement_list


class AssignStatement(Statement):
    def __init__(self, left, right, place):
        Statement.__init__(self, place)
        self.left = left
        self.right = right


class IfStatement(Statement):
    def __init__(self, condition, if_true, if_false, place):
        Statement.__init__(self, place)
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false


class PrintLineStatement(Statement):
    def __init__(self, obj, place):
        Statement.__init__(self, place)
        self.obj = obj


class RandomAccessAssignStatement(Statement):
    def __init__(self, id, position, expr, place):
        Statement.__init__(self, place)
        self.id = id
        self.position = position
        self.expr = expr


class WhileStatement(Statement):
    def __init__(self, condition, action, place):
        Statement.__init__(self, place)
        self.condition = condition
        self.action = action
