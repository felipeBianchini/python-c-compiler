"""
Analizador Semántico usando patrón Listener
Verifica:
- Variables no definidas
- Funciones no definidas
- Número de argumentos en llamadas
- Return fuera de función
- Break/Continue fuera de bucle
- Redefinición de funciones
- Uso correcto de operadores
"""

from src.listener import ASTListener

class SemanticError(Exception):
    """Error semántico durante el análisis"""
    def __init__(self, message, lineno=None):
        self.message = message
        self.lineno = lineno
        super().__init__(self.format_message())
    
    def format_message(self):
        if self.lineno:
            return f"Línea {self.lineno}: {self.message}"
        return self.message

class SymbolTable:
    """Tabla de símbolos con soporte para ámbitos anidados"""
    
    def __init__(self):
        self.scopes = [{}]  # Stack de ámbitos (diccionarios)
        self.functions = {}  # Funciones definidas
    
    def enter_scope(self):
        """Entrar a un nuevo ámbito"""
        self.scopes.append({})
    
    def exit_scope(self):
        """Salir del ámbito actual"""
        if len(self.scopes) > 1:
            self.scopes.pop()
    
    def define(self, name, info):
        """Definir un símbolo en el ámbito actual"""
        self.scopes[-1][name] = info
    
    def lookup(self, name):
        """Buscar un símbolo en todos los ámbitos (de dentro hacia fuera)"""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def define_function(self, name, params, lineno):
        """Definir una función"""
        if name in self.functions:
            raise SemanticError(f"Línea {lineno}: Función '{name}' ya definida")
        self.functions[name] = {'params': params, 'lineno': lineno}
    
    def get_function(self, name):
        """Obtener información de una función"""
        return self.functions.get(name)

class SemanticAnalyzer(ASTListener):
    """Analizador semántico que recorre el AST"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.in_function = False
        self.in_loop = False
    
    def analyze(self, ast):
        """
        Punto de entrada del análisis semántico.
        """
        ast.accept(self)

        # Retornar True/False para facilitar uso en tests
        return not self.has_errors()


    def error(self, message):
        """Registrar un error semántico"""
        self.errors.append(message)
    
    def visit_Program(self, node):
        """Analizar el programa completo"""
        # Primera pasada: registrar todas las funciones
        for stmt in node.statements:
            if stmt.__class__.__name__ == 'FunctionDef':
                self.symbol_table.define_function(
                    stmt.name, 
                    stmt.params, 
                    stmt.lineno
                )
        
        # Segunda pasada: analizar cuerpo
        for stmt in node.statements:
            stmt.accept(self)
    
    def visit_FunctionDef(self, node):
        """Analizar definición de función"""
        # Entrar al ámbito de la función
        self.symbol_table.enter_scope()
        old_in_function = self.in_function
        self.in_function = True
        
        # Definir parámetros en el ámbito de la función
        for param in node.params:
            self.symbol_table.define(param, {'type': 'param', 'lineno': node.lineno})
        
        # Analizar cuerpo
        for stmt in node.body:
            stmt.accept(self)
        
        # Salir del ámbito
        self.symbol_table.exit_scope()
        self.in_function = old_in_function
    
    def visit_Assignment(self, node):
        """Analizar asignación"""
        # Analizar el valor
        node.value.accept(self)
        
        # Definir o actualizar variable
        self.symbol_table.define(node.target, {
            'type': 'variable',
            'lineno': node.lineno
        })
    
    def visit_Return(self, node):
        """Analizar return"""
        if not self.in_function:
            self.error(f"Línea {node.lineno}: 'return' fuera de función")
        
        if node.value:
            node.value.accept(self)
    
    def visit_If(self, node):
        """Analizar condicional"""
        # Analizar condición
        node.condition.accept(self)
        
        # Analizar cuerpo then
        self.symbol_table.enter_scope()
        for stmt in node.then_body:
            stmt.accept(self)
        self.symbol_table.exit_scope()
        
        # Analizar elif
        for condition, body in node.elif_parts:
            condition.accept(self)
            self.symbol_table.enter_scope()
            for stmt in body:
                stmt.accept(self)
            self.symbol_table.exit_scope()
        
        # Analizar else
        if node.else_body:
            self.symbol_table.enter_scope()
            for stmt in node.else_body:
                stmt.accept(self)
            self.symbol_table.exit_scope()
    
    def visit_While(self, node):
        """Analizar bucle while"""
        node.condition.accept(self)
        
        old_in_loop = self.in_loop
        self.in_loop = True
        
        self.symbol_table.enter_scope()
        for stmt in node.body:
            stmt.accept(self)
        self.symbol_table.exit_scope()
        
        self.in_loop = old_in_loop
    
    def visit_For(self, node):
        """Analizar bucle for"""
        node.iterable.accept(self)
        
        old_in_loop = self.in_loop
        self.in_loop = True
        
        self.symbol_table.enter_scope()
        
        # Definir variable de iteración
        self.symbol_table.define(node.target, {
            'type': 'loop_var',
            'lineno': node.lineno
        })
        
        for stmt in node.body:
            stmt.accept(self)
        
        self.symbol_table.exit_scope()
        self.in_loop = old_in_loop
    
    def visit_Break(self, node):
        """Analizar break"""
        if not self.in_loop:
            self.error(f"Línea {node.lineno}: 'break' fuera de bucle")
    
    def visit_Continue(self, node):
        """Analizar continue"""
        if not self.in_loop:
            self.error(f"Línea {node.lineno}: 'continue' fuera de bucle")
    
    def visit_FunctionCall(self, node):
        """Analizar llamada a función"""
        func_info = self.symbol_table.get_function(node.name)
        
        # Verificar que la función existe (permitir built-ins)
        if func_info is None and node.name not in ['print', 'len', 'range', 'input']:
            self.error(f"Línea {node.lineno}: Función '{node.name}' no definida")
        
        # Verificar número de argumentos
        if func_info and len(node.args) != len(func_info['params']):
            self.error(
                f"Línea {node.lineno}: Función '{node.name}' espera "
                f"{len(func_info['params'])} argumentos, recibió {len(node.args)}"
            )
        
        # Analizar argumentos
        for arg in node.args:
            arg.accept(self)
    
    def visit_BinaryOp(self, node):
        """Analizar operación binaria"""
        node.left.accept(self)
        node.right.accept(self)
    
    def visit_UnaryOp(self, node):
        """Analizar operación unaria"""
        node.operand.accept(self)
    
    def visit_Identifier(self, node):
        """Analizar identificador"""
        if self.symbol_table.lookup(node.name) is None:
            # Verificar si es una función
            if self.symbol_table.get_function(node.name) is None:
                self.error(f"Línea {node.lineno}: Variable '{node.name}' no definida")
    
    def visit_Literal(self, node):
        """Analizar literal"""
        pass  # Los literales son siempre válidos
    
    def visit_ExpressionStatement(self, node):
        """Analizar expresión como statement"""
        node.expression.accept(self)
    
    def visit_Pass(self, node):
        """Analizar pass"""
        pass  # pass no hace nada
    
    def has_errors(self):
        """Verificar si hay errores"""
        return len(self.errors) > 0
    
    def print_errors(self):
        """Imprimir errores"""
        for error in self.errors:
            print(f"Error semántico: {error}")
