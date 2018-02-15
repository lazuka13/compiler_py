import ply.lex as ply_lex
import ply.yacc as ply_yacc

import syntax_tree as ast
from lex import *

"""
# Подробное описание работы с YACC можно найти в документации Ply
# http://www.dabeaz.com/ply/ply.html
"""

# Задаем приоритет операций #
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'MINUS', 'PLUS'),
    ('left', 'PERCENT'),
    ('left', 'STAR'),
    ('left', 'LESS'),
    ('right', 'BANG'),
    ('left', 'DOT'),
    ('left', 'L_SQUARE'),
)

# Задаем стартовый символ - с него начинается разбор #
start = 'start'

text = None


# Функция определения координат токена #
def get_pos(p):
    x = find_column(p.lexpos(0))
    y = p.lineno(0)
    return x, y


def find_column(lex_pos):
    last_cr = text.rfind('\n', 0, lex_pos)
    if last_cr < 0:
        last_cr = 0
    column = (lex_pos - last_cr)
    return column or 1


# Набор правил для yacc в соответствии с грамматикой #
def p_goal(p):
    """
    start : main_class class_s
          | main_class
    """
    if len(p) == 2:
        p[0] = ast.Program(p[1], None, ast.Position(*get_pos(p)))
    else:
        p[0] = ast.Program(p[1], p[2], ast.Position(*get_pos(p)))
    return p[0]


def p_main_class(p):
    """
    main_class : CLASS id L_BRACKET PUBLIC STATIC_VOID_MAIN L_ROUND STRING L_SQUARE R_SQUARE id R_ROUND L_BRACKET statement_s R_BRACKET R_BRACKET
    """
    p[0] = ast.MainClass(p[2], p[10], p[13], ast.Position(*get_pos(p)))


def p_class_s(p):
    """
    class_s : class_s class
            | class
    """
    if len(p) == 2:
        p[0] = ast.ClassDeclList(p[1], None)
    else:
        p[0] = ast.ClassDeclList(p[2], p[1])


def p_class(p):
    """
    class : CLASS id L_BRACKET R_BRACKET
          | CLASS id L_BRACKET var_s R_BRACKET
          | CLASS id L_BRACKET method_s R_BRACKET
          | CLASS id L_BRACKET var_s method_s R_BRACKET
          | CLASS id EXTENDS id L_BRACKET R_BRACKET
          | CLASS id EXTENDS id L_BRACKET var_s R_BRACKET
          | CLASS id EXTENDS id L_BRACKET method_s R_BRACKET
          | CLASS id EXTENDS id L_BRACKET var_s method_s R_BRACKET
    """
    if p[3] != 'extends':
        if isinstance(p[4], str):
            p[0] = ast.ClassDecl(p[2], None, None, None, ast.Position(*get_pos(p)))
        elif len(p) == 7:
            p[0] = ast.ClassDecl(p[2], None, p[4], p[5], ast.Position(*get_pos(p)))
        elif isinstance(p[4], ast.VarDeclList):
            p[0] = ast.ClassDecl(p[2], None, p[4], None, ast.Position(*get_pos(p)))
        elif isinstance(p[4], ast.MethodDeclList):
            p[0] = ast.ClassDecl(p[2], None, None, p[4], ast.Position(*get_pos(p)))
    else:
        if isinstance(p[6], str):
            p[0] = ast.ClassDecl(p[2], p[4], None, None, ast.Position(*get_pos(p)))
        elif len(p) == 9:
            p[0] = ast.ClassDecl(p[2], p[4], p[6], p[7], ast.Position(*get_pos(p)))
        elif isinstance(p[6], ast.VarDeclList):
            p[0] = ast.ClassDecl(p[2], p[4], p[6], None, ast.Position(*get_pos(p)))
        elif isinstance(p[6], ast.MethodDeclList):
            p[0] = ast.ClassDecl(p[2], p[4], None, p[6], ast.Position(*get_pos(p)))


def p_var_s(p):
    """
    var_s : var_s var
          | var
    """
    if len(p) == 2:
        p[0] = ast.VarDeclList(p[1], None)
    else:
        p[0] = ast.VarDeclList(p[2], p[1])


def p_var(p):
    """
    var : type id SEMICOLON
    """
    p[0] = ast.VarDecl(p[1], p[2], ast.Position(*get_pos(p)))


def p_method_s(p):
    """
    method_s : method_s method
             | method
    """
    if len(p) == 2:
        p[0] = ast.MethodDeclList(p[1], None)
    else:
        p[0] = ast.MethodDeclList(p[2], p[1])


def p_method(p):
    """
    method : modifier type id L_ROUND arg_s R_ROUND L_BRACKET var_s statement_s RETURN exp SEMICOLON R_BRACKET
           | modifier type id L_ROUND arg_s R_ROUND L_BRACKET var_s RETURN exp SEMICOLON R_BRACKET
           | modifier type id L_ROUND arg_s R_ROUND L_BRACKET statement_s RETURN exp SEMICOLON R_BRACKET
           | modifier type id L_ROUND arg_s R_ROUND L_BRACKET RETURN exp SEMICOLON R_BRACKET
    """
    if isinstance(p[8], str):
        p[0] = ast.MethodDecl(p[1], p[2], p[3], p[5], None, None, p[9], ast.Position(*get_pos(p)))
    elif len(p) == 14:
        p[0] = ast.MethodDecl(p[1], p[2], p[3], p[5], p[8], p[9], p[11], ast.Position(*get_pos(p)))
    elif isinstance(p[8], ast.VarDeclList):
        p[0] = ast.MethodDecl(p[1], p[2], p[3], p[5], p[8], None, p[10], ast.Position(*get_pos(p)))
    else:
        p[0] = ast.MethodDecl(p[1], p[2], p[3], p[5], None, p[8], p[10], ast.Position(*get_pos(p)))


def p_arg_s(p):
    """
    arg_s : empty
          | arg_s COMMA arg
          | arg
    """
    if isinstance(p[1], ast.ArgDecl):
        p[0] = ast.ArgDeclList(p[1], None)
    elif len(p) == 4:
        p[0] = ast.ArgDeclList(p[3], p[1])
    else:
        p[0] = None


def p_arg(p):
    """
    arg : type id
    """
    p[0] = ast.ArgDecl(p[1], p[2], ast.Position(*get_pos(p)))


def p_modifier(p):
    """
    modifier : PUBLIC
             | PRIVATE
    """
    p[0] = str(p[1])


def p_type(p):
    """
    type : INT L_SQUARE R_SQUARE
         | BOOLEAN
         | INT
         | id
    """
    if len(p) == 4:
        p[0] = ast.BasicType('int_array')
    elif p[1] == 'boolean':
        p[0] = ast.BasicType('boolean')
    elif p[1] == 'int':
        p[0] = ast.BasicType('int')
    else:
        p[0] = ast.ClassType(p[1])


def p_statement_s(p):
    """
    statement_s : statement_s statement
                | statement
    """
    if len(p) == 2:
        p[0] = ast.StatementList(p[1], None)
    else:
        p[0] = ast.StatementList(p[2], p[1])


def p_statement(p):
    """
    statement : L_BRACKET statement_s R_BRACKET
              | IF L_ROUND exp R_ROUND statement ELSE statement
              | WHILE L_ROUND exp R_ROUND statement
              | SYSTEM_OUT_PRINTLN L_ROUND exp R_ROUND SEMICOLON
              | id EQUALS exp SEMICOLON
              | id L_SQUARE exp R_SQUARE EQUALS exp SEMICOLON
    """
    if p[1] == 'if':
        p[0] = ast.IfStatement(p[3], p[5], p[7], ast.Position(*get_pos(p)))
    elif p[1] == 'while':
        p[0] = ast.WhileStatement(p[3], p[5], ast.Position(*get_pos(p)))
    elif p[1] == 'System.out.println':
        p[0] = ast.PrintLineStatement(p[3], ast.Position(*get_pos(p)))
    elif len(p) == 4:
        p[0] = ast.Statements(p[2])
    elif len(p) == 5:
        p[0] = ast.AssignStatement(p[1], p[3], ast.Position(*get_pos(p)))
    else:
        p[0] = ast.RandomAccessAssignStatement(p[1], p[3], p[6], ast.Position(*get_pos(p)))


def p_exp_s(p):
    """
    exp_s : exp_s COMMA exp
          | exp
    """
    if len(p) == 2:
        p[0] = ast.ExprList(p[1], None)
    else:
        p[0] = ast.ExprList(p[3], p[1])


def p_exp(p):
    """
    exp : exp L_SQUARE exp R_SQUARE
        | exp DOT LENGTH                                               
        | exp DOT id L_ROUND R_ROUND                                   
        | exp DOT id L_ROUND exp_s R_ROUND
    """
    if len(p) == 5:
        p[0] = ast.RandomAccessExpr(p[1], p[3], ast.Position(*get_pos(p)))
    elif len(p) == 4:
        p[0] = ast.LengthExpr(p[1], ast.Position(*get_pos(p)))
    elif len(p) == 6:
        p[0] = ast.CallMethodExpr(p[1], p[3], None, ast.Position(*get_pos(p)))
    else:
        p[0] = ast.CallMethodExpr(p[1], p[3], p[5], ast.Position(*get_pos(p)))


def p_exp_vars(p):
    """
    exp : INTEGER
        | TRUE
        | FALSE
        | id
        | THIS
        | NEW INT L_SQUARE exp R_SQUARE
        | NEW id L_ROUND R_ROUND
        | BANG exp
        | L_ROUND exp R_ROUND
    """
    if p[1] == 'true' or p[1] == 'false':
        p[0] = ast.ValueExpr(ast.ValueEnum.BOOLEAN, p[1], ast.Position(*get_pos(p)))
    elif p[1] == 'this':
        p[0] = ast.ThisExpr(ast.Position(*get_pos(p)))
    elif len(p) == 6:
        p[0] = ast.NewIntArrExpr(p[4], ast.Position(*get_pos(p)))
    elif len(p) == 5:
        p[0] = ast.NewObjectExpr(p[2], ast.Position(*get_pos(p)))
    elif len(p) == 3:
        p[0] = ast.NotExpr(p[2], ast.Position(*get_pos(p)))
    elif len(p) == 4:
        p[0] = p[2]
    elif isinstance(p[1], int):
        p[0] = ast.ValueExpr(ast.ValueEnum.INTEGER, p[1], ast.Position(*get_pos(p)))
    else:
        p[0] = p[1]


def p_exp_binary_operation(p):
    """
    exp : exp AND exp
        | exp LESS exp
        | exp PLUS exp
        | exp MINUS exp
        | exp STAR exp
        | exp PERCENT exp
        | exp OR exp
    """
    p[0] = ast.BinaryExpr(p[1], p[2], p[3], ast.Position(*get_pos(p)))


def p_id(p):
    """
    id : ID
    """
    p[0] = ast.Id(p[1], ast.Position(*get_pos(p)))


def p_empty(_):
    """empty :"""
    pass


def p_error(p):
    raise SyntaxError(f"Syntax error in input! Text: {p}")


parser = ply_yacc.yacc()


# Функция для разбора программы - именно ее использует конечный пользователь #
def parse_program(file_path) -> ast.Program:
    global parser
    global text
    with open(file_path) as file:
        text = file.read()

    lexer = ply_lex.lex()
    result = parser.parse(text, tracking=True, lexer=lexer)

    return result
