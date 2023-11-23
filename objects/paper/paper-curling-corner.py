import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Vector:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def multiply(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

class Point:
    def __init__(self, position):
        self.position = position
        self.velocity = Vector(0, 0, 0)
        self.acceleration = Vector(0, 0, 0)

    def apply_force(self, force):
        self.acceleration = self.acceleration.add(force)

    def update(self, time_step):
        self.velocity = self.velocity.add(self.acceleration.multiply(time_step))
        self.position = self.position.add(self.velocity.multiply(time_step))
        self.acceleration = Vector(0, 0, 0)  # Reset acceleration

def create_paper_grid(width, height, grid_size):
    grid = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            x = (i / grid_size) * width
            y = (j / grid_size) * height
            row.append(Point(Vector(x, y, 0)))
        grid.append(row)
    return grid

def apply_gravitational_force(paper_grid, gravity=-9.81):
    force = Vector(0, gravity, 0)
    for row in paper_grid:
        for point in row:
            point.apply_force(force)

def update_paper_grid(paper_grid, time_step):
    for row in paper_grid:
        for point in row:
            point.update(time_step)

def render_paper(paper_grid):
    # Placeholder for rendering logic
    for row in paper_grid:
        for point in row:
            print(f"Point at {point.position.x}, {point.position.y}, {point.position.z}")

def render_paper_2d(paper_grid):
    plt.clf()
    x = [point.position.x for row in paper_grid for point in row]
    y = [point.position.y for row in paper_grid for point in row]
    plt.scatter(x, y)
    plt.pause(0.05)


def apply_lifting_force(paper_grid, corner_index, lift_strength):
    corner_point = paper_grid[corner_index[0]][corner_index[1]]
    lift_force = Vector(0, lift_strength, 0)
    corner_point.apply_force(lift_force)


def initialize_opengl():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -30)

def render_paper_opengl(paper_grid):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_POINTS)
    for row in paper_grid:
        for point in row:
            glVertex3fv((point.position.x, point.position.y, point.position.z))
    glEnd()
    pygame.display.flip()

def main_loop():
    width, height, grid_size, time_step = 10, 10, 10, 0.1
    paper_grid = create_paper_grid(width, height, grid_size)
    initialize_opengl()
    while True:
        print("Looping")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        apply_gravitational_force(paper_grid)
        apply_lifting_force(paper_grid, (0, grid_size - 1), 50)
        update_paper_grid(paper_grid, time_step)
        render_paper_opengl(paper_grid)


if __name__ == "__main__":
    main_loop()






