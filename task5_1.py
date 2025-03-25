import matplotlib.pyplot as plt


class Point(object):
    def __init__(self, x, y):
        self.x = round(x, 8)
        self.y = round(y, 8)

    def draw(self):
        plt.scatter(self.x, self.y, color='black', zorder=2)

    def to_str(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def highlight(self):
        plt.scatter(self.x, self.y, color='red', zorder=3)


class Vector(object):
    def __init__(self, p1, p2):
        self.a = p1.x - p2.x
        self.b = p1.y - p2.y

    def pseudoscalar(self, other):
        return self.a * other.b - self.b * other.a


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

    def intersect(self, other):
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


class Polygon(object):

    def __init__(self, points):
        self.points = points
        self.kernel = Point(sum([point.x for point in points]) / len(points), sum([point.y for point in points]) / len(points))

    def draw(self):
        for first_point, second_point in zip(self.points, self.points[1:] + [self.points[0]]):
            Segment(first_point, second_point).draw()

    def draw_kernel(self):
        plt.scatter(self.kernel.x, self.kernel.y, color='blue', zorder=2)
        for point in points:
            Segment(self.kernel, point).draw()

    def is_inside(self, point):
        q_vect = Vector(self.kernel, point)
        for first_point, second_point in zip(self.points, self.points[1:] + [self.points[0]]):
            first_vect = Vector(self.kernel, first_point)
            second_vect = Vector(self.kernel, second_point)
            if q_vect.pseudoscalar(first_vect) * q_vect.pseudoscalar(second_vect) <= 0:
                intersection = Segment(first_point, second_point).intersect(Segment(self.kernel, point))
                return intersection is None


points = [
    Point(2, 0),
    Point(6, 0),
    Point(8, 1),
    Point(7, 5),
    Point(1, 6),
    Point(0, 3),
    Point(1, 1),
]


points_to_check = [
    Point(6, 3),
    Point(8, 5),
Point(1, 5),
]

polygon = Polygon(points)
polygon.draw()
polygon.draw_kernel()
for point in points_to_check:
    if polygon.is_inside(point):
        point.highlight()
    else:
        point.draw()

plt.axis('equal')
plt.grid(True)
plt.show()