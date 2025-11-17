#include <iostream>
#include <vector>

void bubbleSort(std::vector<int>& numbers) {
    int n = numbers.size();
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (numbers[j] > numbers[j + 1]) {
                std::swap(numbers[j], numbers[j + 1]);
            }
        }
    }
}

int main() {
    std::vector<int> nums = {5, 1, 4, 2, 8};

    bubbleSort(nums);

    for (int x : nums) {
        std::cout << x << " ";
    }
    return 0;
}
