import ply.lex as lex

tokens = [
    "L_BRACKET",
    "R_BRACKET",
    "L_ROUND",
    "R_ROUND",
    "L_SQUARE",
    "R_SQUARE",
    "SEMICOLON",
    "MINUS",
    "PLUS",
    "PERCENT",
    "EQUALS",
    "COMMA",
    "DOT",
    "STAR",
    "LESS",
    "BANG",
    "AND",
    "OR",
    "STATIC_VOID_MAIN",
    "SYSTEM_OUT_PRINTLN",
    "ID",
    "INTEGER",
    "COMMENT"
]

t_L_BRACKET = r'{'
t_R_BRACKET = r'}'
t_L_ROUND = r'\('
t_R_ROUND = r'\)'
t_L_SQUARE = r'\['
t_R_SQUARE = r'\]'
t_SEMICOLON = r'\;'
t_MINUS = r'\-'
t_PLUS = r'\+'
t_PERCENT = r'\%'
t_EQUALS = r'\='
t_COMMA = r'\,'
t_DOT = r'\.'
t_STAR = r'\*'
t_LESS = r'\<'
t_BANG = r'\!'
t_AND = r'\&\&'
t_OR = r'\|\|'

reserved = {
    r'class': "CLASS",
    r'extends': "EXTENDS",
    r'public': "PUBLIC",
    r'private': "PRIVATE",
    r'String': "STRING",
    r'int': "INT",
    r'boolean': "BOOLEAN",
    r'if': "IF",
    r'else': "ELSE",
    r'while': "WHILE",
    r'length': "LENGTH",
    r'true': "TRUE",
    r'false': "FALSE",
    r'new': "NEW",
    r'this': "THIS",
    r'return': "RETURN",
}

tokens += list(reserved.values())


def t_STATIC_VOID_MAIN(t):
    r"""static \s void \s main"""
    return t


def t_SYSTEM_OUT_PRINTLN(t):
    r"""System\.out\.println"""
    return t


def t_INTEGER(t):
    r"""[1-9][0-9]*|0"""
    t.value = int(t.value)
    return t


def t_ID(t):
    r"""[a-zA-Z\_]+[a-zA-Z0-9\_]*"""
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r"""\/\/.*"""
    pass


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))


t_ignore = ' \t'


def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column


lexer = lex.lex()
