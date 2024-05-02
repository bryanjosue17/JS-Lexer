# -*- coding: utf-8 -*-
class Nodo(object):
    def __init__(self, tipo, hijos=None, hoja=None):
        self.tipo = tipo
        self.hijos = [self.asegurar_es_nodo(h) for h in (hijos if hijos is not None else [])]
        self.hoja = hoja

    def asegurar_es_nodo(self, item):
        if isinstance(item, Nodo):
            return item
        elif isinstance(item, list):
            return [self.asegurar_es_nodo(h) for h in item]
        elif item is None:
            print("Error: Se intentó agregar un valor None como un nodo")
            return Nodo("Error", None, "NoneType")
        else:
            return NodoTerminal("Literal", item)

    def traducir(self, es_raiz=True):
        if self is None:
            print("Intento de traducir un objeto None")
            return ""
        txt = ""
        if es_raiz:
            txt += "digraph G {\n"
        txt += "\t{0} [label=\"{1}:{2}\"];\n".format(id(self), self.tipo, self.hoja if self.hoja else '')
        for hijo in (self.hijos if self.hijos is not None else []):
            if hijo is not None:
                txt += "\t{0} -> {1};\n".format(id(self), id(hijo))
                txt += hijo.traducir(es_raiz=False)
        if es_raiz:
            txt += "}"
        return txt
    
class NodoPrograma(Nodo):
    def __init__(self, hijos=None):
        super(NodoPrograma, self).__init__("Programa", hijos)

class NodoListaDeclaraciones(Nodo):
    def __init__(self, hijos=None):
        super(NodoListaDeclaraciones, self).__init__("ListaDeclaraciones", hijos)

class NodoDeclaracionVariable(Nodo):
    def __init__(self, tipo, identificador, expresion=None):
        expresion_nodo = self.asegurar_es_nodo(expresion)
        super(NodoDeclaracionVariable, self).__init__("DeclaracionVariable", [expresion_nodo], "{} {}".format(tipo, identificador))


class NodoFuncion(Nodo):
    def __init__(self, nombre, parametros, cuerpo):
        super(NodoFuncion, self).__init__("Funcion", [parametros, cuerpo], nombre)

class NodoControlFlujo(Nodo):
    def __init__(self, tipo, condicion, cuerpo, alternativo=None):
        children = [condicion, cuerpo] + ([alternativo] if alternativo else [])
        super(NodoControlFlujo, self).__init__(tipo, children)

class NodoExpresionBinaria(Nodo):
    def __init__(self, operador, izquierdo, derecho):
        super(NodoExpresionBinaria, self).__init__("ExpresionBinaria", [izquierdo, derecho], operador)

class NodoExpresionUnaria(Nodo):
    def __init__(self, operador, operando):
        super(NodoExpresionUnaria, self).__init__("ExpresionUnaria", [operando], operador)

class NodoTerminal(Nodo):
    def __init__(self, tipo, valor):
        super(NodoTerminal, self).__init__(tipo, hoja=valor)

class NodoBloque(Nodo):
    def __init__(self, declaraciones):
        super(NodoBloque, self).__init__("Bloque", declaraciones)

class NodoSentenciaControl(Nodo):
    def __init__(self, tipo, condicion, cuerpo):
        super(NodoSentenciaControl, self).__init__(tipo, [condicion, cuerpo])

class NodoSentencia(Nodo):
    def __init__(self, tipo, hijo=None):
        super(NodoSentencia, self).__init__(tipo, [hijo] if hijo else [])

class NodoThrow(Nodo):
    def __init__(self, expresion):
        super(NodoThrow, self).__init__("Throw", [expresion])

class NodoTry(Nodo):
    def __init__(self, bloque_try, bloque_catch=None, bloque_finally=None):
        children = [bloque_try] + ([bloque_catch] if bloque_catch else []) + ([bloque_finally] if bloque_finally else [])
        super(NodoTry, self).__init__("Try", children)

class NodoCatch(Nodo):
    def __init__(self, identificador, bloque):
        super(NodoCatch, self).__init__("Catch", [bloque], identificador)

class NodoFinally(Nodo):
    def __init__(self, bloque):
        super(NodoFinally, self).__init__("Finally", [bloque])

class NodoSwitch(Nodo):
    def __init__(self, expresion, casos, caso_default=None):
        hijos = [casos] + ([caso_default] if caso_default else [])
        super(NodoSwitch, self).__init__("Switch", hijos, hoja=expresion)

class NodoCase(Nodo):
    def __init__(self, expresion, sentencias):
        super(NodoCase, self).__init__("Case", [sentencias], hoja=expresion)

class NodoDefault(Nodo):
    def __init__(self, sentencias):
        super(NodoDefault, self).__init__("Default", [sentencias])

class NodoWith(Nodo):
    def __init__(self, expresion, sentencia):
        super(NodoWith, self).__init__("With", [expresion, sentencia])

class NodoDebugger(Nodo):
    def __init__(self):
        super(NodoDebugger, self).__init__("Debugger")

class NodoImport(Nodo):
    def __init__(self, identificador):
        super(NodoImport, self).__init__("Import", hoja=identificador)

class NodoExport(Nodo):
    def __init__(self, identificador):
        super(NodoExport, self).__init__("Export", hoja=identificador)

class NodoClassDeclaration(Nodo):
    def __init__(self, nombre, cuerpo_clase):
        super(NodoClassDeclaration, self).__init__("ClassDeclaration", [cuerpo_clase], nombre)

class NodoFunctionCall(Nodo):
    def __init__(self, identificador, argumentos):
        super(NodoFunctionCall, self).__init__("FunctionCall", [argumentos], identificador)

class NodoArrayAccess(Nodo):
    def __init__(self, identificador, indice):
        super(NodoArrayAccess, self).__init__("ArrayAccess", [indice], identificador)

class NodoObjectAccess(Nodo):
    def __init__(self, objeto, propiedad):
        super(NodoObjectAccess, self).__init__("ObjectAccess", hoja="{}.{}".format(objeto, propiedad))

class NodoBlock(Nodo):
    def __init__(self, declaraciones):
        super(NodoBlock, self).__init__("Block", declaraciones)

class NodoCatchClause(Nodo):
    def __init__(self, identificador, bloque):
        super(NodoCatchClause, self).__init__("CatchClause", [bloque], identificador)

class NodoFinallyClause(Nodo):
    def __init__(self, bloque):
        super(NodoFinallyClause, self).__init__("FinallyClause", [bloque])

class NodoNewExpression(Nodo):
    def __init__(self, tipo, identificador):
        super(NodoNewExpression, self).__init__("NewExpression", hoja="{} {}".format(tipo, identificador))

class NodoDeleteExpression(Nodo):
    def __init__(self, expresion):
        super(NodoDeleteExpression, self).__init__("DeleteExpression", [expresion])

class NodoDebuggerStatement(Nodo):
    def __init__(self):
        super(NodoDebuggerStatement, self).__init__("DebuggerStatement")

class NodoOptParamList(Nodo):
    def __init__(self, parametros):
        super(NodoOptParamList, self).__init__("OptParamList", parametros)

class NodoCompoundStatement(Nodo):
    def __init__(self, declaraciones):
        super(NodoCompoundStatement, self).__init__("CompoundStatement", declaraciones)

class NodoClassBody(Nodo):
    def __init__(self, elementos):
        super(NodoClassBody, he).__init__("ClassBody", elementos)

class NodoArgumentList(Nodo):
    def __init__(self, argumentos=None):
        super(NodoArgumentList, self).__init__("ListaArgumentos",)
        self.argumentos = [self.asegurar_es_nodo(arg) for arg in (argumentos if argumentos is not None else [])]

    def traducir(self, es_raiz=False):
        txt = ""
        for arg in self.argumentos:
            txt += arg.traducir(es_raiz=False)
        return txt

class NodoVoid(Nodo):
    def __init__(self, expresion):
        super(NodoVoid, self).__init__("Void", [expresion])

class NodoIn(Nodo):
    def __init__(self, izquierdo, derecho):
        super(NodoIn, self).__init__("In", [izquierdo, derecho])

class NodoInstanceOf(Nodo):
    def __init__(self, izquierdo, derecho):
        super(NodoInstanceOf, self).__init__("InstanceOf", [izquierdo, derecho])

class NodoThis(Nodo):
    def __init__(self):
        super(NodoThis, self).__init__("This")

class NodoTypeOf(Nodo):
    def init__(self, expresion):
        super(NodoTypeOf, self).__init__("TypeOf", [expresion])

class NodoUMinus(Nodo):
    def __init__(self, expresion):
        super(NodoUMinus, self).__init__("UMinus", [expresion])
