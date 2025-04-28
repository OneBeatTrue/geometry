from itertools import combinations
import matplotlib.pyplot as plt
from shapes import Point, Segment



segments = [
    Segment(Point(1,1), Point(2,5)),
    Segment(Point(2,7), Point(5, -1)),
    Segment(Point(3, 4), Point(0, 5)),
    Segment(Point(3, 1), Point(2, 6)),
    Segment(Point(4, 8), Point(5, 0)),
]


for segment in segments:
    segment.draw()

for segment1, segment2 in combinations(segments, r=2):
    print(segment1.to_str(), segment2.to_str())
    #point = segment1.intersect_a(segment2)
    point = segment1.intersect_b(segment2)
    if point is not None:
        print(segment1.to_str() + " " + segment2.to_str() + " : " + point.to_str())
        point.draw("red")

plt.axis('equal')
plt.grid(True)
plt.show()
