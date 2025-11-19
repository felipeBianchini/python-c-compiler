#include <any>

std::any fibonacci(std::any n)
{
    int a = 2;
    bool b = true;
    std::any c = 2 + b + a;
    return fibonacci(n - 1) + fibonacci(n - 2);
}