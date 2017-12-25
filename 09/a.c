#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const size_t BUFFER_SIZE= 1024*1024;
int test_two_lines(FILE* fin);
int score_one_line(FILE* fin);
int score_string(const char* stream);

int main(int argc, char** argv) {
    FILE* fin = stdin;

    if ( argc >= 2 ) {
        if ( strncmp(argv[1], "test", 4) == 0 ) {
            fin = fopen(argv[1], "r");
            printf("begining tests...\n");
            while ( test_two_lines(fin) == 0 );
            printf("\ntests complete.\n");
            fclose(fin);
            return 0;
        } else {
            fin = fopen(argv[1], "r");
            int score = score_one_line(fin);
            printf("%d\n", score);
        }
    }

    // global clean-up
    if ( fin != stdin ) {
        fclose(fin);
    }

    return 0;
}

int score_one_line(FILE* fin) {
    // lines come in pairs.
    // the first line is the actual input...
    char* line = (char*)malloc(BUFFER_SIZE);
    size_t buffer_length = BUFFER_SIZE;
    int bytes_read = getline(&line, &buffer_length, fin);
    if ( bytes_read == -1 ) {
        free(line);
        return -1;
    }
    line[bytes_read-1] = '\0'; // strip off the trailing newline
    printf("read %d bytes from stream: \"%s\"\n", bytes_read, line);

    int score = score_string(line);

    // clean up
    free(line);

    return score;
}

int test_two_lines(FILE* fin) {
    // lines come in pairs.
    // the first line is the actual input...
    int score = score_one_line(fin);
    if ( score == -1 ) return -1;

    // the next line contains only a single integer, the expected score.
    int expected_score = 0;
    char newline = '\0';
    fscanf(fin, "%d%c", &expected_score, &newline);
    if ( newline != '\n' ) {
        fprintf(stderr, "unexpected character while reading expected score.");
    }
    printf("expected score is: %d\n", expected_score);

    // compare scores and report success/failure
    if ( score != expected_score ) {
        printf("FAILED! Actual score %d does not match expected score %d!\n", score, expected_score);
    } else {
        printf("passed\n");
    }

    return  0;
}

int score_string(const char* input) {
    const char escape = '!';
    const char begin_group = '{';
    const char end_group = '}';
    const char begin_garbage = '<';
    const char end_garbage = '>';

    int score = 0;
    int depth = 0;
    const char* pc = input;

    const char* GARBAGE_MODE = "Garbage";
    const char* GROUP_MODE= "Group";
    const char* mode = GROUP_MODE;

    while ( *pc != '\0'  ) {
        if ( *pc == escape ) {
            pc++;
        } else if ( mode == GROUP_MODE ) {
            if ( *pc == begin_group ) {
                depth++;
                score += depth;
            } else if ( *pc == end_group ) {
                depth--;
                if ( depth < 0 ) {
                    fprintf(stderr, "ILLEGAL DEPTH!\n");
                    return -1;
                }
            } else if ( *pc == begin_garbage ) {
                mode = GARBAGE_MODE;
            }
        } else if ( mode == GARBAGE_MODE ) {
            if ( *pc == end_garbage ) {
                mode = GROUP_MODE;
            }
        } else {
            fprintf(stderr, "ILLEGAL MODE!\n");
            return -1;
        }
        pc++;
    }

    if ( depth != 0 ) {
        fprintf(stderr, "UNCLOSED GROUP!\n");
        return -1;
    }

    return score;
}

