#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int global=0;

void *Thread1(void *x) {
	global = 1;
	sleep(2);
	global = 2;
	return NULL;
}

void *Thread2(void *x) {
	int mysize = 10000;
	global++;
	char* buf = (char*) malloc(mysize);
	for (int i = 0 ; i < mysize; i++)
		buf[i] = i*7;
	global++;
	return NULL;
}


int main() {
	pthread_t t[2];
	pthread_create(&t[0], NULL, Thread1, NULL);
	pthread_create(&t[1], NULL, Thread2, NULL);
	pthread_join(t[0], NULL);
	pthread_join(t[1], NULL);
}
