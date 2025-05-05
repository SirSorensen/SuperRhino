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