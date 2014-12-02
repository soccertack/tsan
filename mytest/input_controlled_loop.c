#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <sanitizer/dfsan_interface.h>

dfsan_label globalInputLabel;
int global3;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Need loop input argument\n");
        return 0;
    }
    globalInputLabel = dfsan_create_label("globalInputLabel", 0);
    dfsan_set_label(globalInputLabel, &argv, argc);
    printf("Begin\n");

    int inputLoop = atoi(argv[1]);
    printf("InputLoop address is %p %d\n", &inputLoop, inputLoop);
    int a = 0;

    // bb true does not have calls or loops
    for(a = 0; a < inputLoop; a++) {
        printf("till to go: %d\n", inputLoop-a);
    }
    printf("inputLoop is: %d\n", inputLoop);

    printf("End\n");
    return 0;
}
