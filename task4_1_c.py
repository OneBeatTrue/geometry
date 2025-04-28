import matplotlib.pyplot as plt
import bisect
from heapq import heappush, heappop
from shapes import Point, Segment
import heapq


class Event:
    def __init__(self, segment, is_start):
        self.segment = segment
        self.is_start = is_start
        self.point = segment.p1 if is_start else segment.p2
        self.x = self.point.x

    def __lt__(self, other):
        if self.x == other.x:
            return self.is_start > other.is_start
        return self.point < other.point


def bentley_ottmann(segments):
    events = []
    active = []
    intersections = []
    for segment in segments:
        events.append(Event(segment, True))
        events.append(Event(segment, False))

    events.sort()
    for event in events:
        if event.is_start:
            active.append(event.segment)
            for other_segment in active:
                if other_segment != event.segment:
                    point = event.segment.intersect(other_segment)
                    if point:
                        intersections.append(point)
        else:
            active.remove(event.segment)
    return intersections


segments = [
    Segment(Point(1,1), Point(2,5)),
    Segment(Point(2,7), Point(5, -1)),
    Segment(Point(3, 4), Point(0, 5)),
    Segment(Point(3, 1), Point(2, 6)),
    Segment(Point(4, 8), Point(5, 0)),
]


for segment in segments:
    segment.draw()

intersection_points = bentley_ottmann(segments)
for point in intersection_points:
    point.draw("red")

plt.axis('equal')
plt.grid(True)
plt.show()
