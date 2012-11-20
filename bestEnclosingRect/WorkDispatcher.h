/** @file WorkDispatcher.h
	@author Stefan Beller

	public domain.
*/
#pragma once
#ifndef __WORKDISPATCHER__
#define __WORKDISPATCHER__

#include <pthread.h>
#include <semaphore.h>
#include <queue>

class WorkDispatcher {
private:
	const unsigned MAX_THREADS; // how many threads to spawn.

	// always aquire the semaphores with lowest priority first.
	sem_t mutex;        // prio 3 (highest)
	sem_t workingcount; // prio 2
	sem_t freecount;    // prio 1 (lowest)

	std::queue<void*> jobs; // queue holding the arguments to be solved.
	pthread_t *threads; // threads

	// runs threaded, calls getTask and the external function.
	// argument is a WorkDispatcher instance to be served.
	static void *dispatcher(void*);

	void *getTask(); // returns the next argument for the function to be called.
	void (*externcall)(void*); // stores the function to be called.

public:
	/**
	 * Creates a WorkDispatcher, which uses up to \a maxthreads threads.
	 * Within the threads the function \a fct is called with the pointer as
	 * given in addTask.
	 * \a maxthreads is an optional parameter. if it is not given, the number
	 * of cores available will be used.
	 */
	WorkDispatcher(void fct(void*), unsigned maxthreads = 0);

	/**
	 * Waits for all tasks to be done and deletes the object instance.
	 */
	~WorkDispatcher();

	/**
	 * Adds another pointer to a working queue, which will be served
	 * from one thread.
	 */
	void addTask(void *task);
};

#endif
