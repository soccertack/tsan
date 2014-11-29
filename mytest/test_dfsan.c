#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sanitizer/dfsan_interface.h>
#include <assert.h>

int global3;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Need loop input argument\n");
        return 0;
    }

    dfsan_label input_label = dfsan_create_label("input", 0);
    dfsan_set_label(input_label, &argv, argc);

    /*int inputLoop = atoi(argv[1]);*/
    int inputLoop = (int)argv;
    int max = inputLoop;
    int a = 1000;

    // bb true does not have calls or loops
    if(max < a) {
        max = a;
        dfsan_label inputLoop_label = dfsan_get_label(max);
        if(dfsan_has_label(inputLoop_label, input_label)) {
            printf("max is tainted by input but should not\n");
            return 0;
        }
    } else {
        dfsan_label inputLoop_label = dfsan_get_label(max);
        if(!dfsan_has_label(inputLoop_label, input_label)) {
            printf("max is not tainted by input but should\n");
            return 0;
        }
    }
    return 0;
}
