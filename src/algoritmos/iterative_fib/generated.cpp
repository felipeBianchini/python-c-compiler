#include<any>
#include<cmath>
#include<iostream>
#include<vector>
#include<map>
#include "utilities.hpp"

auto fib(std::any n) {
    int a = 0;
    int b = 1;
    int c = 0;
    if (std::any_cast<int>(n) == 0) {
        return 0;
    }
    else if (std::any_cast<int>(n) == 1) {
        return 1;
    }
    for (int i = 0; i < std::any_cast<int>(n); i++) {
        c = a + b;
        b = a;
        a = c;

    }

    return a;
}


int main() {
    for (int i = 0; i < 10; i++) {
        std::cout << fib(i) << std::endl;

    }
    return 0;
}