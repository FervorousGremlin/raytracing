from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSlider
from PyQt5.QtCore import Qt
import sys
import numpy as np
import cv2
from raytracer import trace
from objects import Ray, Sphere, Triangle

WIDTH = 800
HEIGHT = 600
FOV = np.pi / 3


class RaytracerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raytracer")
        self.setGeometry(200, 200, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(WIDTH, HEIGHT)

        self.sphere_center_input = QLineEdit(self)
        self.sphere_center_input.setPlaceholderText("Center: x,y,z")
        self.sphere_radius_input = QLineEdit(self)
        self.sphere_radius_input.setPlaceholderText("Radius")
        self.sphere_color_input = QLineEdit(self)
        self.sphere_color_input.setPlaceholderText("Color: R,G,B")
        self.sphere_reflection_input = QLineEdit(self)
        self.sphere_reflection_input.setPlaceholderText("Reflection")
        self.sphere_transparency_input = QLineEdit(self)
        self.sphere_transparency_input.setPlaceholderText("Transparency")

        self.triangle_vertices_input = QLineEdit(self)
        self.triangle_vertices_input.setPlaceholderText("Vertices: x1,y1,z1,x2,y2,z2,x3,y3,z3")
        self.triangle_color_input = QLineEdit(self)
        self.triangle_color_input.setPlaceholderText("Color: R,G,B")
        self.triangle_reflection_input = QLineEdit(self)
        self.triangle_reflection_input.setPlaceholderText("Reflection")
        self.triangle_transparency_input = QLineEdit(self)
        self.triangle_transparency_input.setPlaceholderText("Transparency")

        self.add_sphere_button = QPushButton("Add Sphere", self)
        self.add_sphere_button.clicked.connect(self.add_sphere)

        self.add_triangle_button = QPushButton("Add Triangle", self)
        self.add_triangle_button.clicked.connect(self.add_triangle)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.image_label)

        sphere_input_layout = QHBoxLayout()
        sphere_input_layout.addWidget(self.sphere_center_input)
        sphere_input_layout.addWidget(self.sphere_radius_input)
        sphere_input_layout.addWidget(self.sphere_color_input)
        sphere_input_layout.addWidget(self.sphere_reflection_input)
        sphere_input_layout.addWidget(self.sphere_transparency_input)
        sphere_input_layout.addWidget(self.add_sphere_button)
        self.main_layout.addLayout(sphere_input_layout)

        triangle_input_layout = QHBoxLayout()
        triangle_input_layout.addWidget(self.triangle_vertices_input)
        triangle_input_layout.addWidget(self.triangle_color_input)
        triangle_input_layout.addWidget(self.triangle_reflection_input)
        triangle_input_layout.addWidget(self.triangle_transparency_input)
        triangle_input_layout.addWidget(self.add_triangle_button)
        self.main_layout.addLayout(triangle_input_layout)

        self.central_widget.setLayout(self.main_layout)
        self.fov_label = QLabel("FOV:", self)
        self.fov_slider = QSlider(Qt.Horizontal, self)
        self.fov_slider.setRange(1, 180)
        self.fov_slider.setValue(60)
        self.fov_slider.setTickInterval(1)
        self.fov_slider.setTickPosition(QSlider.TicksBelow)
        self.fov_slider.valueChanged.connect(self.change_fov)

        self.main_layout.addWidget(self.fov_label)
        self.main_layout.addWidget(self.fov_slider)
        # Render the scene initially
        self.render_scene()

    def change_fov(self, value):
        global FOV
        FOV = np.pi * value / 180.0
        self.render_scene()
    def add_sphere(self):
        center_text = self.sphere_center_input.text()
        radius_text = self.sphere_radius_input.text()
        color_text = self.sphere_color_input.text()
        reflection_text = self.sphere_reflection_input.text()
        transparency_text = self.sphere_transparency_input.text()

        try:
            center = np.array([float(val.strip()) for val in center_text.split(",")])
            radius = float(radius_text)
            color = np.array([int(val.strip()) for val in color_text.split(",")])
            reflection = float(reflection_text)
            transparency = float(transparency_text)

            new_sphere = Sphere(center, radius, color, reflection, transparency)
            spheres.append(new_sphere)

            self.render_scene()
        except ValueError:
            pass

    def add_triangle(self):
        vertices_text = self.triangle_vertices_input.text()
        color_text = self.triangle_color_input.text()
        reflection_text = self.triangle_reflection_input.text()
        transparency_text = self.triangle_transparency_input.text()

        try:
            vertices = np.array([float(val.strip()) for val in vertices_text.split(",")]).reshape((3, 3))
            color = np.array([int(val.strip()) for val in color_text.split(",")])
            reflection = float(reflection_text)
            transparency = float(transparency_text)

            new_triangle = Triangle(vertices, color, reflection, transparency)
            triangles.append(new_triangle)
            self.render_scene()
        except ValueError:
            pass

    def render_scene(self):
        image = np.zeros((HEIGHT, WIDTH, 3))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                ray_direction = np.array([
                    (2 * ((x + 0.5) / WIDTH) - 1) * np.tan(FOV / 2) * WIDTH / HEIGHT,
                    (1 - 2 * ((y + 0.5) / HEIGHT)) * np.tan(FOV / 2),
                    -1,
                ])
                ray = Ray(np.array([0, 0, 0]), ray_direction)
                color = trace(ray)
                image[y, x] = color

        image = np.clip(image, 0, 255).astype(np.uint8)
        h, w, ch = image.shape
        q_image = QImage(image.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

