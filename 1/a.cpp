#include <iostream>
#include <cstring>

int digit(char c) {
    return (int)c - (int)'0';
}

int f(const char* digits) {
    size_t len = strlen(digits);
    int sum = 0;
    for ( size_t i=0; i < len; i++ ) {
        int d = digit(digits[i]);
        int nd = digit(digits[(i+1)%len]);
        if ( d == nd ) {
            sum += d;
        }
    }
    return sum;
}

int main(int argc, char** argv) {
    if ( argc != 2 ) {
        std::cout << "USAGE: a 1122" << std::endl;
    } else {
        std::cout << f(argv[1])<< std::endl;
    }
    return 0;
}
