#include <iostream>
#include <fstream>
#include <vector>
#include <numeric>
#include <iomanip>
#include <utility>
#include <algorithm>
#include <stdexcept>

std::string hex(int n) {
    char buffer[10];
	sprintf(buffer, "%02x", n);
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

	std::string get_dense_hash() const {
		std::string dense_hash;
		int i=0;
		int block = 0;
		for ( knot : knots ) {
			if ( i % 16 == 0 ) {
			    block = knot;
			} else {
			    block ^= knot;
				if ( i % 16 == 15 ) {
				    dense_hash.append(hex(block));
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

void read_formatted_file(std::istream& fin) {
	// read input file
    int knots_size = 0;
	fin >> knots_size;
	std::vector<int> twists;
	int twist;
	while ( fin >> twist ) twists.push_back(twist);
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
	char twist;
	std::vector<int> twists;
	std::string line;
	std::getline(fin, line);
	for ( char ch : line ) twists.push_back(static_cast<int>(ch));
	twists.push_back(17);
	twists.push_back(31);
	twists.push_back(73);
	twists.push_back(47);
	twists.push_back(23);
	
	int knots_size = 256;

	// verify we've read the input correctly
	std::cout << "knots size: " << knots_size << "\ntwists: ";
	for ( m : twists ) std::cout << m << ",";
	std::cout << std::endl;

	KnottedLoop knots(knots_size);
	knots.many_twists(twists, 64);
	std::cout << "sparse hash:\n";
	knots.dump(std::cout);
	std::cout << "check hash: " << knots.get_hash() << std::endl;
	std::cout << "dense hash: \"" << knots.get_dense_hash() << "\"" << std::endl;

	fin.close();
	return 0;
}


