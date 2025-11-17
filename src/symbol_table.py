class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # pila de scopes

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, value):
        if name in self.scopes[-1]:
            raise Exception(f"Variable redeclarada: {name}")
        self.scopes[-1][name] = value
    
    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Variable no declarada: {name}")
