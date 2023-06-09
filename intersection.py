import numpy as np

# Ray-sphere intersection
def intersect_sphere(ray, sphere):
    oc = ray.origin - sphere.center
    a = np.dot(ray.direction, ray.direction)
    b = 2.0 * np.dot(oc, ray.direction)
    c = np.dot(oc, oc) - sphere.radius * sphere.radius
    discriminant = b * b - 4 * a * c

    if discriminant >= 0:
        t = (-b - np.sqrt(discriminant)) / (2.0 * a)
        if t > 0:
            return t

    return np.inf

# Ray-triangle intersection
def intersect_triangle(ray, triangle):
    v0, v1, v2 = triangle.vertices
    edge1 = v1 - v0
    edge2 = v2 - v0
    pvec = np.cross(ray.direction, edge2)
    det = np.dot(edge1, pvec)

    if np.abs(det) < 1e-8:
        return np.inf

    inv_det = 1.0 / det
    tvec = ray.origin - v0
    u = np.dot(tvec, pvec) * inv_det

    if u < 0 or u > 1:
        return np.inf

    qvec = np.cross(tvec, edge1)
    v = np.dot(ray.direction, qvec) * inv_det

    if v < 0 or u + v > 1:
        return np.inf

    t = np.dot(edge2, qvec) * inv_det
    return t
