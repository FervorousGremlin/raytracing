
import numpy as np
from objects import Sphere, Triangle, Ray
from intersection import intersect_sphere, intersect_triangle


# Raytracing algorithm
def trace(ray, depth=0):
    if depth > 3:
        return np.array([255, 255, 255])

    t_min = np.inf
    closest_sphere = None
    closest_triangle = None

    for sphere in spheres:
        t = intersect_sphere(ray, sphere)
        if t < t_min:
            t_min = t
            closest_sphere = sphere

    for triangle in triangles:
        t = intersect_triangle(ray, triangle)
        if t < t_min:
            t_min = t
            closest_sphere = None
            closest_triangle = triangle

    if closest_sphere is None and closest_triangle is None:
        return np.array([255, 255, 255])

    intersection = ray.origin + ray.direction * t_min
    normal = np.zeros(3)

    if closest_sphere:
        normal = intersection - closest_sphere.center
        normal = normal / np.linalg.norm(normal)
        reflection_ray = Ray(
            intersection,
            ray.direction - 2.0 * np.dot(ray.direction, normal) * normal
        )
        reflection_color = trace(reflection_ray, depth + 1)
        transparency_color = np.array([255, 255, 255])
        if closest_sphere.transparency > 0:
            transparency_ray = Ray(intersection, ray.direction)
            transparency_color = trace(transparency_ray, depth + 1)
        reflection_factor = closest_sphere.reflection
        transparency_factor = closest_sphere.transparency
        return (
            closest_sphere.color * (1 - reflection_factor - transparency_factor)
            + reflection_factor * reflection_color
            + transparency_factor * transparency_color
        )

    if closest_triangle:
        normal = np.cross(
            closest_triangle.vertices[1] - closest_triangle.vertices[0],
            closest_triangle.vertices[2] - closest_triangle.vertices[0]
        )
        normal = normal / np.linalg.norm(normal)
        reflection_ray = Ray(
            intersection,
            ray.direction - 2.0 * np.dot(ray.direction, normal) * normal
        )
        reflection_color = trace(reflection_ray, depth + 1)
        transparency_color = np.array([255, 255, 255])
        if closest_triangle.transparency > 0:
            transparency_ray = Ray(intersection, ray.direction)
            transparency_color = trace(transparency_ray, depth + 1)
        reflection_factor = closest_triangle.reflection
        transparency_factor = closest_triangle.transparency
        return (
            closest_triangle.color * (1 - reflection_factor - transparency_factor)
            + reflection_factor * reflection_color
            + transparency_factor * transparency_color
        )

spheres = [
    Sphere(np.array([-1.5, 0, -10]), 1.0, np.array([0, 0, 255]), 0.5, 0.0),
    Sphere(np.array([1.5, 0, -10]), 1.0, np.array([255, 0, 0]), 0.5, 0.0),
    Sphere(np.array([0, 1, -8]), 0.5, np.array([0, 255, 0]), 0.5, 0.5),
]

triangles = [
    Triangle(
        np.array([[-1.5, -1, -8], [-1, 0, -8], [-1, -1, -8]]),
        np.array([0, 0, 255]), 0.5, 0.0
    )
]