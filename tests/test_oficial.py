### PRUEBAS
def random_operation(a, b):
    c = a + b
    # Hi I'm a comment!
    return c + a * b + 2.6548

def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    elif n == 0:
        return n / 0
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def fibonacci_d(n):
    n_1 = 1
    n_2 = 1
    while (n_1 < n):
        new = n_1 + n_2
        n_2 = n_1
        n_1 = new
    return n_1

def iter_example():
    l = [1, 2.5, 3, "ho\nla", 5, "mundo"]
    it = iter(l)
    for i in l:
        print(next(it))
    return True

def map_ex():
    d = {
        "hola": "mundo",
        1: [1, 2, 3, 4, 5],
        "dict": {'adios': ':D'}
    }
    for k in d.keys():
        print(d[k])
    return "hola" + "mundo"

def default_ex(a='hola'):
    return a

def set_ex():
    a = {1, 2, "hola", 4, 5}
    return 2 in a

def tuple_ex():
    a = (5, 6, 'joseph')
    b = (1, 2, 'valverde')
    return a + b

def slices_ex():
    l = [1, 2, 3, 4, 5, 6, 7, 7, 8, 9]
    print(l[-2])
    print(l[1:-2])
    k = l[1:2] + l[-3:-4]
    return k

def string_ex():
    print("profe"[2:4])
    print("profe"[2:4] + "profe"[0:2] + "profe"[-1])

class TestClass:
    class_attr = "Soy un atributo de clase"

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def instance_method(self):
        print("Hola, soy {self.name} y mi valor es {self.value}")
        return self.value * 2

    def class_method(cls):
        print("Este es un método de clase, atributo: {cls.class_attr}")
        return cls.class_attr

    def static_method(x, y):
        print("Este es un método estático, x + y = {x + y}")
        return x + y

print(random_operation(5, 6))
print(fibonacci(4))
print(fibonacci_d(4))
print(iter_example())
print(map_ex())
print(default_ex())
print(tuple_ex())
print(set_ex())
print(slices_ex())
string_ex()

obj = TestClass("Felipe", 10)
print(obj.instance_method())
print(TestClass.class_method())
print(TestClass.static_method(3, 4))
