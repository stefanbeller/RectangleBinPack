
#include "WorkDispatcher.h"

#include <assert.h>

WorkDispatcher::WorkDispatcher(void* workerthread(void*)) {
	sem_init(&mutex, 0, 1);
	sem_init(&workingcount, 0, 0);
	sem_init(&freecount, 0, MAXTHREADS);
	threads = new pthread_t[MAXTHREADS];

	for (int i = 0; i < MAXTHREADS; i++) {
		pthread_create(&threads[i], 0, workerthread, reinterpret_cast<void*>(this));
	}

}

WorkerJob *WorkDispatcher::getJob() {
	WorkerJob *ret;
	sem_wait(&workingcount);
	sem_wait(&mutex);
	sem_post(&freecount);
	ret = jobs.front();
	jobs.pop();
	sem_post(&mutex);
	return ret;
}

void WorkDispatcher::addJob(WorkerJob *job) {
	sem_wait(&freecount);
	sem_wait(&mutex);
	jobs.push(job);
	sem_post(&workingcount);
	sem_post(&mutex);
}

WorkDispatcher::~WorkDispatcher() {
	for (int i = 0; i < MAXTHREADS; i++)
		addJob(0);

	for (int i = 0; i < MAXTHREADS; i++)
		pthread_join(threads[i], 0);

	sem_destroy(&mutex);
	sem_destroy(&workingcount);
	sem_destroy(&freecount);

	assert(jobs.size() == 0);
	delete[] threads;
}

