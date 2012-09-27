/** @file Rect.cpp
	@author Jukka Jylänki, Stefan Beller

	GPLv3 or later.
*/
#include <utility>

#include "Rect.h"

bool IsContainedIn(const Rect &a, const Rect &b)
{
	return a.x >= b.x && a.y >= b.y
		&& a.x+a.width <= b.x+b.width
		&& a.y+a.height <= b.y+b.height;
}

unsigned enclosingRectWidth(const std::vector<Rect> &rects) {
	unsigned ret = 0;
	for (vector<Rect>::const_iterator it = rects.begin(), end = rects.end(); it != end; ++it)
		ret = std::max(ret, (unsigned)(it->x + it->width));
	return ret;
}

unsigned enclosingRectHeight(const std::vector<Rect> &rects) {
	unsigned ret = 0;
	for (vector<Rect>::const_iterator it = rects.begin(), end = rects.end(); it != end; ++it)
		ret = std::max(ret, (unsigned)(it->y + it->height));
	return ret;
}

unsigned long enclosingRectArea(const std::vector<Rect> &rects) {
	unsigned w = 0;
	unsigned h = 0;
	for (vector<Rect>::const_iterator it = rects.begin(), end = rects.end(); it != end; ++it) {
		h = std::max(h, (unsigned)(it->y + it->height));
		w = std::max(w, (unsigned)(it->x + it->width));
	}
	return (unsigned long)w * (unsigned long)h;
}

bool DisjointRectCollection::Add(const Rect &r)
{
	// Degenerate rectangles are ignored.
	if (r.width == 0 || r.height == 0)
		return true;

	if (!Disjoint(r))
		return false;
	rects.push_back(r);
	return true;
}

void DisjointRectCollection::Clear()
{
	rects.clear();
}

bool DisjointRectCollection::Disjoint(const Rect &a, const Rect &b)
{
	if (a.x + a.width <= b.x ||
		b.x + b.width <= a.x ||
		a.y + a.height <= b.y ||
		b.y + b.height <= a.y)
		return true;
	return false;
}

bool DisjointRectCollection::Disjoint(const Rect &r) const
{
	// Degenerate rectangles are ignored.
	if (r.width == 0 || r.height == 0)
		return true;

	for(size_t i = 0; i < rects.size(); ++i)
		if (!Disjoint(rects[i], r))
			return false;
	return true;
}
