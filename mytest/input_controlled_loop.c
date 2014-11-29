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
    printf("inputLoop address is %p %d\n", &inputLoop, inputLoop);
    int a = 1000;



    // bb true does not have calls or loops
    while(inputLoop < a) {
        inputLoop++;
    }
    printf("inputLoop is: %d\n", inputLoop);
    return 0;
}
