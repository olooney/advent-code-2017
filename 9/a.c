#include <stdio.h>
#include <stdlib.h>

const size_t BUFFER_SIZE= 1024*1024;

int main(int argc, char** argv) {
    FILE* fin = stdin;

    if ( argc >= 2 ) {
        fin = fopen(argv[1], "r");
    }

    // lines come in pairs.
    // the first line is the actual input...
    char* line = (char*)malloc(BUFFER_SIZE);
    size_t buffer_length = BUFFER_SIZE;
    int bytes_read = getline(&line, &buffer_length, fin);
    line[bytes_read-1] = '\0'; // strip off the trailing newline
    printf("read %d bytes from stream: \"%s\"\n", bytes_read, line);

    // the next line contains only a single integer, the expected score.
    int expected_score = 0;
    char newline;
    scanf("%d%c", &expected_score, &newline);
    if ( newline != '\n' ) {
        fprintf(stderr, "unexpected character while reading expected score.");
    }
    printf("expected score is: %d\n", expected_score);

    // clean up
    free(line);
    if ( fin != stdin ) {
        fclose(fin);
    }

    return 0;
}

