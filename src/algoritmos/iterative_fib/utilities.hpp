#ifndef UTILITIES_HPP
#define UTILITIES_HPP

#include <iostream>
#include <vector>
#include <any>

// Sobrecarga para std::vector<int> (arrays normales)
std::ostream& operator<<(std::ostream& os, const std::vector<int>& vec) {
    os << "[";
    for (size_t i = 0; i < vec.size(); i++) {
        os << vec[i];
        if (i < vec.size() - 1) {
            os << ", ";
        }
    }
    os << "]";
    return os;
}

// Sobrecarga para std::vector<std::any>
std::ostream& operator<<(std::ostream& os, const std::vector<std::any>& vec) {
    os << "[";
    for (size_t i = 0; i < vec.size(); i++) {
        try {
            os << std::any_cast<int>(vec[i]);
        } catch (const std::bad_any_cast&) {
            try {
                os << std::any_cast<double>(vec[i]);
            } catch (const std::bad_any_cast&) {
                try {
                    os << std::any_cast<std::string>(vec[i]);
                } catch (const std::bad_any_cast&) {
                    os << "?";
                }
            }
        }
        if (i < vec.size() - 1) {
            os << ", ";
        }
    }
    os << "]";
    return os;
}

// Sobrecarga para std::any (intenta extraer y mostrar el contenido)
std::ostream& operator<<(std::ostream& os, const std::any& a) {
    try {
        os << std::any_cast<std::vector<std::any>>(a);
    } catch (const std::bad_any_cast&) {
        try {
            os << std::any_cast<std::vector<int>>(a);
        } catch (const std::bad_any_cast&) {
            try {
                os << std::any_cast<int>(a);
            } catch (const std::bad_any_cast&) {
                try {
                    os << std::any_cast<double>(a);
                } catch (const std::bad_any_cast&) {
                    try {
                        os << std::any_cast<std::string>(a);
                    } catch (const std::bad_any_cast&) {
                        os << "[any]";
                    }
                }
            }
        }
    }
    return os;
}

#endif // UTILITIES_HPP