#include <stdio.h>
#include <stdlib.h>

const size_t BUFFER_SIZE= 1024*1024;
int test_two_lines(FILE* fin);
int score_stream(const char* stream);

int main(int argc, char** argv) {
    FILE* fin = stdin;

    if ( argc >= 2 ) {
        fin = fopen(argv[1], "r");
    }

    while ( test_two_lines(fin) == 0 );

    printf("\ndone!\n");

    // global clean-up
    if ( fin != stdin ) {
        fclose(fin);
    }

    return 0;
}

int test_two_lines(FILE* fin) {
    // lines come in pairs.
    // the first line is the actual input...
    char* line = (char*)malloc(BUFFER_SIZE);
    size_t buffer_length = BUFFER_SIZE;
    int bytes_read = getline(&line, &buffer_length, fin);
    if ( bytes_read == -1 ) {
        free(line);
        return 1;
    }
    line[bytes_read-1] = '\0'; // strip off the trailing newline
    printf("read %d bytes from stream: \"%s\"\n", bytes_read, line);

    // the next line contains only a single integer, the expected score.
    int expected_score = 0;
    char newline = '\0';
    fscanf(fin, "%d%c", &expected_score, &newline);
    if ( newline != '\n' ) {
        fprintf(stderr, "unexpected character while reading expected score.");
    }
    printf("expected score is: %d\n", expected_score);

    int score = score_stream(line);
    if ( score != expected_score ) {
        printf("FAILED! Actual score %d does not match expected score %d for input \"%s\"!\n",
               score,
               expected_score,
               line);
    } else {
        printf("passed\n");
    }

    // clean up
    free(line);
    return  0;
}

int score_stream(const char* stream) {
    return 5;
}

