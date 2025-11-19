def fibonacci(n):
    a = 2
    b = True
    c = 2 + b + a
    return fibonacci(n - 1) + fibonacci(n - 2)
