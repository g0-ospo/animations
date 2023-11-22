import pygame
import random
import math
import cv2
import time

# Initialize Pygame
pygame.init()

# Constants for the window size
WIDTH, HEIGHT = 780, 1500
NUM_NODES = 30
NODES = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_NODES)]

# Create a set of unique connections (no duplicates) ensuring there's a path
CONNECTIONS = []
while len(CONNECTIONS) < NUM_NODES - 1:  # Ensure at least a basic connected network
    start, end = random.sample(NODES, 2)
    if (start, end) not in CONNECTIONS and (end, start) not in CONNECTIONS:
        CONNECTIONS.append((start, end))

# Additional connections to create a more complex network
while len(CONNECTIONS) < NUM_NODES * 2:  # Just an arbitrary number of connections
    start, end = random.sample(NODES, 2)
    if (start, end) not in CONNECTIONS and (end, start) not in CONNECTIONS:
        CONNECTIONS.append((start, end))

# Define pulse characteristics
PULSE_SIZE = 5  # Pulse radius
PULSE_SPEED = 5

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neural Network ASCII Art Animation")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
frame_rate = 30

# Function to draw the nodes
def draw_nodes(screen, nodes):
    node_radius = 10  # Node radius
    node_color = (0, 255, 0)  # Green color
    for node in nodes:
        pygame.draw.circle(screen, node_color, node, node_radius)

# Function to draw the connections
def draw_connections(screen, connections):
    for connection in connections:
        pygame.draw.line(screen, pygame.Color('white'), connection[0], connection[1], 1)

# Function to create a pulse along a connection
def create_pulse(connection):
    start, end = connection
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.hypot(dx, dy)
    steps = int(distance / PULSE_SPEED)
    if steps > 0:
        return {
            'start': start,
            'end': end,
            'position': start,
            'direction': (dx / steps, dy / steps),
            'steps': steps,
            'connection': connection  # Keep track of the connection it's on
        }
    return None

# Initialize pulses along connections
PULSES = [create_pulse(connection) for connection in CONNECTIONS]

# Function to draw pulses
def draw_pulses(screen, pulses):
    pulse_color = (255, 0, 0)  # Red color
    for pulse in pulses:
        pygame.draw.circle(screen, pulse_color, (int(pulse['position'][0]), int(pulse['position'][1])), PULSE_SIZE)

# Function to update pulses
def update_pulses(pulses, connections):
    new_pulses = []
    for pulse in pulses:
        if pulse is not None and pulse['position'] is not None and pulse['direction'] is not None:
            pulse['position'] = (pulse['position'][0] + pulse['direction'][0],
                                pulse['position'][1] + pulse['direction'][1])
        pulse['steps'] -= 1
        if pulse['steps'] <= 0:  # Pulse has reached the end node
            connected_paths = [conn for conn in connections if conn[0] == pulse['end']]
            if connected_paths:  # Ensure there are outgoing connections
                new_conn = random.choice(connected_paths)
                new_pulses.append(create_pulse(new_conn))
        else:
            new_pulses.append(pulse)
    return new_pulses

# Main loop

# Initialize the VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID' if mp4v doesn't work
video = cv2.VideoWriter('neural.mp4', fourcc, frame_rate, (WIDTH, HEIGHT))


running = True
while running:
    # Check for Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check if 20 seconds have passed
    if pygame.time.get_ticks() >= 20000:
        break

    # Update pulses
    PULSES = update_pulses(PULSES, CONNECTIONS)

    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw the connections and nodes
    draw_connections(screen, CONNECTIONS)
    draw_nodes(screen, NODES)
    draw_pulses(screen, PULSES)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(frame_rate)

    # Capture the frame
    # Capture the frame
    frame = pygame.surfarray.array3d(pygame.transform.rotate(pygame.transform.flip(screen, False, True), -90))
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)
    print(pygame.time.get_ticks())


# Release the VideoWriter
video.release()

# Quit Pygame
pygame.quit()
