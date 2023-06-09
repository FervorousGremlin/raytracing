import numpy as np
class Sphere:
    def __init__(self, center, radius, color, reflection, transparency):
        self.center = center
        self.radius = radius
        self.color = color
        self.reflection = reflection
        self.transparency = transparency

class Triangle:
    def __init__(self, vertices, color, reflection, transparency):
        self.vertices = vertices
        self.color = color
        self.reflection = reflection
        self.transparency = transparency

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction / np.linalg.norm(direction)