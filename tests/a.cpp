#include <any>
#include <cmath>
# include <iostream>

auto fib(std::any n) {
    int a = 0;
    int b = 1;
    for (int i = 0; i < 3; i++)
     {
        float a = 2 + b;
        float b = a + 1;
        int n = std::floor(a / b);

    }

    return a;
}

int main() {
    return 0;
}