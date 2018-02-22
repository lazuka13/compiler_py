from .base import Visitable


class Statement(Visitable):
    def __init__(self, position):
        Visitable.__init__(self, position)


class StatementList:
    def __init__(self, statement, prev=None):
        if prev is None:
            self.statement_list = []
        else:
            self.statement_list = prev.statement_list
        self.statement_list.append(statement)


class Statements(Statement):
    def __init__(self, statement_list):
        Statement.__init__(self, None)
        self.statement_list = statement_list.statement_list


class AssignStatement(Statement):
    def __init__(self, left, right, position):
        Statement.__init__(self, position)
        self.left = left
        self.right = right


class IfStatement(Statement):
    def __init__(self, condition, if_true, if_false, position):
        Statement.__init__(self, position)
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false


class PrintLineStatement(Statement):
    def __init__(self, obj, position):
        Statement.__init__(self, position)
        self.obj = obj


class RandomAccessAssignStatement(Statement):
    def __init__(self, id, position_in_arr, expr, position):
        Statement.__init__(self, position)
        self.id = id
        self.position_in_arr = position_in_arr
        self.expr = expr


class WhileStatement(Statement):
    def __init__(self, condition, action, position):
        Statement.__init__(self, position)
        self.condition = condition
        self.action = action


class ReturnStatement(Statement):
    def __init__(self, expression, position):
        Statement.__init__(self, position)
        self.expression = expression
