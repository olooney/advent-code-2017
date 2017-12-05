#include<iostream>
#include<vector>

void dump(std::vector<int> mem, int pc) {
	int i = 0;
    for ( int m : mem ) {
        if ( pc == i ) std::cout << '(';
		else std::cout << ' ';

		std::cout << m;

        if ( pc == i ) std::cout << ')';
		else std::cout << ' ';
		i++;
	}
	std::cout << std::endl;
}

int jmp(std::vector<int> mem) {
    int pc = 0;
	int steps = 0;
	int memsize = mem.size();

	while ( pc >=0 and pc < memsize ) {
		// dump(mem, pc);
		int offset = mem[pc];

        // if the offset is three or more, decrease it by one.
        // otherwise, increase it by 1 as before.
        if ( offset >= 3 ) {
            mem[pc]--;
        } else {
            mem[pc]++;
        }

		pc += offset;
        steps++;
	}
	return steps;
}

int main() {
    // read from stdin
	std::vector<int> mem;
    int m;
	while ( std::cin >> m ) {
		mem.push_back(m);
	}

	int steps = jmp(mem);
	std::cout << steps << std::endl;

	return 0;
}
