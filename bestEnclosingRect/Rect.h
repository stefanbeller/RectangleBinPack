/** @file Rect.h
	@author Jukka Jylänki, Stefan Beller

	public domain.
*/
#pragma once
#ifndef __RECT__
#define __RECT__

#include <vector>
#include <cassert>

#ifdef _DEBUG
/// debug_assert is an assert that also requires debug mode to be defined.
#define debug_assert(x) assert(x)
#else
#define debug_assert(x)
#endif

using namespace std;

namespace rbp {

struct RectSize
{
	int width;
	int height;
	int id;
};

struct Rect
{
	int x;
	int y;
	int width;
	int height;
	int id;
};

/// Performs a lexicographic compare on (rect short side, rect long side).
/// @return -1 if the smaller side of a is shorter than the smaller side of b, 1 if the other way around.
///   If they are equal, the larger side length is used as a tie-breaker.
///   If the rectangles are of same size, returns 0.
int CompareRectShortSide(const Rect &a, const Rect &b);

/// Performs a lexicographic compare on (x, y, width, height).
int NodeSortCmp(const Rect &a, const Rect &b);

/// Returns true if a is contained in b.
bool IsContainedIn(const Rect &a, const Rect &b);

unsigned enclosingRectWidth(const std::vector<Rect> &rects);
unsigned enclosingRectHeight(const std::vector<Rect> &rects);
unsigned long enclosingRectArea(const std::vector<Rect> &rects);

class DisjointRectCollection
{
private:
	std::vector<Rect> rects;
public:
	bool Add(const Rect &r);
	void Clear();
	bool Disjoint(const Rect &r) const;
	static bool Disjoint(const Rect &a, const Rect &b);
};

}

#endif
