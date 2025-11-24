#include<any>
#include<cmath>
#include<iostream>
#include<vector>
#include<map>
#include "utilities.hpp"

auto bubble_sort(std::any numbers, std::any n) {
    int aux = 0;
    for (int i = 0; i < std::any_cast<int>(n); i++) {
        for (int j = 0; j < std::any_cast<int>(n) - 1 - i; j++) {
            if (std::any_cast<int>(std::any_cast<std::vector<std::any>>(numbers)[j]) > std::any_cast<int>(std::any_cast<std::vector<std::any>>(numbers)[j + 1])) {
                aux = std::any_cast<int>(std::any_cast<std::vector<std::any>>(numbers)[j + 1]);
                std::any_cast<std::vector<std::any>&>(numbers)[j + 1] = std::any_cast<int>(std::any_cast<std::vector<std::any>>(numbers)[j]);
                std::any_cast<std::vector<std::any>&>(numbers)[j] = aux;

            }

        }

    }

    return numbers;
}


int main() {
    std::vector<std::any> nums = {5, 1, 4, 2, 8};
    std::cout << bubble_sort(nums, 5) << std::endl;
    return 0;
}