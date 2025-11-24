def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    res = fibonacci(n - 1) + fibonacci(n - 2)
    return res

for i in range(50):
    print(fibonacci(i))