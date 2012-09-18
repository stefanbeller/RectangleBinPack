/** @file main.cpp
	@author Stefan Beller

	GPLv3 or later.
*/
#include "MaxRectsBinPack.h"
#include "Rect.h"

#include "WorkDispatcher.h"

#include <stdio.h>
#include <stdlib.h>

#include <vector>
#include <algorithm>
#include <semaphore.h>
#include <sys/wait.h>
#include <iostream>
#include <utility>

#include <pthread.h>

using namespace std;

bool compareRectIds (Rect i, Rect j) { return (i.id < j.id); }

unsigned int maxSmallRectWidth = 0;
unsigned int maxSmallRectHeight = 0;
unsigned long minEnclosingArea = 0;
unsigned long maxEnclosingArea = 0;

unsigned long best_rects_size = 0;
vector<Rect> best_rects;
sem_t best_rects_mutex;

const int MAXTHREADS = 9;

void calculateBoundaries(vector<RectSize> rects) {
	maxSmallRectWidth = 0;
	maxSmallRectHeight = 0;
	minEnclosingArea = 0;
	maxEnclosingArea = 0;
	for (vector<RectSize>::iterator it = rects.begin(), end = rects.end(); it != end; it++) {
		maxSmallRectHeight = std::max(maxSmallRectHeight, (unsigned int)it->height);
		maxSmallRectWidth = std::max(maxSmallRectWidth, (unsigned int)it->width);
		minEnclosingArea += it->height*it->width;
	}
	maxEnclosingArea = rects.size() * maxSmallRectHeight * maxSmallRectWidth;
	best_rects_size = maxEnclosingArea;
}

struct WorkerJob {
	vector<RectSize> *passed_rects;
	unsigned long area;
	unsigned int w;
	sem_t *postOnFound;
	WorkerJob(vector<RectSize> *passed_rects_, unsigned long area_, unsigned int w_, sem_t *postOnFound_) {
		passed_rects = passed_rects_;
		area = area_;
		w = w_;
		postOnFound = postOnFound_;
	}
};

void checkArea(void *args)
{
	WorkDispatcher *dispatcher = reinterpret_cast<WorkDispatcher*>(args);
	while (WorkerJob *job = dispatcher->getJob()) {
		MaxRectsBinPack bin;
		vector<Rect> returnrects;
		vector<RectSize> rects(*(job->passed_rects));
		unsigned h = job->area/job->w;

		bin.Init(job->w, h);
		MaxRectsBinPack::FreeRectChoiceHeuristic heuristic = MaxRectsBinPack::RectBestShortSideFit;
		bin.Insert(rects, returnrects, heuristic);

		// if all rects could be inserted and we're better than before:
		if (rects.size() == 0) {
			if (enclosingRectArea(returnrects) < best_rects_size) {
				sem_wait(&best_rects_mutex);
				if (enclosingRectArea(returnrects) < best_rects_size) {
					best_rects_size = enclosingRectArea(returnrects);
					best_rects = returnrects;
				}
				sem_post(&best_rects_mutex);
			}
			sem_post(job->postOnFound);
		}
		delete job;
	}
	pthread_exit(0);
}

bool checkAreaSize(vector<RectSize> &passed_rects, unsigned long area, bool quitEarly, int maxTries = 0) {
	// returns true if a fit was found
	bool foundFit = false;
	WorkDispatcher *workDispatcher = new WorkDispatcher(reinterpret_cast<void* (*)(void*)>(&checkArea));

	sem_t fitFounds;
	sem_init(&fitFounds, 0, 0);

	if (maxTries) {
		int yetToStart = maxTries;
		while (yetToStart > 0) {

			unsigned w = maxSmallRectWidth + rand() % area/maxSmallRectHeight;

			WorkerJob *t = new WorkerJob(&passed_rects, area, w, &fitFounds);
			workDispatcher->addJob(t);
			yetToStart--;

			if (!foundFit && !sem_trywait(&fitFounds))
				foundFit = true;

			if (quitEarly && foundFit)
				yetToStart = 0;
		}

	} else {
		for (unsigned int w = maxSmallRectWidth, end = area/maxSmallRectWidth; w < end; w++) {
			WorkerJob *t = new WorkerJob(&passed_rects, area, w, &fitFounds);
			workDispatcher->addJob(t);

			if (!foundFit && !sem_trywait(&fitFounds))
				foundFit = true;

			if (quitEarly && foundFit)
				w = end;
		}
	}

	delete workDispatcher;

	if (!foundFit && !sem_trywait(&fitFounds))
		foundFit = true;

	return foundFit;
}

void binarySearch(vector<RectSize> &rects) {
	unsigned long  upper = maxEnclosingArea;
	unsigned long  lower = minEnclosingArea;

	while (upper - lower > 1) {
		unsigned long middle = (upper + lower) / 2;
		if (checkAreaSize(rects, middle, true, 1024))
			upper = best_rects_size;
		else
			lower = middle;
	}
}

void linearSearch(vector<RectSize> &rects) {
	do {
	} while (checkAreaSize(rects, best_rects_size - 1, false));
}

int main(int argc, char **argv)
{
	if (argc < 3 || argc % 2 != 1)
	{
		printf("Usage: MaxRectsBinPackTest w_0 h_0 w_1 h_1 w_2 h_2 ... w_n h_n\n");
		printf("       w_i is the width of the i'th rectangle to pack, and h_i the height.\n");
		printf("Example: MaxRectsBinPackTest 256 256 30 20 50 20 10 80 90 20\n\n");
		printf("On error 1 will be returned. On success the return value is 0 and the x/y coordinates \n");
		printf("of each input rect will be printed to screen. The order of the output is the same as in the input.\n");
		return 1;
	}

	sem_init(&best_rects_mutex, 0, 1);

	vector<RectSize> rects;
	// Pack each rectangle (w_i, h_i) the user inputted on the command line.
	for(int i = 1; i < argc; i += 2)
	{
		// Read next rectangle to pack.
		RectSize r;
		r.width = atoi(argv[i]);
		r.height = atoi(argv[i+1]);
		r.id = (i-1)/2;
		rects.push_back(r);
	}

	calculateBoundaries(rects);
	binarySearch(rects);
	linearSearch(rects);

	sort(best_rects.begin(), best_rects.end(), compareRectIds);
	for (vector<Rect>::iterator it = best_rects.begin(); it != best_rects.end(); it++) {
		printf ("%d %d\n", it->x, it->y);
	}
	return 0;
}
