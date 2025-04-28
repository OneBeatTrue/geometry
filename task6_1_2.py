import matplotlib.pyplot as plt
from shapes import Point, Polygon, Line, Segment, Vector


class VoronoiCell(object):
    def __init__(self, point, polygon):
        self.point = point
        self.polygon = polygon
        self.neighbors = set()

    def check_neighbors(self):
        new_neighbors = set()
        for neighbor in self.neighbors:
            add_neighbor = False
            for point in self.polygon.points:
                if point in neighbor.polygon.points:
                    add_neighbor = True
                    break
            if add_neighbor:
                new_neighbors.add(neighbor)
        self.neighbors = new_neighbors

    def draw(self, polygon_color="black", point_color="red", fill_color="white"):
        self.polygon.draw(polygon_color)
        self.point.draw(point_color)
        # self.polygon.fill(fill_color)


class VoronoiDiagram(object):
    def __init__(self, cells):
        self.cells = cells

    def draw(self):
        for cell in self.cells:
            cell.draw()

    def draw_delaunay(self, color="blue"):
        for cell in self.cells:
            for neighbor in cell.neighbors:
                Segment(cell.point, neighbor.point).draw(color)

    def closest_pair(self):
        min_segment = None
        for cell in self.cells:
            for neighbor in cell.neighbors:
                segment = Segment(cell.point, neighbor.point)
                if min_segment is None or segment.get_length() < min_segment.get_length():
                    min_segment = segment
        return min_segment

    def get_relaxed(self):
        return [cell.polygon.kernel for cell in self.cells]


def build_voronoi_diagram(points, edges):
    sorted_points = sorted(points)
    diagram = voronoi_split(sorted_points, edges, 0, len(points))
    for cell in diagram.cells:
        cell.check_neighbors()
    return diagram


def voronoi_split(points, edges, left, right):
    if right - left == 1:
        return VoronoiDiagram([VoronoiCell(points[left], edges)])
    if right - left == 2:
        mid_perpendicular = Segment(points[left], points[right - 1]).mid_perpendicular()
        left_ceil = VoronoiCell(points[left], edges.clip(mid_perpendicular))
        right_ceil = VoronoiCell(points[right - 1], edges.clip(mid_perpendicular.inverted()))
        left_ceil.neighbors = {right_ceil}
        right_ceil.neighbors = {left_ceil}
        return VoronoiDiagram([left_ceil, right_ceil])

    mid = (left + right) // 2
    left_diagram = voronoi_split(points, edges, left, mid)
    right_diagram = voronoi_split(points, edges, mid, right)

    return voronoi_merge(left_diagram, right_diagram)


def voronoi_merge(left, right):
    all_cells = []

    for cells, other_cells in [[left.cells, right.cells], [right.cells, left.cells]]:
        for cell in cells:
            polygon = cell.polygon
            neighbors = cell.neighbors
            for other_cell in other_cells:
                mid_perpendicular = Segment(cell.point, other_cell.point).mid_perpendicular()
                if mid_perpendicular(cell.point) > 0:
                    mid_perpendicular = mid_perpendicular.inverted()
                if polygon.is_intersect_line(mid_perpendicular):
                    polygon = polygon.clip(mid_perpendicular)
                    neighbors.add(other_cell)
            all_cells.append((cell, polygon, neighbors))

    cell_list = []
    for cell, polygon, neighbors in all_cells:
        cell.polygon = polygon
        cell.neighbors = neighbors
        cell_list.append(cell)

    return VoronoiDiagram(cell_list)


size = 20
range_x, range_y = size, size
x_min, x_max, y_min, y_max = -range_x / 2, range_x / 2, -range_y / 2, range_y / 2

n = 10
points = [Point.get_random(x_min, x_max, y_min, y_max) for _ in range(n)]
multiplier = 100

edges = Polygon([
    Point(multiplier * x_min, multiplier * y_min),
    Point(multiplier * x_max, multiplier * y_min),
    Point(multiplier * x_max, multiplier * y_max),
    Point(multiplier * x_min, multiplier * y_max),
])
diagram = build_voronoi_diagram(points, edges)

plt.figure(figsize=(10, 10))
diagram.draw()
diagram.draw_delaunay()
closest = diagram.closest_pair()
closest.draw("red")
print(closest.to_str())
print("Distance: ", closest.get_length())

visual_multiplier = 1.5
plt.xlim(visual_multiplier * x_min, visual_multiplier * x_max)
plt.ylim(visual_multiplier * y_min, visual_multiplier * y_max)
plt.show()
