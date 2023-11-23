"""
   boot-sequence.py

   Author: Niroshan Rajadurai (@niroshan)
   Repository: https://www.github.com/g0-ospo/animations
   Date: 2023-11-23

    Description:
        This script is a command-line program used to animate a boot sequence. It uses the Pygame library to create the animation.

    Usage:
        python boot-sequence.py

    License:
        This script is released under the MIT License. For more details, see the LICENSE file in the repository.


"""

import pygame
import time
import cv2
import numpy as np

# Initialize pygame
pygame.init()

# Set the dimensions of the window and font attributes
width, height = 3840, 2160  # 4K resolution
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('System Boot')

# Font setup (make sure the 'Press Start 2P Regular' font is installed on your system)
font_name = 'Press Start 2P Regular'
font_color = (0, 255, 0)  # Green color like old terminals
font_size = 40
font = pygame.font.SysFont(font_name, font_size)

# Set the FPS and clock
fps = 30
clock = pygame.time.Clock()

# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID' if mp4v doesn't work
video = cv2.VideoWriter('system_boot.mp4', fourcc, fps, (width, height))

# Boot messages to be displayed
ascii_art = [
    "%%%%%%%%%%%%%%%%%%",
    "%%%%%%%%%%%%%%%%%%%%%%%%%%",
    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
    "%%%%%%%%%    %%%%%%%%%%%%%%%%%%    %%%%%%%%%",
    "%%%%%%%%%%                          %%%%%%%%%%",
    "%%%%%%%%%%%                          %%%%%%%%%%%",
    "%%%%%%%%%%%%                          %%%%%%%%%%%",
    "%%%%%%%%%%%                             %%%%%%%%%%",
    "%%%%%%%%%%%                              %%%%%%%%%%",
    "%%%%%%%%%%%                              %%%%%%%%%%",
    "%%%%%%%%%%%                              %%%%%%%%%%",
    "%%%%%%%%%%%                              %%%%%%%%%%",
    "%%%%%%%%%%%                             %%%%%%%%%%%",
    "%%%%%%%%%%%%                          %%%%%%%%%%%",
    "%%%%%%%%%%%%%                      %%%%%%%%%%%%%",
    "%%%%%%%%%%%%%%%%%              %%%%%%%%%%%%%%%%%%",
    "%%%%%%% %%%%%%%%%%         %%%%%%%%%%%%%%%%%%",
    "%%%%%% %%%%%%%%%          %%%%%%%%%%%%%%%%",
    "%%%%%%  %%%%%             %%%%%%%%%%%%%%",
    "%%%%%%%%    %            %%%%%%%%%%%%%",
    "%%%%%%%%%%%            %%%%%%%%%%%",
    "%%%%%%%%            %%%%%%%%",
    "%%%%%            %%%%%",
]

# calculate the width of the screen in characters
screen_width = int(width / (font_size * 0.6) / 2)

# Calculate the necessary padding for each line to be centered
centered_ascii_art = [
    line.center(screen_width) for line in ascii_art
]

boot_messages = [
    "",
    "",
    "",
    "",
    "BOOTING...",
    "[OK] INITIALIZING QUANTUM PROCESSORS...",
    "[OK] SYSTEM WIDE DIAGNOSTICS: NOMINAL...",
    "[OK] SECURE BOOT: ENABLED...",
    "[OK] INITIALIZING REAL-TIME KERNEL PATCHING MODULE...",
    "[OK] COMPILING DYNAMIC LINK LIBRARIES...",
    "[OK] VALIDATING DATA INTEGRITY PROTOCOLS...",
    "[OK] SYNCHRONIZING DISTRIBUTED FILE SYSTEM...",
    "[OK] ENGAGING CODE VERIFICATION ENGINES...",
    "[OK] ALIGNING SATELLITE NETWORK CONNECTIONS...",
    "[OK] CONFIGURING SYSTEM FOR ANONYMOUS OPERATIONS...",
    "[OK] ACTIVATING QUANTUM ENCRYPTION ALGORITHMS...",
    "[OK] PERFORMING MULTI-FACTOR AUTHENTICATION...",
    "[OK] HARDENING KERNEL AGAINST INTRUSIONS...",
    "[OK] ESTABLISHING SECURE COMMUNICATION CHANNELS...",
    "[OK] PERFORMING AUTONOMOUS SYSTEM CALIBRATION...",
    "[OK] INITIATING PROTOCOL 47-C FOR NETWORK SECURITY...",
    "[OK] FINALIZING SELF-HEALING FRAMEWORK INTEGRATION...",
    "[OK] OPTIMIZING SYSTEM PERFORMANCE PARAMETERS...",
    "SYSTEM BOOT COMPLETE.",
    "",
    "GITHUB ADVANCED SECURITY INITIALIZATION SEQUENCE...",
    "[OK] STARTING SECURITY VULNERABILITY ASSESSMENT...",
    "[OK] DEPLOYING COUNTERMEASURE STRATEGIES...",
    "[OK] LAUNCHING DECISION SUPPORT SYSTEM...",
    "[OK] LAUNCHING SEMANTIC ANALYSIS ENGINE - CODEQL...",
    "[OK] INITIALIZING SUPPLY CHAIN ENGINE - DEPENDABOT...",
    "[OK] STARTING TOKEN SCANNING FRAMEWORK - SECRET SCANNER...",
    "GITHUB ADVANCED SECURITY SEQUENCE COMPLETE.",
    "",
    "AI SYSTEM INITIALIZATION SEQUENCE...",
    "[OK] LOADING AI SUBSYSTEMS...",
    "[OK] CHECKING SYSTEM INTEGRITY...",
    "[OK] NEURAL NETWORKS SYNCHRONIZED...",
    "[OK] HYPERVISOR STATUS: SECURE...",
    "[OK] INITIALIZING MACHINE LEARNING MODULES...",
    "[OK] ENCRYPTED DATA LINK ESTABLISHED...",
    "[OK] DEPLOYING ANOMALY DETECTION SYSTEM...",
    "[OK] OPTIMIZING CONVOLUTIONAL NETWORKS...",
    "[OK] SYSTEM INTEGRATION CHECK COMPLETE...",
    "[OK] INITIATING ADVANCED ALGORITHMIC CORE...",
    "[OK] INTEGRATING ADVANCED PREDICTIVE MODELS...",
    "[OK] AI PLATFORM STATUS: FULLY OPERATIONAL...",
    "AI NEURAL ENGINE INITIALIZATION SEQUENCE COMPLETE.",
    "",
    "WELCOME TO GITHUB ADVANCED SECURITY ARTIFICIAL INTELLIGENCE PLATFORM",
    "",
    "READY TO PERFORM SECURITY ANALYSIS AND CODE OPTIMIZATION...",
    ""
]

combined_messages = centered_ascii_art + boot_messages


# Function to draw text on the screen
def draw_text(messages, y_start):
    y_offset = 0
    for message in messages:
        label = font.render(message, True, font_color)
        window.blit(label, (100, y_start + y_offset))
        y_offset += font_size + 10  # Spacing between lines

# Main loop
running = True
message_index = 0
message_interval = 0.4  # New message every 0.2 seconds
next_message_time = time.time() + message_interval
displayed_messages = []

frame_count = 0  # Track the number of frames
print(f"Rendering {len(combined_messages)} boot messages... (this may take a while)")
video_duration = int(float(message_interval) * float(len(combined_messages)))   # Total duration of the video + 2 seconds
#max_frames = fps * video_duration  # Total number of frames to render
max_frames = 300

max_lines = int(height / (font_size + 10))  # Maximum number of lines to display

if max_lines > 2:
    max_lines -= 2  # Leave room for the "BOOTING..." and "SYSTEM BOOT COMPLETE." messages

while running and frame_count < max_frames:
    current_time = time.time()
    window.fill((0, 0, 0))  # Fill the screen with black

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if it's time to add a new boot message
    if current_time >= next_message_time and message_index < len(combined_messages):
        displayed_messages.append(combined_messages[message_index])
        message_index += 1
        next_message_time = current_time + message_interval

        if len(displayed_messages) > max_lines:
            displayed_messages.pop(0)  # Remove the oldest message

    # Draw the accumulated boot messages
    draw_text(displayed_messages, 100)

    # Update the display
    pygame.display.flip()

    # Capture the current frame
    frame = pygame.surfarray.array3d(window)
    frame = frame.transpose([1, 0, 2])
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)

    print(f"Frame {frame_count} of {max_frames}")
    # Increment frame count
    frame_count += 1

    # Run at specified FPS
    clock.tick(fps)


# Release the video writer and quit pygame
video.release()
pygame.quit()