#include<iostream>
#include<string>
#include<sstream>
#include<vector>
#include<algorithm>
#include<utility>
#include<tuple>

template<class T>
std::vector<T> parse_line(std::string line) {
    std::istringstream linestream(line);
    std::vector<T> numbers{
            std::istream_iterator<T>{linestream},
            std::istream_iterator<T>{}
    };
    return numbers;
}

template<typename T>
std::pair<T, T> find_divisible_pair(std::vector<T> numbers) {
    std::sort(numbers.rbegin(), numbers.rend()); 
    size_t len = numbers.size();

    for ( auto i=numbers.begin(); i != numbers.end(); i++ ) {
        T n = *i;
        T half_n = n/2;
        for ( auto j=numbers.end()-1; j > i; j-- ) {
            T m = *j;
            if ( m > half_n ) break;
            if ( n % m == 0 ) {
                return {n, m};
            }
        }
    }
    return {0, 0};
}

int main() {
    std::string line;
    int checksum = 0;
    int lineno = 0;
    while ( getline(std::cin, line) ) {
        lineno++;
        auto numbers = parse_line<int>(line);
        int n, m;
        std::tie(n, m) = find_divisible_pair(numbers);
        if ( m == 0 ) {
            std::cerr << "no evenly divisible pair found on line " << lineno << std::endl;
            return 1;
        }
        checksum += n/m;

        // for ( int n : numbers ) std::cout << n << ',';
        // std::cout << m << " divides " << n;
        // std::cout << std::endl;
    }

    std::cout << checksum << std::endl;

    return 0;
}
