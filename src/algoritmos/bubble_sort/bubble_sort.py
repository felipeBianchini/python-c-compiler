def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers

nums = [5, 1, 4, 2, 8]
print(bubble_sort(nums))
