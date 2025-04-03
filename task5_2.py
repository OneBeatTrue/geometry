from itertools import combinations
import matplotlib.pyplot as plt

eps = 8


class Point(object):
    def __init__(self, x, y):
        self.x = round(x, eps)
        self.y = round(y, eps)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self, color='black'):
        plt.scatter(self.x, self.y, color=color, zorder=2)

    def to_str(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def highlight(self):
        plt.scatter(self.x, self.y, color='#66ff00', zorder=3)

    def lowlight(self):
        plt.scatter(self.x, self.y, color='red', zorder=3)

class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2 or self.p1 == other.p2 and self.p2 == other.p1

    def draw(self):
        plt.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], color='black', zorder=1)

    def to_str(self):
        return self.p1.to_str() + " " + self.p2.to_str()

    def get_line(self):
        a = self.p2.y - self.p1.y
        b = self.p1.x - self.p2.x
        c = self.p2.x * self.p1.y - self.p2.y * self.p1.x
        return a, b, c

    def contain(self, point):
        a, b, c = self.get_line()
        return (min(self.p1.x, self.p2.x) <= point.x <= max(self.p1.x, self.p2.x) and
                min(self.p1.y, self.p2.y) <= point.y <= max(self.p1.y, self.p2.y) and
                round(a * point.x + b * point.y + c, eps) == 0)

    def intersect(self, other):
        a1, b1, c1 = self.get_line()
        a2, b2, c2 = other.get_line()
        if round(a1 * b2 - b1 * a2, eps) != 0:
            intersection_point = Point(
                    (b1 * c2 - c1 * b2) / (a1 * b2 - b1 * a2),
                    (c1 * a2 - a1 * c2) / (a1 * b2 - b1 * a2)
                )
            if self.contain(intersection_point) and other.contain(intersection_point):
                return intersection_point
        return None


class HorizontalRightRay(object):
    def __init__(self, point):
        self.point = point

    def intersect(self, segment):
        if segment.contain(self.point):
            return self.point
        return Segment(self.point, Point(max(segment.p1.x, segment.p2.x, self.point.x) + 1, self.point.y)).intersect(segment)


class Polygon(object):
    def __init__(self, points):
        self.points = points

    def draw(self):
        for first_point, second_point in zip(self.points, self.points[1:] + [self.points[0]]):
            Segment(first_point, second_point).draw()

    def is_inside(self, point):
        q_ray = HorizontalRightRay(point)
        intersections = []
        segments = []
        all_segments = []
        for first_point, second_point in zip(self.points, self.points[1:] + self.points[0:1]):
            segment = Segment(first_point, second_point)
            all_segments.append(segment)
            if segment.contain(point):
                return True
            intersection = q_ray.intersect(segment)
            if intersection is not None:
                intersections.append(intersection)
                segments.append(segment)

        if len(intersections) < 2:
            return len(intersections) % 2 == 1

        pairs = [tuple([intersection, segment]) for intersection, segment in zip(intersections, segments)]
        cycle_check = len(pairs) != 2 and (pairs[0][0] == pairs[-1][0] or (Segment(pairs[0][0], pairs[-1][0]) in all_segments))
        # циклическая проверка нужна в случае если обход сторон разорвал последовательные точки пересечения
        count = not cycle_check
        # в случае если не требуется циклическая проверка посследнюю точку положим сразу
        for i in range(len(pairs) - (not cycle_check)):
            first_point, first_segment, second_point, second_segment = pairs[i][0], pairs[i][1], pairs[(i + 1) % len(pairs)][0], pairs[(i + 1) % len(pairs)][1]
            if ((first_point != first_segment.p1 and first_point != first_segment.p2) or # если пересечение произошло не в вершине
                (max(first_segment.p1.y, first_segment.p2.y) == max(second_segment.p1.y, second_segment.p2.y) or # проверка на то лежат ли отрезки по разные стороны от луча
                 min(first_segment.p1.y, first_segment.p2.y) == min(second_segment.p1.y, second_segment.p2.y))):
                count += 1
        return count % 2 == 1


# points = [
#     Point(2, 0),
#     Point(6, 0),
#     Point(8, 1),
#     Point(7, 5),
#     Point(1, 6),
#     Point(0, 3),
#     Point(1, 1),
# ]
#
#
# points_to_check = [
#     Point(6, 3),
#     Point(8, 5),
# Point(1, 5),
# ]

# points = [
#     Point(1, 1),
#     Point(2, 2),
#     Point(4, 0),
#     Point(4, 1),
#     Point(5, 1),
#     Point(6, 0),
#     Point(6, 4),
#     Point(4, 6),
#     # Point(3.7, 4),
#     # Point(3.5, 4),
#     # Point(3, 4),
#     # Point(5, 4),
#     Point(2, 4),
#     Point(0, 6),
# ]
#
#
# points_to_check = [
#     Point(1.5, 4),
#     Point(3.5, 5),
#     Point(4, 1),
# ]

points = [
    Point(1, 1),
    Point(2, 2),
    Point(4, 0),
    Point(6, 4),
    Point(4, 6),
    Point(2, 4),
    Point(0, 6),
]


points_to_check = [
    Point(1.5, 4.2),
    Point(3.5, 5),
    Point(4.5, 1),
]

polygon = Polygon(points)
polygon.draw()
for point in points_to_check:
    if polygon.is_inside(point):
        point.highlight()
    else:
        point.lowlight()

plt.axis('equal')
plt.grid(True)
plt.show()