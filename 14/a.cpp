#include <iostream>
#include <functional>
#include <fstream>
#include <vector>
#include <numeric>
#include <iomanip>
#include <utility>
#include <algorithm>
#include <stdexcept>
#include <boost/lexical_cast.hpp>

using boost::lexical_cast;

std::string hex(int n) {
    char buffer[10];
	sprintf(buffer, "%02x", n);
	return std::string(buffer);  
}

std::string binary(int n) {
    char buffer[] = "00000000";

    int mask = 0x01;
    for ( int i=0; i<8; i++ ) {
        if ( n & mask ) buffer[7-i] = '1';
        mask <<= 1;
    }

	return std::string(buffer);  
}

std::string used(int n) {
    char buffer[] = "........";

    int mask = 0x01;
    for ( int i=0; i<8; i++ ) {
        if ( n & mask ) buffer[7-i] = '#';
        mask <<= 1;
    }

	return std::string(buffer);  
}

class KnottedLoop {
public:
	std::vector<int> knots;
	int position;
	int skip_size;
	
    KnottedLoop(int knots_size): knots(knots_size) {
		std::iota(knots.begin(), knots.end(), 0);
		position = 0;
		skip_size = 0;
	}

	void half_twist(int length) {
		int start = position;
	    int end = (start + length -1) % knots.size();
		// std::cout << "reversing range from " << start << " " << "to " << end << << "length=" << length << std::endl;
		for ( int i=0; i < length / 2; i++ ) {
			int left = (start + i) % knots.size();
			int right = (end - i + knots.size()) % knots.size();
			// std::cout << "swapping left: " << left << " " << "right: " << right << std::endl;
			std::swap(knots[left], knots[right]);
		}
		position = (position + length + skip_size) % knots.size();
		skip_size++;
	}

	void many_twists(std::vector<int> lengths, int repeat) {
	    for (int i=0; i < repeat; i++ ) {
			for ( int length : lengths ) {
				half_twist(length);
			}
		}
	}

	int get_hash() const {
		if ( knots.size() >= 2 ) {
			return knots[0] * knots[1];
		} else {
			throw std::runtime_error("knot loop is to short to hash!\n");
		}
	}

	std::string get_dense_hash( std::function<std::string(int)> serializer = hex ) const {
		std::string dense_hash;
		int i=0;
		int block = 0;
		for ( knot : knots ) {
			if ( i % 16 == 0 ) {
			    block = knot;
			} else {
			    block ^= knot;
				if ( i % 16 == 15 ) {
				    dense_hash.append(serializer(block));
					block = 0;
				}
			}
		    i++;
		}
		return dense_hash;
	}

	void dump(std::ostream& out, int length=0) {
		int index = 0;
		for ( auto knot : knots ) {
			if ( length > 0 && index == position ) out << "("; else out << " ";
			if ( index == position ) out << "["; else out << " ";
			out << std::setw(3) << knot;
			if ( index == position ) out << "]"; else out << " ";
			if ( length > 0 && index == (position + length-1) % knots.size() ) out << ")"; else out << " ";
			if ( index > 0 and (index+1) % 10 == 0 ) out << "\n";
			index++;
		}
		out << std::endl;
	}
	
};

std::string knot_hash(std::string line, std::function<std::string(int)> serializer=hex) {
	std::vector<int> twists;
	for ( char ch : line ) twists.push_back(static_cast<int>(ch));
	twists.push_back(17);
	twists.push_back(31);
	twists.push_back(73);
	twists.push_back(47);
	twists.push_back(23);
	
	KnottedLoop knots(256);
	knots.many_twists(twists, 64);
    return knots.get_dense_hash(serializer);
}

void read_formatted_file(std::istream& fin) {
	// read input file
    int knots_size = 0;
	fin >> knots_size;
	std::vector<int> twists;
	int twist;
	while ( fin >> twist ) twists.push_back(twist);
}

std::string read_raw_line(std::istream& fin) {
	std::string line;
	std::getline(fin, line);
    return line;
}

int main(int argc, char** argv) {

	// parse command line arguments
	if ( argc < 2 ) {
	    std::cout << "USAGE a.out FILENAME" << std::endl;
		return 0;
	}

	// open input file
	std::ifstream fin(argv[1]);
	if ( not fin.good() ) {
	    std::cerr << "unable to open input file \"" << argv[1] << "\"." << std::endl;
		return 1;
	}

    std::string line = read_raw_line(fin);
    std::cout << "input: \"" << line << "\"\n";

	fin.close();

    std::string disk = "";
    for ( int i=0; i<128; i++ ) {
        std::string row_id = line + "-" + lexical_cast<std::string>(i);
        std::cout << "row: \"" << row_id << "\"\t";
        auto hex_hash = knot_hash(row_id);
        std::cout << "knot_hash: " << hex_hash << "\t";
        auto disk_hash = knot_hash(row_id, used);
        disk += disk_hash;
        std::cout << disk_hash << std::endl;
    }

    size_t n_used = std::count(disk.begin(), disk.end(), '#');
    std::cout << "disk used: " << n_used << "/" << disk.size() << std::endl;

	return 0;
}


