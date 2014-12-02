#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

#define MAX_SIZE 10

int global=0;
char queue[MAX_SIZE] = {'\0',};

void *Thread1(void *x) {
    int next = strlen(queue);
    if (next == MAX_SIZE) {
        printf("ERROR\n");
        return NULL;
    }
	sleep(2);
	queue[next] = 1;
	return NULL;
}

void *Thread2(void *x) {
	int mysize = 10000;
	queue[0]++;
	char* buf = (char*) malloc(mysize);
	for (int i = 0 ; i < mysize; i++)
		buf[i] = i*7;
	queue[0]++;
	return NULL;
}


int main() {
	pthread_t t[2];
	pthread_create(&t[0], NULL, Thread1, NULL);
	pthread_create(&t[1], NULL, Thread2, NULL);
	pthread_join(t[0], NULL);
	pthread_join(t[1], NULL);
}
