import ply.yacc as yacc
from source.syntax_tree import *
from source.lex import tokens

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

start = 'start'


def get_place(p):
    return p.lineno(0), p.lexpos(0)


def p_goal(p):
    """
    start : main_class class_s
          | main_class
    """
    if len(p) == 2:
        p[0] = Program(p[1], None, get_place(p))
    else:
        p[0] = Program(p[1], p[2], get_place(p))
    return p[0]


def p_main_class(p):
    """
    main_class : CLASS id L_BRACKET PUBLIC STATIC_VOID_MAIN L_ROUND STRING L_SQUARE R_SQUARE id R_ROUND L_BRACKET statement_s R_BRACKET R_BRACKET
    """
    p[0] = MainClass(p[2], p[10], p[13], get_place(p))


def p_class_s(p):
    """
    class_s : class_s class
            | class
    """
    if len(p) == 2:
        p[0] = ClassDeclList(p[1], None)
    else:
        p[0] = ClassDeclList(p[2], p[1])


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
            p[0] = ClassDecl(p[2], None, None, None, get_place(p))
        elif len(p) == 7:
            p[0] = ClassDecl(p[2], None, p[4], p[5], get_place(p))
        elif isinstance(p[4], VarDeclList):
            p[0] = ClassDecl(p[2], None, p[4], None, get_place(p))
        elif isinstance(p[4], MethodDeclList):
            p[0] = ClassDecl(p[2], None, None, p[4], get_place(p))
    else:
        if isinstance(p[6], str):
            p[0] = ClassDecl(p[2], p[4], None, None, get_place(p))
        elif len(p) == 9:
            p[0] = ClassDecl(p[2], p[4], p[6], p[7], get_place(p))
        elif isinstance(p[6], VarDeclList):
            p[0] = ClassDecl(p[2], p[4], p[6], None, get_place(p))
        elif isinstance(p[6], MethodDeclList):
            p[0] = ClassDecl(p[2], p[4], None, p[7], get_place(p))


def p_var_s(p):
    """
    var_s : var_s var
          | var
    """
    if len(p) == 2:
        p[0] = VarDeclList(p[1], None)
    else:
        p[0] = VarDeclList(p[2], p[1])


def p_var(p):
    """
    var : type id SEMICOLON
    """
    p[0] = VarDecl(p[1], p[2], get_place(p))


def p_method_s(p):
    """
    method_s : method_s method
             | method
    """
    if len(p) == 2:
        p[0] = MethodDeclList(p[1], None)
    else:
        p[0] = MethodDeclList(p[2], p[1])


def p_method(p):
    """
    method : modifier type id L_ROUND arg_s R_ROUND L_BRACKET var_s statement_s RETURN exp SEMICOLON R_BRACKET
           | modifier type id L_ROUND arg_s R_ROUND L_BRACKET var_s RETURN exp SEMICOLON R_BRACKET
           | modifier type id L_ROUND arg_s R_ROUND L_BRACKET statement_s RETURN exp SEMICOLON R_BRACKET
           | modifier type id L_ROUND arg_s R_ROUND L_BRACKET RETURN exp SEMICOLON R_BRACKET
    """
    if isinstance(p[8], str):
        p[0] = MethodDecl(p[1], p[2], p[3], p[5], None, None, p[9], get_place(p))
    elif len(p) == 14:
        p[0] = MethodDecl(p[1], p[2], p[3], p[5], p[8], p[9], p[11], get_place(p))
    elif isinstance(p[8], VarDeclList):
        p[0] = MethodDecl(p[1], p[2], p[3], p[5], p[8], None, p[10], get_place(p))
    else:
        p[0] = MethodDecl(p[1], p[2], p[3], p[5], None, p[8], p[10], get_place(p))


def p_arg_s(p):
    """
    arg_s : empty
          | arg_s COMMA arg
          | arg
    """
    if isinstance(p[1], ArgDecl):
        p[0] = ArgDeclList(p[1], None)
    elif len(p) == 4:
        p[0] = ArgDeclList(p[3], p[1])
    else:
        p[0] = None


def p_arg(p):
    """
    arg : type id
    """
    p[0] = ArgDecl(p[1], p[2], get_place(p))


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
        p[0] = BasicType('int_array')
    elif p[1] == 'boolean':
        p[0] = BasicType('boolean')
    elif p[1] == 'int':
        p[0] = BasicType('int')
    else:
        p[0] = ClassType(p[1])


def p_statement_s(p):
    """
    statement_s : statement_s statement
                | statement
    """
    if len(p) == 2:
        p[0] = StatementList(p[1], None)
    else:
        p[0] = StatementList(p[2], p[1])


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
        p[0] = IfStatement(p[3], p[5], p[7], get_place(p))
    elif p[1] == 'while':
        p[0] = WhileStatement(p[3], p[5], get_place(p))
    elif p[1] == 'System.out.println':
        p[0] = PrintLineStatement(p[3], get_place(p))
    elif len(p) == 4:
        p[0] = Statements(p[2])
    elif len(p) == 5:
        p[0] = AssignStatement(p[1], p[3], get_place(p))
    else:
        p[0] = RandomAccessAssignStatement(p[1], p[3], p[6], get_place(p))


def p_exp_s(p):
    """
    exp_s : exp_s COMMA exp
          | exp
    """
    if len(p) == 2:
        p[0] = ExprList(p[1], None)
    else:
        p[0] = ExprList(p[3], p[1])


def p_exp(p):
    """
    exp : exp L_SQUARE exp R_SQUARE
        | exp DOT LENGTH                                               
        | exp DOT id L_ROUND R_ROUND                                   
        | exp DOT id L_ROUND exp_s R_ROUND
    """
    if len(p) == 5:
        p[0] = RandomAccessExpr(p[1], p[3], get_place(p))
    elif len(p) == 4:
        p[0] = LengthExpr(p[1], get_place(p))
    elif len(p) == 5:
        p[0] = CallMethodExpr(p[1], p[3], None, get_place(p))
    else:
        p[0] = CallMethodExpr(p[1], p[3], p[5], get_place(p))


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
    if p[1] == 'True':
        p[0] = TrueExpr(get_place(p))
    elif p[1] == 'False':
        p[0] = FalseExpr(get_place(p))
    elif p[1] == 'this':
        p[0] = ThisExpr(get_place(p))
    elif len(p) == 6:
        p[0] = NewIntArrExpr(p[4], get_place(p))
    elif len(p) == 5:
        p[0] = NewObjectExpr(p[2], get_place(p))
    elif len(p) == 3:
        p[0] = NotExpr(p[2], get_place(p))
    elif len(p) == 4:
        p[0] = p[2]
    elif isinstance(p[1], int):
        p[0] = IntegerExpr(p[1], get_place(p))
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
    p[0] = BinaryExpr(p[1], p[2], p[3], get_place(p))


def p_id(p):
    """
    id : ID
    """
    p[0] = Id(p[1], get_place(p))


def p_empty(p):
    """empty :"""
    pass


def p_error(p):
    print("Syntax error in input!")
    exit(1)


parser = yacc.yacc()


def parse_program(file_path):
    with open(file_path) as file:
        text = file.read()
    result = parser.parse(text)
    return result
