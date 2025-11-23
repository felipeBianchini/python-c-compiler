def bubble_sort(numbers, n):
    aux = 0
    for i in range(n):
        for j in range(n - 1 - i):
            if numbers[j] > numbers[j + 1]:
                aux = numbers[j + 1]
                numbers[j + 1] = numbers[j]
                numbers[j] = aux
    return numbers

nums = [5, 1, 4, 2, 8]
print(bubble_sort(nums, 5))
