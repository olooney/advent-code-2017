#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <set>
#include <algorithm>


using Banks = std::vector<int>;

int balance(Banks& banks);
std::ostream& operator<<(std::ostream& out, const Banks& banks);

int main(int argc, char* argv[]) {

    // validate args
    if ( argc < 2 ) {
        std::cout << "USAGE: a.out FILE" << std::endl;
        return 0;
    }

    std::ifstream fin(argv[1]);
    if ( not fin.is_open() ) {
        std::cout << "file \"" << argv[1] << "\" not found." << std::endl;
        return 1;
    }

    // read in the full contents of the file.
    std::istream_iterator<int> begin(fin), end;
    std::vector<int> banks(begin, end);

    // compute the number of cycles before the first repeated state.
    int cycles = balance(banks);
    std::cout << cycles << std::endl;

    // compute the number of cycles from repeated state to repeated state.
    int loop_cycles = balance(banks);
    std::cout << loop_cycles << std::endl;

    return 0;
}

int balance(Banks& banks) {
    std::set<Banks> visited_states;
    
    int cycles = 0;
    while ( visited_states.find(banks) == visited_states.end() ) {
        //std::cerr << banks;

        // bookkeeping 
        visited_states.insert(banks);
        cycles++;

        // redistribute
        auto fullest_bank = std::max_element(banks.begin(), banks.end());
        auto iter_bank = fullest_bank;
        int blocks = *fullest_bank;
        // std::cerr << "fullest bank index=" << iter_bank - banks.begin() << " blocks=" << blocks << std::endl;
        *fullest_bank = 0;
        while ( blocks > 0 ) {
            iter_bank++;
            if ( iter_bank == banks.end() ) iter_bank = banks.begin();
            (*iter_bank)++;
            blocks--;
        }
    }
    // std::cerr << banks;
    return cycles;
}

std::ostream& operator<<(std::ostream& out, const Banks& banks) {
    for ( auto bank : banks ) {
        out << bank << "\t";
    }
    out << std::endl;
}
