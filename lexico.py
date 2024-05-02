# -*- coding: utf-8 -*-
import ply.lex as lex

# Lista de palabras reservadas de JavaScript
reserved = {
    'break': 'BREAK',
    'case': 'CASE',
    'catch': 'CATCH',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'debugger': 'DEBUGGER',
    'default': 'DEFAULT',
    'delete': 'DELETE',
    'do': 'DO',
    'else': 'ELSE',
    'finally': 'FINALLY',
    'for': 'FOR',
    'function': 'FUNCTION',
    'if': 'IF',
    'in': 'IN',
    'instanceof': 'INSTANCEOF',
    'new': 'NEW',
    'return': 'RETURN',
    'switch': 'SWITCH',
    'this': 'THIS',
    'throw': 'THROW',
    'try': 'TRY',
    'typeof': 'TYPEOF',
    'var': 'VAR',
    'void': 'VOID',
    'while': 'WHILE',
    'with': 'WITH',
    'let': 'LET',
    'class': 'CLASS',
    'export': 'EXPORT',
    'import': 'IMPORT'
}

# Lista de tokens
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'EQ', 'NEQ',
    'LT', 'LE', 'GT', 'GE', 'AND', 'OR', 'NOT',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COLON',
    'SEMICOLON', 'COMMA', 'DOT',
] + list(reserved.values())

# Reglas para tokens simples
t_AND = r'\&\&'
t_OR = r'\|\|'
t_NOT = r'!'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_VAR = r'\bvar\b'
t_LET = r'\blet\b'
t_CONST = r'\bconst\b'

# Regla para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Regla para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para cadenas de texto
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # quita las comillas
    return t

# Regla para espacios y tabulaciones
t_ignore = ' \t'

# Regla para manejar los saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construye el lexer
lexer = lex.lex()
