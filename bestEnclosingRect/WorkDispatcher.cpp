/** @file WorkDispatcher.cpp
	@author Stefan Beller

	public domain.
*/
#include "WorkDispatcher.h"
#include <assert.h>

void* WorkDispatcher::dispatcher(void *args) {
	WorkDispatcher *disp = reinterpret_cast<WorkDispatcher*>(args);
	while (void *job = disp->getTask()) {
		disp->externcall(job);
	}
	pthread_exit(0);
}

WorkDispatcher::WorkDispatcher(void workertask(void*), const unsigned numThreads)
 : MAX_THREADS(numThreads)
 , externcall(workertask)
{
	sem_init(&mutex, 0, 1);
	sem_init(&workingcount, 0, 0);
	sem_init(&freecount, 0, MAX_THREADS);
	threads = new pthread_t[MAX_THREADS];

	for (unsigned i = 0; i < MAX_THREADS; i++) {
		pthread_create(&threads[i], 0, reinterpret_cast<void* (*)(void*)>(&WorkDispatcher::dispatcher), reinterpret_cast<void*>(this));
	}
}

void *WorkDispatcher::getTask() {
	void *ret;
	sem_wait(&workingcount);
	sem_wait(&mutex);
	ret = jobs.front();
	jobs.pop();
	sem_post(&freecount);
	sem_post(&mutex);
	return ret;
}

void WorkDispatcher::addTask(void *job) {
	sem_wait(&freecount);
	sem_wait(&mutex);
	jobs.push(job);
	sem_post(&workingcount);
	sem_post(&mutex);
}

WorkDispatcher::~WorkDispatcher() {
	for (unsigned i = 0; i < MAX_THREADS; i++)
		addTask(0);

	for (unsigned i = 0; i < MAX_THREADS; i++)
		pthread_join(threads[i], 0);

	sem_destroy(&mutex);
	sem_destroy(&workingcount);
	sem_destroy(&freecount);

	assert(jobs.size() == 0);
	delete[] threads;
}

