import data_visualisation
#https://stackoverflow.com/questions/13491676/get-all-pixel-coordinates-between-2-points
def slope(a, b):
    if a[0] == b[0]:
        return None  # vertical line
    return (b[1] - a[1]) / (b[0] - a[0])

def intercept(point, m):
    if m is None:
        return point[0]  # vertical line
    return point[1] - m * point[0]

# We expect SingleRayDistanceAndColor to take of bounding the points for us.
def calculate_points_2(p1, p2):
    m = slope(p1, p2)
    b = intercept(p1, m)
    if m is None or b is None:
        return []
    coordinates = []
    for x in range(p1[0], p2[0] + 1):
        y = m * x + b
        coordinates.append([int(x), int(y)])
    return coordinates

def is_point_out_of_bounds(point, height, width):
    x,y = point
    return (x < 0 and y < 0) and (x >= width and y >= height)

def calculate_percentage_discovered(matrix, height, width):
    count = 0
    for row in matrix:
        for value in row:
            if value > 0:
                count += 1
    return count / (height*width)

def save_results(floor_plan):
    data_visualisation.save_heatmap(floor_plan, "heatmap of floorplan")