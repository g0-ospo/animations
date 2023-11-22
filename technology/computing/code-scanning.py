
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
font_size = 35
font = pygame.font.SysFont(font_name, font_size)

# Set the FPS and clock
fps = 30
clock = pygame.time.Clock()


# Initialize the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID' if mp4v doesn't work
video = cv2.VideoWriter('code-output-4.mp4', fourcc, fps, (width, height))

# code_output to be displayed
code_ouput = [
  "userController.js",
  "",
  "001: const pool = require('./dbPool');",
  "002: ",
  "003: exports.getUserByName = (name) => {",
  "004:     let query = 'SELECT * FROM users WHERE name = $1';",
  "005:     return pool.query(query, [name]);",
  "006: };",
  "007: ",
  "008: exports.createUser = (user) => {",
  "009:     let query = 'INSERT INTO users(name, email, account_balance) VALUES ($1, $2, $3)';",
  "010:     return pool.query(query, [user.name, user.email, user.account_balance]);",
  "011: };",
  "",
  "authMiddleware.js",
  "",
  "001: const jwt = require('jsonwebtoken');",
  "002: const secret = process.env.JWT_SECRET;",
  "003: ",
  "004: exports.verifyToken = (req, res, next) => {",
  "005:     let token = req.headers['authorization'];",
  "006:     if (!token) return res.status(403).send({ message: 'No token provided.' });",
  "007: ",
  "008:     jwt.verify(token, secret, (err, decoded) => {",
  "009:         if (err) return res.status(500).send({ message: 'Failed to authenticate token.' });",
  "010:         req.userId = decoded.id;",
  "011:         next();",
  "012:     });",
  "013: };",
  "",
 "server.js",
  "",
  "001: var express = require('express')",
  "002: var bodyParser = require('body-parser')",
  "003: const { Pool } = require('pg')",
  "004: ",
  "005: const pool = new Pool({",
  "006:     user: 'dbuser',",
  "007:     host: 'database.server.com',",
  "008:     database: 'mydb',",
  "009:     password: process.env.POSTGRES_PASSWORD,",
  "010:     port: 3211,",
  "011: })",
  "012: ",
  "013: var app = express()",
  "014: app.use(bodyParser.json())",
  "015: app.use(bodyParser.urlencoded({",
  "016:     extended: true",
  "017: }));",
  "018: ",
  "019: console.log(\"Critical Server Service for Banking Backend\");",
  "020: ",
  "021: app.get(\"/\", function(req, res){",
  "022:     const search = req.query.q",
  "023: ",
  "024:     if (search) {",
  "025:         var squery = \"SELECT * FROM users WHERE name = \\\"\" + search + \"\\\"\"",
  "026:         pool.query(squery, (err, res) => {",
#  "025:         var squery = \"SELECT * FROM users WHERE name = $1\";",
#  "026:         pool.query(squery, [search], (err, result) => {",
  "027:             if (err) {",
  "028:                 return res.status(500).json(err);",
  "029:             }",
  "030:             res.status(200).json(result.rows);",
  "031:         })",
  "032:     } else {",
  "033:         res.status(400).send('No search query provided');",
  "034:     }",
  "035: })",
  "036: ",
  "037: app.listen(8000, function () {",
  "038:     console.log(\"Server running\");",
  "039: });",
  "",
  "envConfig.js",
  "",
  "001: const dotenv = require('dotenv');",
  "002: dotenv.config();",
  "003: ",
  "004: module.exports = {",
  "005:     PORT: process.env.PORT || 8000,",
  "006:     POSTGRES_PASSWORD: process.env.POSTGRES_PASSWORD,",
  "007:     JWT_SECRET: process.env.JWT_SECRET,",
  "008: };",
  ""
]

combined_messages = code_ouput


# Function to draw text on the screen
def draw_text_orig(messages, y_start):
    y_offset = 0
    for message in messages:
        label = font.render(message, True, font_color)
        window.blit(label, (100, y_start + y_offset))
        y_offset += font_size + 10  # Spacing between lines

presence_count = 0
frame_count = 0

def draw_text(lines, start_y):
    global presence_count, frame_count 
    for i, line in enumerate(lines):
        color = (0, 255, 0)

        if frame_count <= 200 and presence_count < 15 and line in [
            "025:         var squery = \"SELECT * FROM users WHERE name = \\\"\" + search + \"\\\"\""
        ]:
            presence_count += 1
        elif frame_count <= 200 and presence_count >= 15 and line in [
                "025:         var squery = \"SELECT * FROM users WHERE name = \\\"\" + search + \"\\\"\"",
                "026:         pool.query(squery, (err, res) => {"
        ]:
            color = (255, 0, 0)
        elif frame_count > 200 and frame_count <= 400:
            if line == "025:         var squery = \"SELECT * FROM users WHERE name = \\\"\" + search + \"\\\"\"":
                line = "025:         var squery = \"SELECT * FROM users WHERE name = $1\";"
                color = (255, 255, 0)
            elif line == "026:         pool.query(squery, (err, res) => {":
                line = "026:         pool.query(squery, [search], (err, result) => {"
                color = (255, 255, 0)
        elif frame_count > 400:
            if line == "025:         var squery = \"SELECT * FROM users WHERE name = \\\"\" + search + \"\\\"\"":
                line = "025:         var squery = \"SELECT * FROM users WHERE name = $1\";"
                color = (0, 255, 0)
            elif line == "026:         pool.query(squery, (err, res) => {":
                line = "026:         pool.query(squery, [search], (err, result) => {"
                color = (0, 255, 0)

        text_surface = font.render(line, True, color)
        window.blit(text_surface, (50, start_y + i * (font_size + 10)))

# Main loop
running = True
message_index = 0
message_interval = 0.2  # New message every 0.2 seconds
next_message_time = time.time() + message_interval
displayed_messages = []

print(f"Rendering {len(combined_messages)} boot messages... (this may take a while)")
video_duration = int(float(message_interval) * float(len(combined_messages)))   # Total duration of the video + 2 seconds
#max_frames = fps * video_duration  # Total number of frames to render
#max_frames = fps * len(combined_messages)  # Total number of frames to render
max_frames = 600

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