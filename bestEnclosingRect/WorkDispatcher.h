

#pragma once
#ifndef __WORKDISPATCHER__
#define __WORKDISPATCHER__

#include <pthread.h>
#include <semaphore.h>
#include <queue>

class WorkerJob;
extern const int MAXTHREADS;

class WorkDispatcher {
private:
	sem_t mutex; // prio 3
	sem_t workingcount; // prio 2
	sem_t freecount; // prio 1
	std::queue<WorkerJob*> jobs;
	pthread_t *threads;
public:
	WorkDispatcher(void* workerthread(void*));
	~WorkDispatcher();

	WorkerJob *getJob();
	void addJob(WorkerJob *job);
};

#endif
