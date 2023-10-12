import cv2
import numpy as np

# Define color ranges for filtering
color_ranges = {
    'red': ((0, 100, 100), (10, 255, 255)),
    'green': ((30, 50, 50), (70, 255, 255)),
    'blue': ((90, 50, 50), (130, 255, 255)),
    'yellow': ((20, 100, 100), (40, 255, 255)),
}


# Define shape detection function
def detect_shape(contour):
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
    num_sides = len(approx)
    if num_sides == 3:
        return "triangle"
    elif num_sides == 4:
        return "square"
    else:
        return "circle"

# Access the laptop camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to HSV color space for filtering
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Filter the frame to detect colored objects
    masked_frames = {}
    for color_name, color_range in color_ranges.items():
        mask = cv2.inRange(hsv_frame, color_range[0], color_range[1])
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        masked_frames[color_name] = masked

    # Find contours of colored objects in each masked frame
    for color_name, masked_frame in masked_frames.items():
        gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over the contours
        for c in contours:
            # Calculate area and perimeter of contour
            area = cv2.contourArea(c)

            # Skip small contours
            if area < 900:
                continue

            # Detect shape of contour
            shape = detect_shape(c)

            # Find the centroid of the contour
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Check if object matches user-defined parameters
            if color_name == "red" and shape == "square":
                cv2.putText(frame, "red square", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            elif color_name == "red" and shape == "triangle":
                cv2.putText(frame, "red triangle", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            elif color_name == "red" and shape == "circle":
                cv2.putText(frame, "red circle", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            else:
                cv2.putText(frame, "U.I", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 10, 10), 2)
        # Display the resulting frame
    cv2.imshow('frame', frame)

# Exit if user presses 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
