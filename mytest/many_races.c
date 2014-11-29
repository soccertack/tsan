#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

// Ideally, reports should be ordered by: (first) bug3 > bug4 > bug2 > bug1

int global1;
int global2;
int global3;
int global4;
int global5;

// Starting two Thread1_bug1 will create a race. The window here is small, just the printf.
void *Thread_PrintfBetween(void *x) {
    global1++;
    int temp = global1;
    printf("temp1 %d", temp);
    sleep(1);
    global1++;
    return NULL;
}

// Starting two Thread1_bug2 will create a race. The window here is a loop with a fixed number of iteration.
void *Thread_StaticLoop(void *x) {
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
void *Thread_DynamicLoop(void *x) {
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
void *Thread_BlockingRead(void *x) {
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
//
// Starting two Thread_bug5 will create a race. The window here is the malloc.
void *Thread_MallocBetween(void *x) {
    int temp = global5;
    char* buf = (char*) malloc(1000);
    global5++;
    return NULL;
}

void *Thread_Nothing(void *x) {
	return NULL;
}

int main() {
    const int nthreads = 2;
    pthread_t t[nthreads];

    int inputLoop = 10000;

    pthread_create(&t[0], NULL, Thread_PrintfBetween, NULL);
    pthread_create(&t[1], NULL, Thread_PrintfBetween, NULL);
    /*pthread_create(&t[2], NULL, Thread_StaticLoop, NULL);*/
    /*pthread_create(&t[3], NULL, Thread_StaticLoop, NULL);*/
    /*pthread_create(&t[4], NULL, Thread_DynamicLoop, &inputLoop);*/
    /*pthread_create(&t[5], NULL, Thread_DynamicLoop, &inputLoop);*/
    /*pthread_create(&t[6], NULL, Thread_BlockingRead, NULL);*/
    /*pthread_create(&t[7], NULL, Thread_BlockingRead, NULL);*/
    /*pthread_create(&t[8], NULL, Thread_MallocBetween, NULL);*/
    /*pthread_create(&t[9], NULL, Thread_MallocBetween, NULL);*/

    int i = 0;
    for (i = 0; i < nthreads; i++) {
        pthread_join(t[i], NULL);
    }
}
