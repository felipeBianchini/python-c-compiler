#include<any>
#include<cmath>
#include<iostream>
#include<vector>
#include<map>
auto fibonacci(std::any n) {
    if (std::any_cast<int>(n) == 0) {
        return 0;
    }
    else if (std::any_cast<int>(n) == 1) {
        return 1;
    }
    int res = fibonacci(std::any_cast<int>(n) - 1) + fibonacci(std::any_cast<int>(n) - 2);

    return res;
}


int main() {
    for (int i = 0; i < 10; i++) {
        std::cout << fibonacci(i) << std::endl;

    }
    return 0;
}