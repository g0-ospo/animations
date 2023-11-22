import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants for the window size
WIDTH, HEIGHT = 480, 2160
NUM_NODES = 20
MAX_DEPTH = 5
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
ROTATION_SPEED = 2 * math.pi / 10  # Radians per second
PULSE_SPEED = 5
PULSE_SIZE = 2

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Neural Network ASCII Art Animation")

# Initialize clock and frame rate
clock = pygame.time.Clock()
frame_rate = 30

# Function to generate a 3D-looking node with random depth
def generate_3d_node(max_width, max_height, max_depth):
    return [random.randint(0, max_width), random.randint(0, max_height), random.uniform(1, max_depth)]

NODES = [generate_3d_node(WIDTH, HEIGHT, MAX_DEPTH) for _ in range(NUM_NODES)]

# Establish connections based on the depth of the nodes
CONNECTIONS = []
while len(CONNECTIONS) < NUM_NODES * 2:
    start, end = random.sample(NODES, 2)
    if (start, end) not in CONNECTIONS and (end, start) not in CONNECTIONS:
        CONNECTIONS.append((start, end))

# Initialize pulses along connections
PULSES = []

# Function to rotate a point around the vertical axis
def rotate_y_axis(x, z, angle, center_x):
    s, c = math.sin(angle), math.cos(angle)
    x, z = (x - center_x) * c - z * s, (x - center_x) * s + z * c
    x += center_x
    return x, z

# Function to simulate 3D rotation by adjusting X based on Z (depth)
def transform_to_3d(node, angle):
    x, y, z = node
    new_x, new_z = rotate_y_axis(x, z, angle, CENTER_X)
    # Scaling factor for depth effect (smaller z means larger scale)
    scale = 1 + (MAX_DEPTH - new_z) / MAX_DEPTH
    return new_x, y, new_z, scale

# Function to draw nodes with depth
def draw_nodes(screen, nodes):
    for node in nodes:
        x, y, _, scale = transform_to_3d(node, 0)  # No rotation angle for static drawing
        pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), int(5 * scale))

# Function to draw connections considering depth
def draw_connections(screen, connections):
    for start, end in connections:
        start_x, start_y, _, start_scale = transform_to_3d(start, 0)
        end_x, end_y, _, end_scale = transform_to_3d(end, 0)
        pygame.draw.line(screen, (255, 255, 255), (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(1 * (start_scale + end_scale) / 2))

# Function to draw pulses
def draw_pulses(screen, pulses):
    for pulse in pulses:
        position, scale = pulse['position'], pulse['scale']
        pygame.draw.circle(screen, (255, 0, 0), (int(position[0]), int(position[1])), int(PULSE_SIZE * scale))

# Function to update pulses and create new ones if they reach the end node
def update_pulses(pulses, connections, angle):
    new_pulses = []
    for pulse in pulses:
        start, end, progress = pulse['start'], pulse['end'], pulse['progress'] + PULSE_SPEED
        start_x, start_y, _, start_scale = transform_to_3d(start, angle)
        end_x, end_y, _, end_scale = transform_to_3d(end, angle)

        if progress < 100:
            new_x = start_x + (end_x - start_x) * progress / 100
            new_y = start_y + (end_y - start_y) * progress / 100
            new_scale = start_scale + (end_scale - start_scale) * progress / 100
            new_pulses.append({'start': start, 'end': end, 'progress': progress, 'position': (new_x, new_y), 'scale': new_scale})
        else:
            # Create new pulses when an old one finishes
            next_node = random.choice([node for node in NODES if node != end])
            new_pulses.append({'start': end, 'end': next_node, 'progress': 0, 'position': (end_x, end_y), 'scale': end_scale})
    return new_pulses

# Create initial pulses
for _ in range(NUM_NODES // 2):
    start, end = random.choice(CONNECTIONS)
    PULSES.append({'start': start, 'end': end, 'progress': 0, 'position': start[:2], 'scale': 1})

# Main loop
last_time = time.time()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate rotation based on elapsed time
    current_time = time.time()
    elapsed_time = current_time - last_time
    last_time = current_time
    rotation_angle = ROTATION_SPEED * elapsed_time

    # Update pulses with rotation
    NODES = rotate_y_axis(NODES, rotation_angle)
    CONNECTIONS = rotate_y_axis(CONNECTIONS, rotation_angle)
    PULSES = update_pulses(PULSES, CONNECTIONS, rotation_angle)

    # Drawing
    screen.fill((0, 0, 0))
    draw_connections(screen, CONNECTIONS)
    draw_nodes(screen, NODES)
    draw_pulses(screen, PULSES)
    pygame.display.flip()
    clock.tick(frame_rate)

pygame.quit()
