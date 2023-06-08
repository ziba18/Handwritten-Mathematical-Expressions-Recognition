import math


def calculate_degree_difference(edge1, edge2):
    def calculate_slope(edge):
        x = edge[0][0]
        y = edge[0][1]
        x_prime = edge[1][0]
        y_prime = edge[1][1]
        if x == x_prime:
            return float('inf')
        else:
            return (y_prime - y) / (x_prime - x)

    slope1 = calculate_slope(edge1)
    if slope1 == float('inf'):
        degree1 = 90.0  # Define the angle for vertical lines (e.g., 90 degrees)
    else:
        angle1 = math.atan(slope1)
        degree1 = math.degrees(angle1)

    slope2 = calculate_slope(edge2)
    if slope2 == float('inf'):
        degree2 = 90.0  # Define the angle for vertical lines (e.g., 90 degrees)
    else:
        angle2 = math.atan(slope2)
        degree2 = math.degrees(angle2)

    degree_diff = abs(degree1 - degree2)
    if degree_diff > 180:
        degree_diff = 360 - degree_diff

    return degree_diff
