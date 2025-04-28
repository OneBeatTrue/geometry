import matplotlib.pyplot as plt
from shapes import Point, Polygon


size = 20
range_x, range_y = size, size
x_min, x_max, y_min, y_max = -range_x / 2, range_x / 2, -range_y / 2, range_y / 2

n = 10
points = [Point.get_random(x_min, x_max, y_min, y_max) for _ in range(n)]

m = 5
points_to_check = [Point.get_random(x_min, x_max, y_min, y_max) for _ in range(m)]

polygon = Polygon.get_coverage_graham(points)
print("Perimeter:", polygon.get_perimeter())
print("Area:", polygon.get_area())
polygon.draw()

for point in points:
    point.draw()

plt.axis('equal')
plt.grid(True)
plt.show()

