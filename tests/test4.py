array = [1,2,3]
for i in array:
    print(i)
    if i == 0:
        break
for i in range(5+1):
    print(i)
n = 0
while n < 5:
    if n == 3:
        continue
    print(n)
    n += 1