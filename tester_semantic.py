"""
Test para el parser minimalista
SOLO prueba las características requeridas en la especificación
"""

from src.lexer import Lexer
from src.parser import Parser
from src.semantic_analyzer import SemanticAnalyzer
from src.listener import PrintListener


def make_lexer(code):
    """Crea un lexer con cola de errores y lo carga con el código."""
    errors = []
    lexer = Lexer(errors=errors)
    lexer.build()
    lexer.input(code)
    return lexer, errors


def test_basic():
    """Test 1: Operaciones básicas"""
    print("="*70)
    print("TEST 1: Operaciones Básicas")
    print("="*70)
    
    code = """
x = 10
y = 20
z = x + y
print(z)
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)  # lexer ya viene inicializado
        if ast:
            print("✓ Parsing OK")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


def test_function():
    """Test 2: Función simple"""
    print("\n" + "="*70)
    print("TEST 2: Función Simple")
    print("="*70)
    
    code = """
def suma(a, b):
    resultado = a + b
    return resultado

x = suma(5, 10)
print(x)
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)
        if ast:
            print("✓ Parsing OK")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


def test_if_elif_else():
    """Test 3: Condicionales"""
    print("\n" + "="*70)
    print("TEST 3: Condicionales if/elif/else")
    print("="*70)
    
    code = """
x = 15

if x > 20:
    print(1)
elif x > 10:
    print(2)
else:
    print(3)
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)
        if ast:
            print("✓ Parsing OK")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


def test_while():
    """Test 4: While loop"""
    print("\n" + "="*70)
    print("TEST 4: Bucle While")
    print("="*70)
    
    code = """
x = 0
while x < 5:
    print(x)
    x = x + 1
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)
        if ast:
            print("✓ Parsing OK")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


def test_for():
    """Test 5: For loop"""
    print("\n" + "="*70)
    print("TEST 5: Bucle For con range()")
    print("="*70)
    
    code = """
for i in range(5):
    print(i)
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)
        if ast:
            print("✓ Parsing OK")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


def test_operators():
    """Test 6: Todos los operadores"""
    print("\n" + "="*70)
    print("TEST 6: Operadores Aritméticos, Relacionales y Lógicos")
    print("="*70)
    
    code = """
a = 10
b = 5

suma = a + b
resta = a - b
mult = a * b
div = a / b
mod = a % b

mayor = a > b
menor = a < b
igual = a == b
diferente = a != b

y = a > 0 and b < 10
o = a < 0 or b > 0
negacion = not igual
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)
        if ast:
            print("✓ Parsing OK")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


def test_dynamic_typing():
    """Test 7: Tipado dinámico"""
    print("\n" + "="*70)
    print("TEST 7: Tipado Dinámico")
    print("="*70)
    
    code = """
x = 10
print(x)
x = 3.14
print(x)
x = True
print(x)
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)
        if ast:
            print("✓ Parsing OK")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


def test_factorial():
    """Test 8: Factorial recursivo (caso completo)"""
    print("\n" + "="*70)
    print("TEST 8: Factorial Recursivo")
    print("="*70)
    
    code = """
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

resultado = factorial(5)
print(resultado)
"""
    
    print(code)
    
    lexer, errors = make_lexer(code)
    parser = Parser()
    
    try:
        ast = parser.parser.parse(code, lexer)
        if ast:
            print("✓ Parsing OK")
            
            # Visualizar AST
            print("\n--- AST ---")
            printer = PrintListener()
            ast.accept(printer)
            
            # Análisis semántico
            print("\n--- Análisis Semántico ---")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)
            analyzer.print_report()
        else:
            print("✗ Parsing FAILED")

        if errors:
            print("LEXER ERRORS:", errors)

    except Exception as e:
        print(f"✗ ERROR: {e}")


if __name__ == '__main__':
    
    test_basic()
    test_function()
    test_if_elif_else()
    test_while()
    test_for()
    test_operators()
    test_dynamic_typing()
    test_factorial()
