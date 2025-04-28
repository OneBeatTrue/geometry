import matplotlib.pyplot as plt
import bisect
from heapq import heappush, heappop
from shapes import Point, Segment


class Event:
    def __init__(self, segment, is_start):
        self.segment = segment
        self.is_start = is_start
        self.point = segment.p1 if is_start else segment.p2
        self.x = self.point.x

    def __lt__(self, other):
        if self.x == other.x:
            return self.is_start > other.is_start
        return self.x < other.x


def bentley_ottmann(segments):
    events = []
    status = []
    intersections = []

    for segment in segments:
        heappush(events, Event(segment, True))
        heappush(events, Event(segment, False))

    def insert(segment, x):
        y = segment.intersect_vertical(x)
        bisect.insort(status, (y, segment))

    def remove(segment, x):
        y = segment.intersect_vertical(x)
        index = bisect.bisect_left(status, (y, segment))
        if index < len(status) and status[index][1] == segment:
            status.pop(index)

    def check_neighbors(index):
        if 0 <= index < len(status) - 1:
            seg1 = status[index][1]
            seg2 = status[index + 1][1]
            point = seg1.intersect_b(seg2)
            if point:
                intersections.append(point)

    while events:
        event = heappop(events)
        x = event.x

        if event.is_start:
            insert(event.segment, x)
            index = bisect.bisect_left(status, (event.segment.intersect_vertical(x), event.segment))
            check_neighbors(index - 1)
            check_neighbors(index)
        else:
            index = bisect.bisect_left(status, (event.segment.intersect_vertical(x), event.segment))
            check_neighbors(index - 1)
            check_neighbors(index + 1)
            remove(event.segment, x)

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
