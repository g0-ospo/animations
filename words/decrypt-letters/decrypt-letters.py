import pygame
import random
import string
import time
import argparse
import imageio
import numpy as np
import os
from PIL import Image
from pygifsicle import optimize

# Initialize pygame
pygame.init()

# Set up the display
frame_rate = 30
width, height = 1080, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Word Animation')


# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0 , 0)
transparent = (0, 0, 0, 0)

# Set up font
#font_size = 90
#font_size = ''
#font_name = 'Press Start 2P Regular'
#font_name = 'MinicomputerHv-Regular'
#font_name =''
#font = ''
#font = pygame.font.Font(None, font_size)

def animate_word(target_word, letters_to_solve, font_name, font_size, width, height):
    running = True


    font = pygame.font.SysFont(font_name, font_size)

    word = [' ']*len(target_word)  # Start with a blank word
    indices = list(range(len(target_word)))  # Indices to animate
    solved_letters = 0
    all_letters = string.ascii_uppercase + string.whitespace + '-' 
    frames = []

    surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a transparent surface

    frames_save_folder = f'crypto-animate-{target_word}-{font_name}-{font_size}-{width}x{height}'
    os.makedirs(frames_save_folder, exist_ok=True)
    # check the directory is empty, if so delete any files in there
    if not os.listdir(frames_save_folder) == []:
        for file in os.listdir(frames_save_folder):
            os.remove(os.path.join(frames_save_folder, file))


    # Main loop
    while running and indices:
        screen.fill(transparent)
        surface.fill(transparent)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Letter animation
        for i in indices:
            if solved_letters < letters_to_solve:
                word[i] = random.choice(all_letters)  # Generate a random ASCII character

        # Render the current state of the word
        rendered_word = ''.join(word)
        text = font.render(rendered_word, False, red)
        surface.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

        screen.blit(surface, (0, 0))
        
        pygame.display.flip()

        # Save the current frame

        # Save the current frame
        rgb_array = pygame.surfarray.array3d(surface)
        alpha_array = pygame.surfarray.array_alpha(surface)
        frame = np.dstack((rgb_array, alpha_array))  # Combine the RGB and alpha channels
        frame = np.flip(frame, 0)  # Flip the y-axis
        frames.append(frame)

        # Check if we should stop animating certain letters
        for i in reversed(indices):
            if word[i] == target_word[i]:  # Stop when the letter matches the target
                indices.remove(i)
                solved_letters += 1
                if solved_letters >= letters_to_solve:
                    break
        
        time.sleep(0.05)  # Controls the speed of the animation

        pygame.image.save(surface, f'{frames_save_folder}/{len(frames):04d}.png')


    # Keep the final word on screen for a short time
    time.sleep(2)
    pygame.quit()

    # Save the animation as a GIF
    #imageio.mimsave(f'crypto-animate-{target_word}-{font_name}-{font_size}-{width}x{height}.gif', frames, fps=30)

    # Get a list of files in the directory
    file_names = os.listdir(frames_save_folder)

    # Prepend the directory name to each file name
    file_paths = [os.path.join(frames_save_folder, file_name) for file_name in file_names]

    # Read the files and save them as a GIF
    #imageio.mimsave(f'crypto-animate-{target_word}-{font_name}-{font_size}-{width}x{height}.gif', [imageio.imread(file_path) for file_path in file_paths], fps=30)


    # Read the files
    images = [Image.open(file_path) for file_path in file_paths]

    # Save the images as a GIF
    images[0].save(
        f'crypto-animate-{target_word}-{font_name}-{font_size}-{width}x{height}.gif',
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / frame_rate),
        disposal=2,
        transparency=0,
        optimize=False
    )

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("word", help="the target word to animate to")
parser.add_argument("letters_to_solve", type=int, help="the number of letters to solve at a time")
parser.add_argument("font_name", help="the name of the font to use")
parser.add_argument("font_size", type=int, help="the size of the font to use")
parser.add_argument("width", type=int, help="the width of the animation")
parser.add_argument("height", type=int, help="the height of the animation")
args = parser.parse_args()


# The target word to animate to
target_word = args.word.upper()
letters_to_solve = args.letters_to_solve
animate_word(target_word, letters_to_solve, font_name=args.font_name, font_size=args.font_size, width=args.width, height=args.height )