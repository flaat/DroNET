import numpy as np

def compute_circle_path(radius: int, center: tuple) -> list:
    """ compute a set of finite coordinates to simulate a circle trajectory of input radius around a given center

        radius : int -> the radius of the trajectory
        centers : tuple (x, y) the center of the trajectory
        return a list of tuple (coordinates)
    """
    x = list(range(-radius, radius))
    coords = []
    for x_ in x:
        y_ = radius ** 2 - (x_) ** 2
        coords.append((x_, (y_ ** (0.5))))
    coords2 = coords[::-1]
    coords2 = [(x, -y) for x, y in coords2]
    coords += coords2
    return [(x + center[0], y + center[1]) for x, y in coords]

def euclidean_distance(p1, p2)-> float:
    """ Given points p1, p2 in R^2 it returns the norm of the vector connecting them.
    @param p1: starting point
    @param p2: end point
    """
    dist = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    return dist

def angle_between_points(p1, p2, p3)-> float:
    """
        Given 3 points it returns the angle between line1(p1,p2) and line2(p1,p3)
    @param p1: Origin point
    @param p2: Second point
    @param p3: Third point
    @return: angle between 3 points
    """
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p1) - np.array(p3)
    return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def projection_on_line_between_points(p1, p2, p3)-> float:
    """
        Given 3 points ...
    @param p1: origin point
    @param p2: second point
    @param p3: third point
    @return:
    """
    # p1=d_0, p2=D, p3=d_i
    return euclidean_distance(p1, p3) * np.cos(angle_between_points(p1, p2, p3))