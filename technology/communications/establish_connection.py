"""

establish_connection.py

Author: Niroshan Rajadurai (@niroshan)
Repository: https://github.com/g0-ospo/animations

Description: 
    This script is a command-line program used to animate the establishment of a connection. It uses the Pygame library to create the animation.

Usage:
    python establish_connection.py

License:
    This script is released under the MIT License. For more details, see the LICENSE file in the repository.


"""

import pygame
import cv2
import numpy as np

# Initialize pygame
pygame.init()

# Set the dimensions of the window and font attributes
width, height = 3840, 2160  # 4K resolution
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Program Loading')
font_name = 'Press Start 2P Regular'  # Make sure this font is installed on your system
font_color = (0, 255, 0)  # Green color like old terminals
font_size = 100  # Adjust the size as needed, 40 might be too small for 4K resolution
font = pygame.font.SysFont(font_name, font_size)

# Set the FPS and clock
fps = 30
clock = pygame.time.Clock()

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID' if mp4v doesn't work
video = cv2.VideoWriter('establising_link.mp4', fourcc, float(fps), (width, height))

# Function to draw text on the screen
def draw_text(message, pos, dim_effect=False, alpha_val=255):
    label = font.render(message, True, font_color)
    label.set_alpha(alpha_val)
    label_rect = label.get_rect(center=(pos[0], pos[1]))
    window.blit(label, label_rect)

# Positioning of the text
center_x = width // 2
center_y = height // 2

# Total frames for 5 seconds video
total_frames = fps * 7

# Main loop
frame_count = 0
while frame_count < total_frames:
    # Fill the screen with black
    window.fill((0, 0, 0))

    # Handle quitting the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            frame_count = total_frames

    # Draw the "Program Loading" text
    if frame_count <= fps * 5:
        # draw test left justified and center vertically
        draw_text("> Establishing Link", (1000, center_y))
    else:
        draw_text("> Connection Established", (1250, center_y), dim_effect=True)

    # Calculate the alpha value for the dimming effect
    alpha_val = 255 if (frame_count // (fps // 10)) % 2 == 0 else 0  # 5Hz dim effect

    # Add the dots with dimming effect
    if frame_count >= fps * 0 and frame_count <= fps * 5:
        draw_text(" .", (2000, center_y), dim_effect=True, alpha_val=alpha_val)
    if frame_count >= fps * 1 and frame_count <= fps * 5:
        draw_text(" .", (2070, center_y), dim_effect=True, alpha_val=alpha_val)
    if frame_count >= fps * 2 and frame_count <= fps * 5:
        draw_text(" .", (2140, center_y), dim_effect=True, alpha_val=alpha_val)
    if frame_count >= fps * 3 and frame_count <= fps * 5:
        draw_text(" .", (2210, center_y), dim_effect=True, alpha_val=alpha_val)
    if frame_count >= fps * 4 and frame_count <= fps * 5:
        draw_text(" .", (2280, center_y), dim_effect=True, alpha_val=alpha_val)

    # Update the display
    pygame.display.flip()

    # Capture the current frame
    frame = pygame.surfarray.array3d(window)
    frame = frame.transpose([1, 0, 2])
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)

    # Increment the frame count
    frame_count += 1

    # Run at specified FPS
    clock.tick(fps)

# Release the video writer and quit pygame
video.release()
pygame.quit()
