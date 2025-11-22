def fib(n):
    a = 0
    b = 1
    for i in range(3):
        a = 2 + b
        b = a + 1
        n = a // b
    return a
