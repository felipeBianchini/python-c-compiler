# Variables globales de diferentes tipos
contador = 0
pi = 3.14159
nombre_usuario = "Alice"
activo = True
vacio = None

# Listas, tuplas, sets y diccionarios
numeros = [1, 2, 3, 4, 5]
coordenadas = (10, 20)
unicos = {1, 2, 3}
persona = {
    "nombre": "Bob",
    "edad": 30,
    "ciudad": "Madrid"
}

# Operaciones aritméticas complejas
resultado1 = (10 + 5) * 2
resultado2 = pi * 2
resultado3 = contador + 100

# Operaciones lógicas y relacionales
es_mayor = resultado1 > 50
es_valido = activo and es_mayor
comparacion = pi == 3.14

# Función simple sin parámetros
def saludar():
    mensaje = "Hola Mundo"
    print(mensaje)
    return mensaje

def sumar(a, b, c):
    total = a + b + c
    return total

def calcular_area(base, altura):
    area = base * altura
    perimetro = 2 * (base + altura)
    return area

def fibonacci(n):
    if n <= 1:
        return n
    else:
        fib1 = fibonacci(n - 1)
        fib2 = fibonacci(n - 2)
        return fib1 + fib2

# Bucle for simple
for i in range(10):
    cuadrado = i * i
    print(cuadrado)

# Bucle while
temp = 0
while temp < 5:
    temp = temp + 1
    print(temp)

# Condicional if-elif-else
valor = 15
if valor > 20:
    categoria = "Alto"
    print(categoria)
elif valor > 10:
    categoria = "Medio"
    print(categoria)
else:
    categoria = "Bajo"
    print(categoria)

# Llamadas a funciones
resultado_suma = sumar(10, 20, 30)
area_rect = calcular_area(5, 10)
fib_10 = fibonacci(10)
saludo = saludar()
besos = fibonacci(10)+ fibonacci(3)

# ERRORES INTENCIONALES ABAJO

# Error 1: Variable no declarada en uso
print(variable_no_declarada)

# Error 2: Asignación usando variable no declarada
resultado_err = x_inexistente + 10

# Error 3: Llamada a función no declarada
valor_err = funcion_que_no_existe(5, 10)

# Error 4: Uso de variable en operación antes de declararla
calculo = numero_secreto * 2

# Error 5: Append en variable no lista
texto = "hola"
texto.append("mundo")

# Error 6: Acceso a variable no declarada en condicional
if variable_misteriosa > 10:
    print("Mayor")

# Error 7: Variable no declarada en bucle
for i in range(10):
    resultado_loop = i + variable_no_def

# Error 8: Múltiples errores en una expresión
resultado_error = var1 + var2