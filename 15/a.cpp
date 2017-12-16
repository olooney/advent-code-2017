#include <iostream>
#include <iomanip>

class Generator {
    long value;
	long factor;
	long modulo;
	long multiple;
public:
    Generator(long seed, long factor, long multiple=1, long modulo=2147483647L):
		value(seed), factor(factor), modulo(modulo), multiple(multiple) { } 

	long generate() {
		do {
			value = (value * factor) % modulo;
		} while ( value % multiple != 0 );
		return value;
	}
};

bool judge(long x, long y) {
	const static long MASK = (1 << 16) -1;
    return (x & MASK) == (y & MASK);
}

int main() {

	// test input
	//Generator genA{65L, 16807L, 4L};
	//Generator genB{8921L, 48271L, 8L};

	// real input
	Generator genA{679L, 16807L, 4L};
	Generator genB{771L, 48271L, 8L};

	long matches = 0;
	const long N = static_cast<long>(5e6);
	const long M = static_cast<long>(1e6);
	//const long N = 1056;
	//const long M = 1;

	for ( long i=0; i<N; i++ ) {
		long a = genA.generate();
		long b = genB.generate();
		bool judgement = judge(a, b);
		if ( judgement ) matches++;
		if ( i % M == 0 ) { 
			std::cout << std::setw(20) << a << "\t" << std::setw(20) << b << "\t" << matches << std::endl;
		}
	}
	std::cout << "matches: " << matches << std::endl;

    return 0;
}
