#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

// Ideally, reports should be ordered by: (first) bug3 > bug4 > bug2 > bug1

int global1;
int global2;
int global3;
int global4;

// Starting two Thread1_bug1 will create a race. The window here is small, just the printf.
void *Thread_bug1(void *x) {
    int temp = global1;
    printf("temp1 %d", temp);
    global1++;
    return NULL;
}

// Starting two Thread1_bug2 will create a race. The window here is a loop with a fixed number of iteration.
void *Thread_bug2(void *x) {
    int temp = global2;
    int temp2 = 0;
    for(int i = 0; i < 10000; i++) {
        temp2 = i > temp ? i : temp;
    }
    printf("bug1 %d", temp2);
    global2++;
    return NULL;
}

// Starting two Thread1_bug3 will create a race. The window here is a loop with the number of iterations dependent on the input x.
void *Thread_bug3(void *x) {
    int* loop = (int*) x;
    int temp = global3;
    int temp2 = 0;
    for(int i = 0; i < *loop; i++) {
        temp2 = i > temp ? i : temp;
    }
    printf("bug3 %d", temp2);
    global3++;
    return NULL;
}

// Starting two Thread1_bug4 will create a race. The window here is a read that might block.
void *Thread_bug4(void *x) {
    char buf[1000];
    size_t nread;
    FILE* file = fopen("/dev/random", "rb");
    if (!file) {
        printf("FAIL to open random\n");
        exit(1);
    }

    int temp = global4;
    nread = fread(buf, 1, 100, file);
    printf("bug4 %zu", nread);
    global4++;

    fclose(file);
    return NULL;
}

int main() {
    pthread_t t[8];

    int inputLoop = 10000;

    pthread_create(&t[0], NULL, Thread_bug1, NULL);
    pthread_create(&t[1], NULL, Thread_bug1, NULL);
    pthread_create(&t[2], NULL, Thread_bug2, NULL);
    pthread_create(&t[3], NULL, Thread_bug2, NULL);
    pthread_create(&t[4], NULL, Thread_bug3, &inputLoop);
    pthread_create(&t[5], NULL, Thread_bug3, &inputLoop);
    pthread_create(&t[6], NULL, Thread_bug4, NULL);
    pthread_create(&t[7], NULL, Thread_bug4, NULL);

    pthread_join(t[0], NULL);
    pthread_join(t[1], NULL);
    pthread_join(t[2], NULL);
    pthread_join(t[3], NULL);
    pthread_join(t[4], NULL);
    pthread_join(t[5], NULL);
    pthread_join(t[6], NULL);
    pthread_join(t[7], NULL);
}
