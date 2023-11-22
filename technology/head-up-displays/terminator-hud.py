import cv2
import numpy as np
import sys
import time

# Initialize parameters
battery_level = 100
start_time = time.time()


# Function to perform template matching and draw a crosshair
def track_object_and_draw_crosshair(frame, template):
    print("enter")
    template_height, template_width = template.shape[:2]

    print(f"Template width: {template_width}, height: {template_height}")

    # Match template
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print(f"Max value: {max_val}, max location: {max_loc}")

    # Determine the bounding box of the template on the frame
    top_left = max_loc
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    print(f"Top left: {top_left}, bottom right: {bottom_right}")

    # Calculate the center of the bounding box
    center_x, center_y = top_left[0] + template_width // 2, top_left[1] + template_height // 2

    # Draw the crosshair at the center
    cv2.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), (0, 0, 255), 2)
    cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), (0, 0, 255), 2)

    print("exit")
    return frame, (center_x, center_y)

# Function to draw the widgets
def draw_widgets(frame, frame_count, fps):
    global battery_level, start_time
    h, w = frame.shape[:2]

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_thickness = 4  # Increase the thickness for bold text
    font_color = (255, 255, 255)  # Blood red color

    # Starting Y position
    startY = 40
    line_spacing = 10  # Spacing between lines

    # Update and draw battery level
    if frame_count % 150 == 0 and battery_level > 0:
        battery_level -= 1
    battery_text = f'Battery: {battery_level}%'
    (label_width, label_height), baseline = cv2.getTextSize(battery_text, font, font_scale, font_thickness)
    cv2.putText(frame, battery_text, (w - label_width - 10, startY + label_height), font, font_scale, font_color, font_thickness)

    # Update Y position for the next text
    startY += label_height + line_spacing

    # Calculate and draw time online
    time_online = time.time() - start_time
    time_online_hours = int(time_online // 3600)
    time_online_minutes = int((time_online % 3600) // 60)
    time_online_seconds = int(time_online % 60)
    time_online_milliseconds = int((time_online % 1) * 1000)
    time_online_text = f'Time Online: {time_online_hours:02d}:{time_online_minutes:02d}:{time_online_seconds:02d}.{time_online_milliseconds:03d}'
    (label_width, label_height), baseline = cv2.getTextSize(time_online_text, font, font_scale, font_thickness)
    cv2.putText(frame, time_online_text, (w - label_width - 10, startY + label_height), font, font_scale, font_color, font_thickness)

    # Update Y position for the next text
    startY += label_height + line_spacing

    # Update and draw language
    language_text = 'Language: Python' if frame_count >= 90 else 'Language: Detecting...'
    (label_width, label_height), baseline = cv2.getTextSize(language_text, font, font_scale, font_thickness)
    cv2.putText(frame, language_text, (w - label_width - 10, startY + label_height), font, font_scale, font_color, font_thickness)

    # Update Y position for the next text
    startY += label_height + line_spacing

    # Update and draw mode
    if frame_count < 90:
        dot_count = (frame_count // 30) % 4  # Cycle through 0 to 3
        mode_text = 'Mode: Initializing' + '.' * dot_count
    elif frame_count < 150:
        mode_text = 'Mode: System Ready'
    else:
        mode_text = 'Mode: Vulnerability Hunting'
    (label_width, label_height), baseline = cv2.getTextSize(mode_text, font, font_scale, font_thickness)
    cv2.putText(frame, mode_text, (w - label_width - 10, startY + label_height), font, font_scale, font_color, font_thickness)

    return frame

def increase_contrast(frame, clip_limit=2.0, tile_grid_size=(8, 8)):
    # Convert to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
    
    # Split the LAB image to different channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    cl = clahe.apply(l)
    
    # Merge the CLAHE enhanced L-channel with the a and b channels
    limg = cv2.merge((cl, a, b))
    
    # Convert image from LAB color model back to RGB
    enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
    
    return enhanced_frame

if __name__ == '__main__':

    # Check for command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py video_file template_image")
        sys.exit(1)

    video_file = sys.argv[1]
    template_image_file = sys.argv[2]

    # Load the template image
    template = cv2.imread(template_image_file, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Error: Could not load template image '{template_image_file}'")
        sys.exit(1)

    # Load the video
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"Error: Could not open video '{video_file}'")
        sys.exit(1)

    # Prepare to write the output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        print(f"Frame width: {frame.shape[1]}, height: {frame.shape[0]}")
        # print frame number
        print(f"Frame number: {cap.get(1)}, total frames: {cap.get(7)}, fps: {cap.get(5)}, duration: {cap.get(7) / cap.get(5)}")
        if not ret:
            break

        # Track object and draw the crosshair
        tracked_frame, position = track_object_and_draw_crosshair(frame, template)

        red_tinge = np.full_like(frame, (0, 0, 255), dtype=np.uint8)
        tracked_frame = cv2.addWeighted(tracked_frame, 0.7, red_tinge, 0.3, 0)

        # Increase the contrast of the frame
        tracked_frame = increase_contrast(tracked_frame, clip_limit=10.0, tile_grid_size=(8, 8))

        # Draw widgets on the frame
        fps = cap.get(cv2.CAP_PROP_FPS) # Get the frames per second of the video
        widgets_frame = draw_widgets(tracked_frame, frame_count, fps)

        # Write the frame into the output file
        out.write(widgets_frame)

        # Display the resulting frame with a resulo of 
        widgets_frame = cv2.resize(widgets_frame, (1280, 720))
        cv2.imshow('Object Tracking', widgets_frame)

        frame_count += 1

        print("Press 'q' to quit")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("Bottom of loop")

    # Release everything when the job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
