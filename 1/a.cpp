#include <iostream>
#include <cstring>

int digit(char c) {
    return (int)c - (int)'0';
}

int f(const char* digits, int offset=1) {
    size_t len = strlen(digits);
    int sum = 0;
    for ( size_t i=0; i < len; i++ ) {
        int d = digit(digits[i]);
        int nd = digit(digits[(i+offset)%len]);
        if ( d == nd ) {
            sum += d;
        }
    }
    return sum;
}

int g(std::string digits) {
    int sum = 0;

    if ( digits.empty() ) return 0;

    digits.push_back(digits[0]);
    int prev = 0;
    int current = digit(digits[0]);
    auto second = ++digits.begin();

    for ( auto iter = second; iter != digits.end(); iter++ ) {
        prev = current;
        current = digit(*iter);
        if ( prev == current ) {
            sum += prev;
        }
        
    }
    return sum;
}

int main(int argc, char** argv) {
    if ( argc != 2 ) {
        std::cout << "USAGE: a 1122" << std::endl;
    } else {
        std::cout << f(argv[1], strlen(argv[1])/2)<< std::endl;
    }
    return 0;
}
