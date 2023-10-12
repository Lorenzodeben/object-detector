import cv2
import numpy as np




class ObjectDetection:

    def __init__(self):
        self.color_ranges = {
            'RED': ((0, 100, 100), (10, 255, 255)),
            'GREEN': ((30, 50, 50), (70, 255, 255)),
            'BLUE': ((90, 50, 50), (130, 255, 255)),
            'YELLOW': ((20, 100, 100), (40, 255, 255)),
        }
        
        self.pixel_x = []
        self.pixel_y = []

    def detect_shape(self, contour):
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
        num_sides = len(approx)
        if num_sides == 3:
            return "triangle"
        elif num_sides == 4:
            return "square"
        else:
            return "circle"

    def run(self, colors, shapes):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            masked_frames = {}
            for color_name, color_range in self.color_ranges.items():
                mask = cv2.inRange(hsv_frame, color_range[0], color_range[1])
                masked = cv2.bitwise_and(frame, frame, mask=mask)
                masked_frames[color_name] = masked

            self.objectDetector = 0
            for i in range(len(colors)):
                color = colors[i]
                shape = shapes[i]
                masked_frame = masked_frames[color]
                gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for c in contours:
                    area = cv2.contourArea(c)

                    if area < 900:
                        continue

                    Objectshape = self.detect_shape(c)

                    M = cv2.moments(c)
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Check if the detected object matches the user-defined color and shape
                    if color == color and Objectshape == shape:
                        # Draw a label "User Object" at the centroid of the object
                        cv2.putText(frame, "User Object", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        cv2.circle(frame, (cx,cy),5,(100,100,100),-1)
                        self.pixel_y.append(cx)
                        self.pixel_x.append(cy-240)
                        self.objectDetector += 1

                    else:
                        # Draw a label "Undefined Object" at the centroid of the object
                        cv2.putText(frame, "Undefined Object", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10, 10, 10), 2)

                cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_pixel_x(self):
        return self.pixel_x

    def get_pixel_y(self):
        return self.pixel_y
    
    def get_objectDetector(self):
        return self.objectDetector
    
    def get_pixels(self):
        if self.objectDetector == 3:
            return self.pixel_x[:3], self.pixel_y[:3], self.objectDetector
        
    
