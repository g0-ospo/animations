import pygame
import time
from moviepy.editor import ImageSequenceClip

# Initialize pygame
pygame.init()

# Set the dimensions of the window and font attributes
width, height = 3840, 2160  # 4K resolution
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Scanning Widget')
font_name = 'Press Start 2P Regular'
font_size = 40  # Adjust the size as needed
font = pygame.font.SysFont(font_name, font_size)

# Set the FPS and clock
fps = 60
clock = pygame.time.Clock()

# Function to draw flashing text on the screen
def draw_flashing_text(message, pos, color, frequency, elapsed_time):
    label = font.render(message, True, color)
    label_rect = label.get_rect(center=(pos[0], pos[1]))
    # Calculate alpha based on frequency
    alpha = 255 if (time.time() * frequency) % 2 < 1 else 0
    label.set_alpha(alpha)
    window.blit(label, label_rect)

# Colors
green_color = (0, 255, 0)  # Red color
orange_color = (255, 165, 0)  # Orange color
red_color = (255, 0, 0)  # Red color

# Positioning of the text
center_x = width // 2
center_y = height // 2

# Start the animation
start_time = time.time()

# List to store frames for video output
frames = []

# Main loop for 5 seconds of animation
running = True
while running:
    current_time = time.time() - start_time
    if current_time > 5:
        running = False

    window.fill((0, 0, 0))  # Fill the screen with black

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the flashing texts
    draw_flashing_text("LOADING CODE", (center_x, center_y - 60), orange_color, 2, current_time)
    draw_flashing_text("SCANNING CODE", (center_x, center_y), orange_color, 2, current_time)
    draw_flashing_text("VULNERABILITY DETECTED", (center_x, center_y + 60), red_color, 2, current_time)
    draw_flashing_text("FINDINGFIX", (center_x, center_y + 120), orange_color, 2, current_time)
    draw_flashing_text("VALIDATING FIX", (center_x, center_y + 180), orange_color, 2, current_time)
    draw_flashing_text("FIX CONFIRMED", (center_x, center_y + 240), green_color, 2, current_time)
    draw_flashing_text("CODE SECURE", (center_x, center_y + 300), green_color, 2, current_time)
    draw_flashing_text("READY TO DEPLOY", (center_x, center_y + 360), green_color, 2, current_time)

    # Capture the frame
    pygame.display.flip()
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = frame.transpose([1, 0, 2])
    frames.append(frame)

    # Run at specified FPS
    clock.tick(fps)

# Quit pygame
pygame.quit()

# Create the video file
clip = ImageSequenceClip(frames, fps=fps)
clip.write_videofile("scanning_widget_animation-3.mp4", codec="libx264", fps=fps)
