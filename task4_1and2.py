from itertools import combinations
import matplotlib.pyplot as plt


class Point(object):
    def __init__(self, x, y):
        self.x = round(x, 8)
        self.y = round(y, 8)

    def draw(self):
        plt.scatter(self.x, self.y, color='red', zorder=2)

    def to_str(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self):
        plt.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], color='black', zorder=1)

    def to_str(self):
        return self.p1.to_str() + " " + self.p2.to_str()

    def get_line(self):
        a = self.p2.y - self.p1.y
        b = self.p1.x - self.p2.x
        c = self.p2.x * self.p1.y - self.p2.y * self.p1.x
        return a, b, c

    def intersect_1(self, other):
        a1, b1, c1 = self.get_line()
        a2, b2, c2 = other.get_line()
        if a1 * b2 - b1 * a2 != 0:
            intersection_point = Point(
                    (b1 * c2 - c1 * b2) / (a1 * b2 - b1 * a2),
                    (c1 * a2 - a1 * c2) / (a1 * b2 - b1 * a2)
                )
            if (min(self.p1.x, self.p2.x) <= intersection_point.x <= max(self.p1.x, self.p2.x) and
                    min(self.p1.y, self.p2.y) <= intersection_point.y <= max(self.p1.y, self.p2.y) and
                    min(other.p1.x, other.p2.x) <= intersection_point.x <= max(other.p1.x, other.p2.x) and
                    min(other.p1.y, other.p2.y) <= intersection_point.y <= max(other.p1.y, other.p2.y)):
                return intersection_point
        return None

    def get_vect(self):
        a = self.p1.x - self.p2.x
        b = self.p1.y - self.p2.y
        return a, b

    def pseudoscalar(self, other):
        a_x, a_y = self.get_vect()
        b_x, b_y = other.get_vect()
        return a_x * b_y - b_x * a_y

    def intersect_2(self, other):
        s = self
        r1 = Segment(s.p1, other.p1)
        r2 = Segment(s.p1, other.p2)
        ps1 = s.pseudoscalar(r1) * s.pseudoscalar(r2)

        s = other
        r1 = Segment(s.p1, self.p1)
        r2 = Segment(s.p1, self.p2)
        ps2 = s.pseudoscalar(r1) * s.pseudoscalar(r2)

        if ps1 <= 0 and ps2 <= 0:
            return self.intersect_1(other)


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
    # point = segment1.intersect_1(segment2)
    point = segment1.intersect_2(segment2)
    if point is not None:
        print(segment1.to_str() + " " + segment2.to_str() + " : " + point.to_str())
        point.draw()

plt.axis('equal')
plt.grid(True)
plt.show()
