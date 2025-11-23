c = 0
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

c = 1 + 2
for i in range(10):
    print(fib(i))
