#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

int jin=0;
int mat=0;
pthread_spinlock_t myspinlock;

void *Thread1(void *x) {
	jin = 1;
	sleep(1);
	jin = 2;
	    return NULL;
}

void *Thread2(void *x) {
	  jin++;
	    return NULL;
}

void *Thread3(void *x) {
	mat++;
	sleep(2);
	  mat++;
	    return NULL;
}

void *Thread4(void *x) {
	mat = 3;
	    return NULL;
}

int main() {
	pthread_spin_init(&myspinlock, 0);

	pthread_t t[4];
	pthread_create(&t[0], NULL, Thread1, NULL);
	pthread_create(&t[1], NULL, Thread2, NULL);
//	pthread_create(&t[2], NULL, Thread3, NULL);
//	pthread_create(&t[3], NULL, Thread4, NULL);
	pthread_join(t[0], NULL);
	pthread_join(t[1], NULL);
//	pthread_join(t[2], NULL);
//	pthread_join(t[3], NULL);
}
