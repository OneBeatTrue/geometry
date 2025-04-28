import matplotlib.pyplot as plt
from shapes import Point, Polygon


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
# polygon.draw_kernel()
for point in points_to_check:
    if polygon.is_inside_by_angle_method(point):
        point.highlight()
    else:
        point.lowlight()

plt.axis('equal')
plt.grid(True)
plt.show()
