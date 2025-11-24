def fib(n):
    a = 0
    b = 1
    c = 0
    if n == 0:
        return 0
    elif n == 1:
        return 1
    for i in range(n):
        c = a + b
        b = a
        a = c
    return a

for i in range(50):
    print(fib(i))
