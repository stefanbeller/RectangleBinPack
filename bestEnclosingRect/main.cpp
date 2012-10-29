/** @file main.cpp
	@author Stefan Beller

	public domain.
*/
#include "MaxRectsBinPack.h"
#include "Rect.h"

#include "WorkDispatcher.h"
#include "NumberOfCores.h"

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

unsigned int maxSmallRectWidth;
unsigned int maxSmallRectHeight;
unsigned long minEnclosingArea;
unsigned long maxEnclosingArea;

const int MAXTHREADS = getNumCores();
const int maxTriesBinarySearch = 2048;


// holds rectangles of equal size; each rectangle has width/height as a power of 2.
// may only be changed if the mutex is hold.
unsigned long constraint_rects_size = 0;
vector<RectSize> constraint_rects;
sem_t constraint_rects_mutex;

// holds the best solution found so far.
// may only be changed if the mutex is hold.
unsigned long best_rects_size = 0;
vector<Rect> best_rects;
sem_t best_rects_mutex;


struct WorkerJob {
	vector<RectSize> *passed_rects;
	unsigned int w;
	unsigned int h;
	sem_t *postOnFound;
	bool updateConstraintsRect;
	WorkerJob(vector<RectSize> *passed_rects_, unsigned int w_, unsigned int h_, sem_t *postOnFound_, bool updateConstraintsRect_) {
		passed_rects = passed_rects_;
		w = w_;
		h = h_;
		postOnFound = postOnFound_;
		updateConstraintsRect = updateConstraintsRect_;
	}
};


void calculateBoundaries(vector<RectSize> rects) {
	maxSmallRectWidth = 1;
	maxSmallRectHeight = 1;
	minEnclosingArea = 0;
	for (vector<RectSize>::iterator it = rects.begin(), end = rects.end(); it != end; ++it) {
		maxSmallRectHeight = std::max(maxSmallRectHeight, (unsigned int)it->height);
		maxSmallRectWidth = std::max(maxSmallRectWidth, (unsigned int)it->width);
		minEnclosingArea += it->height*it->width;
	}
	maxEnclosingArea = rects.size() * maxSmallRectHeight * maxSmallRectWidth;
	best_rects_size = 2 * maxEnclosingArea;
}

/// Round up to next higher power of 2 (return x if it's already a power
/// of 2).
unsigned pow2roundup(unsigned x)
{
	if (x == 0)
		return 0;
	--x;
	x |= x >> 1;
	x |= x >> 2;
	x |= x >> 4;
	x |= x >> 8;
	x |= x >> 16;
	return x+1;
}

void checkArea(void *args)
{
	WorkerJob *job = reinterpret_cast<WorkerJob*>(args);
	MaxRectsBinPack bin;
	vector<Rect> returnrects;
	vector<RectSize> rects(*(job->passed_rects));
	bin.Init(job->w, job->h);
	MaxRectsBinPack::FreeRectChoiceHeuristic heuristic = MaxRectsBinPack::RectBestShortSideFit;
	bin.Insert(rects, returnrects, heuristic);

	// if all rects could be inserted and we're better than before:
	if (rects.empty()) {
		unsigned long mysize = enclosingRectArea(returnrects);
		if (mysize < best_rects_size) {
			sem_wait(&best_rects_mutex);
			if (mysize < best_rects_size) {
				best_rects_size = mysize;
				best_rects = returnrects;
			}
			sem_post(&best_rects_mutex);
		}
		if (job->postOnFound) sem_post(job->postOnFound);
		if (job->updateConstraintsRect) {
			sem_wait(&constraint_rects_mutex);
			if (mysize < constraint_rects_size) {
				constraint_rects_size = mysize;
				constraint_rects.clear();
			}
			if (mysize == constraint_rects_size) {
				RectSize r;
				r.width = job->w;
				r.height = job->h;
				constraint_rects.push_back(r);
			}
			sem_post(&constraint_rects_mutex);
		}
	}
	delete job;
}

bool checkAreaSizeExhaustive(vector<RectSize> &passed_rects, unsigned long area) {
	// returns true if a fit was found
	WorkDispatcher *workDispatcher = new WorkDispatcher(reinterpret_cast<void (*)(void*)>(&checkArea), MAXTHREADS);

	sem_t fitFounds;
	sem_init(&fitFounds, 0, 0);

	for (size_t i = 0; i < constraint_rects.size(); ++i) {
		RectSize r = constraint_rects[i];
		unsigned int maxEnclosingWidth = r.width;
		unsigned int maxEnclosingHeight = r.height;
		for (unsigned int w = maxSmallRectWidth, end = maxEnclosingWidth; w < end; w++) {
			unsigned int h = min(static_cast<unsigned int>(area/w), maxEnclosingHeight);
			assert (w <= maxEnclosingWidth || h <= maxEnclosingHeight);
			WorkerJob *t = new WorkerJob(&passed_rects, w, h, &fitFounds, false);
			workDispatcher->addTask(t);
		}
	}

	delete workDispatcher;

	return !sem_trywait(&fitFounds);
}

bool checkAreaSizeFast(vector<RectSize> &passed_rects, unsigned long area, int maxTries = 0) {
	// returns true if a fit was found
	bool foundFit = false;
	WorkDispatcher *workDispatcher = new WorkDispatcher(reinterpret_cast<void (*)(void*)>(&checkArea), MAXTHREADS);

	sem_t fitFounds;
	sem_init(&fitFounds, 0, 0);

	int yetToStart = maxTries;
	while (yetToStart > 0) {
		unsigned int constraint_rects_index = rand() % constraint_rects.size();
		RectSize r = constraint_rects[constraint_rects_index];
		unsigned int maxEnclosingWidth = r.width;
		unsigned int maxEnclosingHeight = r.height;

		int minWidth = maxSmallRectWidth;
		int maxWidth = maxEnclosingWidth;
		unsigned int w = minWidth + ((maxWidth - minWidth) > 0 ? rand() % (maxWidth - minWidth) : 0);
		unsigned int h = std::min(static_cast<unsigned int>(area/w), maxEnclosingHeight);

		assert(w <= maxEnclosingWidth && h <= maxEnclosingHeight);

		WorkerJob *t = new WorkerJob(&passed_rects, w, h, &fitFounds, false);
		workDispatcher->addTask(t);
		yetToStart--;

		if (!foundFit && !sem_trywait(&fitFounds)) {
			foundFit = true;
			yetToStart = 0;
		}
	}

	delete workDispatcher;

	if (!foundFit && !sem_trywait(&fitFounds))
		foundFit = true;

	return foundFit;
}

void checkAreaSizePowersOf2(vector<RectSize> &passed_rects) {
	WorkDispatcher *workDispatcher = new WorkDispatcher(reinterpret_cast<void (*)(void*)>(&checkArea), MAXTHREADS);

	sem_t fitFounds;
	sem_init(&fitFounds, 0, 0);
	constraint_rects_size = 4 * maxEnclosingArea;

	for (unsigned int w = pow2roundup(maxSmallRectWidth); w <= 2 * maxEnclosingArea/maxSmallRectHeight; w*=2) {
		for (unsigned int h = pow2roundup(maxSmallRectHeight); h <= 2 * maxEnclosingArea/maxSmallRectWidth; h*=2) {
			if ( w * h < minEnclosingArea) continue;
			WorkerJob *t = new WorkerJob(&passed_rects, w, h, &fitFounds, true);
			workDispatcher->addTask(t);
		}
	}

	delete workDispatcher;
	assert(constraint_rects.size() > 0);
}

void binarySearch(vector<RectSize> &rects) {
	unsigned long upper = min((unsigned long)(constraint_rects_size),(unsigned long)maxEnclosingArea);
	unsigned long lower = minEnclosingArea;

	while (upper - lower > 1) {
		unsigned long middle = (upper + lower) / 2;
		if (checkAreaSizeFast(rects, middle, maxTriesBinarySearch)) {
			upper = best_rects_size;
			lower = std::min(lower, upper);
		}
		else {
			lower = middle;
		}
	}
}

void linearSearch(vector<RectSize> &rects) {
	do {
	} while (checkAreaSizeExhaustive(rects, best_rects_size - 1));
}

int main(int argc, char **argv)
{
	if (argc < 3 || argc % 2 != 1)
	{
		fprintf(stderr, "Usage: \n\trectpacker w_0 h_0 w_1 h_1 w_2 h_2 ... w_n h_n\n\n");
		fprintf(stderr, "w_i is the width of the i'th rectangle to pack, and h_i the height.\n");
		fprintf(stderr, "Example: MaxRectsBinPackTest 256 256 30 20 50 20 10 80 90 20\n\n");
		fprintf(stderr, "On error a value unequal zero will be returned.\n");
		fprintf(stderr, "On success the return value is 0 and the x/y coordinates \n");
		fprintf(stderr, "of each input rect will be printed to screen.\n");
		fprintf(stderr, "The order of the output is the same as in the input.\n");
		return 1;
	}

	sem_init(&best_rects_mutex, 0, 1);
	sem_init(&constraint_rects_mutex, 0, 1);

	vector<RectSize> rects;
	// Pack each rectangle (w_i, h_i) the user inputted on the command line.
	for(int i = 1; i < argc; i += 2)
	{
		// Read next rectangle to pack.
		RectSize r;
		r.width = atoi(argv[i]);
		r.height = atoi(argv[i+1]);
		if (r.width <= 0 || r.height <= 0) {
			fprintf(stderr, "input parameters: width and height must be greater than zero.\n");
			return 2;
		}

		r.id = (i-1)/2;
		rects.push_back(r);
	}

	calculateBoundaries(rects);
	checkAreaSizePowersOf2(rects);
	binarySearch(rects);
	linearSearch(rects);

	sort(best_rects.begin(), best_rects.end(), compareRectIds);
	for (vector<Rect>::iterator it = best_rects.begin(); it != best_rects.end(); ++it) {
		printf ("%d %d\n", it->x, it->y);
	}
	return 0;
}
