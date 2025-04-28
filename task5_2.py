import matplotlib.pyplot as plt
from shapes import Point, Polygon

size = 20
range_x, range_y = size, size
x_min, x_max, y_min, y_max = -range_x / 2, range_x / 2, -range_y / 2, range_y / 2

n = 16
points = [Point.get_random(x_min, x_max, y_min, y_max) for _ in range(n)]

first_points = points[:n // 2]
first_polygon = Polygon.get_coverage_graham(first_points)
first_polygon.fill("#ff808a")
first_polygon.draw("red")
for point in first_points:
    point.draw("#8b0000")

second_points = points[n // 2:]
second_polygon = Polygon.get_coverage_graham(second_points)
second_polygon.fill("#a6caf0")
second_polygon.draw("blue")
for point in second_points:
    point.draw("#00406b")

intersection = first_polygon.intersect(second_polygon)
intersection.fill("#876c99")
intersection.draw("purple")
for point in points:
    if intersection.is_inside(point):
        point.draw("#462036")


plt.axis('equal')
plt.grid(True)
plt.show()
