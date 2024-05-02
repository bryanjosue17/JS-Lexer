# -*- coding: utf-8 -*-
import os
import codecs
import ply.yacc as yacc
from lexico import tokens
from lexico import lexer
from semantico import *

# Reglas de precedencia (de menor a mayor precedencia)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('nonassoc', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Definir la acción de inicio
def p_start(p):
    'start : program'
    p[0] = p[1]

# Definir la regla para el programa
def p_program(p):
    'program : statement_list'
    p[0] = NodoPrograma(p[1])

# Definir la regla para la lista de declaraciones
def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

# Definir la regla general para una declaración
def p_statement(p):
    '''
    statement : var_declaration
              | expression_statement
              | function_declaration
              | if_statement
              | for_statement
              | while_statement
              | do_while_statement
              | return_statement
              | break_statement
              | continue_statement
              | block
              | try_statement
              | throw_statement
              | switch_statement
              | with_statement
              | debugger_statement
              | class_declaration
              | import_statement
              | export_statement
    '''
    p[0] = p[1]  # Asume que todos estos producen un Nodo

# Definir la regla para una declaración de expresión
def p_expression_statement(p):
    'expression_statement : expression SEMICOLON'
    p[0] = NodoSentencia("ExpressionStatement", [p[1]])

# Definir la regla para una expresión
def p_expression(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | expression EQ expression
               | expression NEQ expression
               | expression LT expression
               | expression LE expression
               | expression GT expression
               | expression GE expression
               | expression AND expression
               | expression OR expression
               | NOT expression
               | ID
               | NUMBER
               | STRING
               | new_expression
               | delete_expression
               | function_call
               | array_access
               | object_access
               | expression_void
               | expression_in
               | expression_instanceof
               | expression_this
               | expression_typeof
               | expression_uminus
    '''
    if len(p) == 4:
        p[0] = NodoExpresionBinaria(p[2], p[1], p[3])
        print("Creating NodoExpresionBinaria with {}, {}, {}".format(p[1], p[2], p[3]))
    elif len(p) == 3:
        if p[1] == 'NOT':
            p[0] = NodoExpresionUnaria('NOT', p[2])
            print("Creating NodoExpresionUnaria with NOT, {}".format(p[2]))
        else:
            p[0] = NodoFunctionCall(p[1], p[2])
            print("Creating NodoFunctionCall with {}, {}".format(p[1], p[2]))
    else:
        if isinstance(p[1], str) and p[1].isidentifier():
            p[0] = NodoTerminal("Identifier", p[1])
            print("Creating NodoTerminal with Identifier {}".format(p[1]))
        elif isinstance(p[1], (int, float, str)):
            p[0] = NodoTerminal("Literal", p[1])
            print("Creating NodoTerminal with Literal {}".format(p[1]))
        else:
            p[0] = p[1]  # Esto asume que el token ya es un nodo
            print("Using existing Nodo")

# p_var_declaration
def p_var_declaration(p):
    '''
    var_declaration : VAR ID ASSIGN expression SEMICOLON
                    | LET ID ASSIGN expression SEMICOLON
                    | CONST ID ASSIGN expression SEMICOLON
    '''
    p[0] = NodoDeclaracionVariable(p[1], p[2], p[4])

# p_function_declaration
def p_function_declaration(p):
    'function_declaration : FUNCTION ID LPAREN opt_param_list RPAREN compound_statement'
    p[0] = NodoFuncion(p[2], p[4], p[6])

# p_if_statement
def p_if_statement(p):
    '''
    if_statement : IF LPAREN expression RPAREN statement
                 | IF LPAREN expression RPAREN statement ELSE statement
    '''
    if len(p) == 6:
        p[0] = NodoControlFlujo("If", p[3], p[5])
    else:
        p[0] = NodoControlFlujo("IfElse", p[3], p[5], p[7])

# p_for_statement
def p_for_statement(p):
    '''
    for_statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement
    '''
    p[0] = NodoControlFlujo("For", [p[3], p[4], p[5]], p[7])

# p_while_statement
def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN statement'
    p[0] = NodoControlFlujo("While", p[3], p[5])

# p_do_while_statement
def p_do_while_statement(p):
    'do_while_statement : DO statement WHILE LPAREN expression RPAREN SEMICOLON'
    p[0] = NodoControlFlujo("DoWhile", p[5], p[2])

# p_return_statement
def p_return_statement(p):
    'return_statement : RETURN expression SEMICOLON'
    p[0] = NodoSentencia("Return", p[2])

# p_break_statement
def p_break_statement(p):
    'break_statement : BREAK SEMICOLON'
    p[0] = NodoSentencia("Break")

# p_continue_statement
def p_continue_statement(p):
    'continue_statement : CONTINUE SEMICOLON'
    p[0] = NodoSentencia("Continue")

# p_try_statement
def p_try_statement(p):
    '''
    try_statement : TRY block catch_clause
                  | TRY block finally_clause
                  | TRY block catch_clause finally_clause
    '''
    if len(p) == 4:
        p[0] = NodoTry(p[2], p[3] if isinstance(p[3], NodoCatch) else None, None if isinstance(p[3], NodoCatch) else p[3])
    elif len(p) == 5:
        p[0] = NodoTry(p[2], p[3], p[4])

# p_throw_statement
def p_throw_statement(p):
    'throw_statement : THROW expression SEMICOLON'
    p[0] = NodoThrow(p[2])

# p_switch_statement
def p_switch_statement(p):
    '''
    switch_statement : SWITCH LPAREN expression RPAREN LBRACE case_statements default_case RBRACE
    '''
    p[0] = NodoSwitch(p[3], p[6], p[7])

# p_case_statements
def p_case_statements(p):
    '''
    case_statements : case_statement
                    | case_statements case_statement
    '''
    if len(p) == 2:
        p[0] = NodoListaDeclaraciones([p[1]])
    else:
        p[1].hijos.append(p[2])
        p[0] = p[1]

# p_case_statement
def p_case_statement(p):
    'case_statement : CASE expression COLON statement_list'
    p[0] = NodoCase(p[2], p[4])

# p_default_case
def p_default_case(p):
    'default_case : DEFAULT COLON statement_list'
    p[0] = NodoDefault(p[3])

# p_with_statement
def p_with_statement(p):
    'with_statement : WITH LPAREN expression RPAREN statement'
    p[0] = NodoWith(p[3], p[5])

# p_class_declaration
def p_class_declaration(p):
    'class_declaration : CLASS ID LBRACE class_body RBRACE'
    p[0] = NodoClassDeclaration(p[2], p[4])

# p_import_statement
def p_import_statement(p):
    'import_statement : IMPORT ID SEMICOLON'
    p[0] = NodoImport(p[2])

# p_export_statement
def p_export_statement(p):
    'export_statement : EXPORT ID SEMICOLON'
    p[0] = NodoExport(p[2])

def p_block(p):
    'block : LBRACE statement_list RBRACE'
    p[0] = NodoBlock([p[2]])

def p_catch_clause(p):
    'catch_clause : CATCH LPAREN ID RPAREN block'
    p[0] = NodoCatchClause(p[3], p[5])

def p_finally_clause(p):
    'finally_clause : FINALLY block'
    p[0] = NodoFinallyClause([p[2]])

def p_new_expression(p):
    'new_expression : NEW ID'
    p[0] = NodoNewExpression("New", p[2])

def p_delete_expression(p):
    'delete_expression : DELETE expression'
    p[0] = NodoDeleteExpression([p[2]])

def p_function_call(p):
    'function_call : ID LPAREN argument_list RPAREN'
    p[0] = NodoFunctionCall(p[1], p[3])

def p_array_access(p):
    'array_access : ID LBRACKET expression RBRACKET'
    p[0] = NodoArrayAccess(p[1], p[3])

def p_object_access(p):
    'object_access : ID DOT ID'
    p[0] = NodoObjectAccess(p[1], p[3])

def p_debugger_statement(p):
    'debugger_statement : DEBUGGER SEMICOLON'
    p[0] = NodoDebuggerStatement()

def p_opt_param_list(p):
    '''
    opt_param_list : param_list
                   | empty
    '''
    p[0] = NodoOptParamList([p[1]] if p[1] else [])

def p_param_list(p):
    '''
    param_list : ID
               | param_list COMMA ID
    '''
    if len(p) == 2:
        p[0] = NodoArgumentList([p[1]])
    else:
        p[1].argumentos.append(p[3])
        p[0] = p[1]

def p_compound_statement(p):
    'compound_statement : LBRACE statement_list RBRACE'
    p[0] = NodoCompoundStatement([p[2]])

def p_class_body(p):
    '''
    class_body : class_member
               | class_body class_member
    '''
    if len(p) == 2:
        p[0] = NodoClassBody([p[1]])
    else:
        p[1].children.append(p[2])
        p[0] = p[1]

def p_class_member(p):
    'class_member : function_declaration'
    p[0] = p[1]  # Asumiendo que solo function_declaration se trata como un miembro de clase aquí.

def p_argument_list(p):
    '''
    argument_list : expression
                  | argument_list COMMA expression
    '''
    if len(p) == 2:
        p[0] = NodoArgumentList([p[1]])
    else:
        p[1].argumentos.append(p[3])
        p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None # No hacer nada
def p_expression_void(p):
    'expression : VOID expression'
    p[0] = NodoVoid(p[2])

def p_expression_in(p):
    'expression : expression IN expression'
    p[0] = NodoIn(p[1], p[3])

def p_expression_instanceof(p):
    'expression : expression INSTANCEOF expression'
    p[0] = NodoInstanceOf(p[1], p[3])

def p_expression_this(p):
    'expression : THIS'
    p[0] = NodoThis()

def p_expression_typeof(p):
    'expression : TYPEOF expression'
    p[0] = NodoTypeOf(p[2])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = NodoUMinus(p[2])

# Definir la regla para expresiones void
def p_expression_void(p):
    'expression_void : VOID expression'
    p[0] = NodoVoid(p[2])

# Definir la regla para expresiones "in"
def p_expression_in(p):
    'expression_in : expression IN expression'
    p[0] = NodoIn(p[1], p[3])

# Definir la regla para expresiones "instanceof"
def p_expression_instanceof(p):
    'expression_instanceof : expression INSTANCEOF expression'
    p[0] = NodoInstanceOf(p[1], p[3])

# Definir la regla para la expresión "this"
def p_expression_this(p):
    'expression_this : THIS'
    p[0] = NodoThis()

# Definir la regla para expresiones typeof
def p_expression_typeof(p):
    'expression_typeof : TYPEOF expression'
    p[0] = NodoTypeOf(p[2])

# Definir la regla para expresiones unarias negativas
def p_expression_uminus(p):
    'expression_uminus : MINUS expression %prec UMINUS'
    p[0] = NodoUMinus(p[2])

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

def analizar_y_traducir(archivo):
    # Leer el contenido del archivo
    with codecs.open(archivo, "r", "utf-8") as fp:
        cadena = fp.read()

    # Analizar el contenido del archivo
    yacc.yacc()
    result = yacc.parse(cadena, debug=1)

    # Definir la ruta del archivo .dot en el directorio actual del script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dot_path = os.path.join(base_dir, 'graphvizthree.dot')

    # Escribir la salida en un archivo .dot
    with open(dot_path, 'w') as graphFile:
        graphFile.write(result.traducir())

    print("El programa traducido se guardó en \"{}\"".format(dot_path))

    # Retornar la ruta del archivo .dot
    return dot_path


