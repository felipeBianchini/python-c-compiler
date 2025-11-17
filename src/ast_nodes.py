"""
Definición de nodos del AST para el transpilador Python a C++
"""

class ASTNode:
    def __init__(self):
        self.parent = None
    
    def children(self):
        return []
    
    def set_parent(self, node):
        if node is not None:
            node.parent = self

    def accept(self, listener):
        # enter rule
        method = getattr(listener, f"enter_{self.__class__.__name__}", None)
        if method:
            method(self)

        # recorrer hijos
        for child in self.children():
            if child:
                child.accept(listener)

        # exit rule
        method = getattr(listener, f"exit_{self.__class__.__name__}", None)
        if method:
            method(self)


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class FunctionDef(ASTNode):
    def __init__(self, name, params, body, lineno=0):
        self.name = name
        self.params = params
        self.body = body
        self.lineno = lineno

class Return(ASTNode):
    def __init__(self, value, lineno=0):
        self.value = value
        self.lineno = lineno

class Assignment(ASTNode):
    def __init__(self, target, value, lineno=0):
        self.target = target
        self.value = value
        self.lineno = lineno

class If(ASTNode):
    def __init__(self, condition, then_body, elif_parts, else_body, lineno=0):
        self.condition = condition
        self.then_body = then_body
        self.elif_parts = elif_parts
        self.else_body = else_body
        self.lineno = lineno

class While(ASTNode):
    def __init__(self, condition, body, lineno=0):
        self.condition = condition
        self.body = body
        self.lineno = lineno

class For(ASTNode):
    def __init__(self, target, iterable, body, lineno=0):
        self.target = target
        self.iterable = iterable
        self.body = body
        self.lineno = lineno

class FunctionCall(ASTNode):
    def __init__(self, name, args, lineno=0):
        self.name = name
        self.args = args
        self.lineno = lineno

class BinaryOp(ASTNode):
    def __init__(self, left, op, right, lineno=0):
        self.left = left
        self.op = op
        self.right = right
        self.lineno = lineno

class UnaryOp(ASTNode):
    def __init__(self, op, operand, lineno=0):
        self.op = op
        self.operand = operand
        self.lineno = lineno

class Identifier(ASTNode):
    def __init__(self, name, lineno=0):
        self.name = name
        self.lineno = lineno

class Literal(ASTNode):
    def __init__(self, value, type_name, lineno=0):
        self.value = value
        self.type_name = type_name
        self.lineno = lineno

class ExpressionStatement(ASTNode):
    def __init__(self, expression, lineno=0):
        self.expression = expression
        self.lineno = lineno

class Pass(ASTNode):
    def __init__(self, lineno=0):
        self.lineno = lineno

class Break(ASTNode):
    def __init__(self, lineno=0):
        self.lineno = lineno

class Continue(ASTNode):
    def __init__(self, lineno=0):
        self.lineno = lineno
