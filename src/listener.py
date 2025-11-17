"""
Interfaz base para el patrón Listener
El patrón Listener (también conocido como Visitor) permite separar
los algoritmos de las estructuras de datos sobre las que operan.
"""

class ASTListener:
    """
    Clase base para los listeners del AST.
    Cada listener implementa métodos visit_* para cada tipo de nodo.
    """
    
    def generic_visit(self, node):
        """
        Método por defecto si no existe un visit específico.
        Puedes sobrescribir este método para manejar nodos desconocidos.
        """
        raise NotImplementedError(
            f"No se implementó el método visit_{node.__class__.__name__} "
            f"en {self.__class__.__name__}"
        )
    
    # ==================== Métodos visit para cada tipo de nodo ====================
    
    def visit_Program(self, node):
        """Visitar nodo Program (raíz del AST)"""
        pass
    
    def visit_FunctionDef(self, node):
        """Visitar definición de función"""
        pass
    
    def visit_Return(self, node):
        """Visitar sentencia return"""
        pass
    
    def visit_Assignment(self, node):
        """Visitar asignación de variable"""
        pass
    
    def visit_If(self, node):
        """Visitar sentencia if/elif/else"""
        pass
    
    def visit_While(self, node):
        """Visitar bucle while"""
        pass
    
    def visit_For(self, node):
        """Visitar bucle for"""
        pass
    
    def visit_FunctionCall(self, node):
        """Visitar llamada a función"""
        pass
    
    def visit_BinaryOp(self, node):
        """Visitar operación binaria (+, -, *, /, etc.)"""
        pass
    
    def visit_UnaryOp(self, node):
        """Visitar operación unaria (-, not, +)"""
        pass
    
    def visit_Identifier(self, node):
        """Visitar identificador (nombre de variable)"""
        pass
    
    def visit_Literal(self, node):
        """Visitar literal (número, string, bool)"""
        pass
    
    def visit_ExpressionStatement(self, node):
        """Visitar expresión como statement"""
        pass
    
    def visit_Pass(self, node):
        """Visitar sentencia pass"""
        pass
    
    def visit_Break(self, node):
        """Visitar sentencia break"""
        pass
    
    def visit_Continue(self, node):
        """Visitar sentencia continue"""
        pass


class CompositeListener(ASTListener):
    """
    Listener compuesto que permite ejecutar múltiples listeners
    en secuencia sobre el mismo AST.
    
    Útil cuando necesitas hacer múltiples pasadas de análisis.
    """
    
    def __init__(self, *listeners):
        """
        Inicializar con una lista de listeners.
        
        Ejemplo:
            semantic = SemanticAnalyzer()
            optimizer = ASTOptimizer()
            composite = CompositeListener(semantic, optimizer)
        """
        self.listeners = listeners
    
    def generic_visit(self, node):
        """Delegar la visita a todos los listeners"""
        for listener in self.listeners:
            node.accept(listener)
    
    # Sobrescribir todos los métodos visit para delegar
    def visit_Program(self, node):
        for listener in self.listeners:
            listener.visit_Program(node)
    
    def visit_FunctionDef(self, node):
        for listener in self.listeners:
            listener.visit_FunctionDef(node)
    
    def visit_Return(self, node):
        for listener in self.listeners:
            listener.visit_Return(node)
    
    def visit_Assignment(self, node):
        for listener in self.listeners:
            listener.visit_Assignment(node)
    
    def visit_If(self, node):
        for listener in self.listeners:
            listener.visit_If(node)
    
    def visit_While(self, node):
        for listener in self.listeners:
            listener.visit_While(node)
    
    def visit_For(self, node):
        for listener in self.listeners:
            listener.visit_For(node)
    
    def visit_FunctionCall(self, node):
        for listener in self.listeners:
            listener.visit_FunctionCall(node)
    
    def visit_BinaryOp(self, node):
        for listener in self.listeners:
            listener.visit_BinaryOp(node)
    
    def visit_UnaryOp(self, node):
        for listener in self.listeners:
            listener.visit_UnaryOp(node)
    
    def visit_Identifier(self, node):
        for listener in self.listeners:
            listener.visit_Identifier(node)
    
    def visit_Literal(self, node):
        for listener in self.listeners:
            listener.visit_Literal(node)
    
    def visit_ExpressionStatement(self, node):
        for listener in self.listeners:
            listener.visit_ExpressionStatement(node)
    
    def visit_Pass(self, node):
        for listener in self.listeners:
            listener.visit_Pass(node)
    
    def visit_Break(self, node):
        for listener in self.listeners:
            listener.visit_Break(node)
    
    def visit_Continue(self, node):
        for listener in self.listeners:
            listener.visit_Continue(node)


class PrintListener(ASTListener):
    """
    Listener de ejemplo que imprime el AST de forma indentada.
    Útil para debugging y visualización del árbol.
    """
    
    def __init__(self):
        self.indent_level = 0
    
    def _print(self, text):
        """Imprimir con indentación"""
        print("  " * self.indent_level + text)
    
    def visit_Program(self, node):
        self._print("Program:")
        self.indent_level += 1
        for stmt in node.statements:
            stmt.accept(self)
        self.indent_level -= 1
    
    def visit_FunctionDef(self, node):
        params = ", ".join(node.params)
        self._print(f"FunctionDef: {node.name}({params})")
        self.indent_level += 1
        for stmt in node.body:
            stmt.accept(self)
        self.indent_level -= 1
    
    def visit_Return(self, node):
        self._print("Return:")
        if node.value:
            self.indent_level += 1
            node.value.accept(self)
            self.indent_level -= 1
    
    def visit_Assignment(self, node):
        self._print(f"Assignment: {node.target} =")
        self.indent_level += 1
        node.value.accept(self)
        self.indent_level -= 1
    
    def visit_If(self, node):
        self._print("If:")
        self.indent_level += 1
        self._print("Condition:")
        self.indent_level += 1
        node.condition.accept(self)
        self.indent_level -= 1
        
        self._print("Then:")
        self.indent_level += 1
        for stmt in node.then_body:
            stmt.accept(self)
        self.indent_level -= 1
        
        for condition, body in node.elif_parts:
            self._print("Elif:")
            self.indent_level += 1
            self._print("Condition:")
            self.indent_level += 1
            condition.accept(self)
            self.indent_level -= 1
            for stmt in body:
                stmt.accept(self)
            self.indent_level -= 1
        
        if node.else_body:
            self._print("Else:")
            self.indent_level += 1
            for stmt in node.else_body:
                stmt.accept(self)
            self.indent_level -= 1
        
        self.indent_level -= 1
    
    def visit_While(self, node):
        self._print("While:")
        self.indent_level += 1
        node.condition.accept(self)
        for stmt in node.body:
            stmt.accept(self)
        self.indent_level -= 1
    
    def visit_For(self, node):
        self._print(f"For: {node.target} in")
        self.indent_level += 1
        node.iterable.accept(self)
        for stmt in node.body:
            stmt.accept(self)
        self.indent_level -= 1
    
    def visit_FunctionCall(self, node):
        self._print(f"FunctionCall: {node.name}")
        if node.args:
            self.indent_level += 1
            for arg in node.args:
                arg.accept(self)
            self.indent_level -= 1
    
    def visit_BinaryOp(self, node):
        self._print(f"BinaryOp: {node.op}")
        self.indent_level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.indent_level -= 1
    
    def visit_UnaryOp(self, node):
        self._print(f"UnaryOp: {node.op}")
        self.indent_level += 1
        node.operand.accept(self)
        self.indent_level -= 1
    
    def visit_Identifier(self, node):
        self._print(f"Identifier: {node.name}")
    
    def visit_Literal(self, node):
        self._print(f"Literal: {node.value} ({node.type_name})")
    
    def visit_ExpressionStatement(self, node):
        self._print("ExpressionStatement:")
        self.indent_level += 1
        node.expression.accept(self)
        self.indent_level -= 1
    
    def visit_Pass(self, node):
        self._print("Pass")
    
    def visit_Break(self, node):
        self._print("Break")
    
    def visit_Continue(self, node):
        self._print("Continue")
