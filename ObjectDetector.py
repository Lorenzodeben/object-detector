import cv2
import numpy as np

class DetectedObject:
    def __init__(self, shape, position, color = "UNKOWN"):
        self.shape = shape
        self.color = color
        self.position = position

class ObjectDetector:
    def __init__(self, pref_objects):
        self.pref_objects = pref_objects

        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 640, 440)
        cv2.createTrackbar("Threshold1", "Parameters", 255, 255, self.empty)
        cv2.createTrackbar("Threshold2", "Parameters", 255, 255, self.empty)
        cv2.createTrackbar("Areamin", "Parameters", 500, 30000, self.empty)
        cv2.createTrackbar("Areamax", "Parameters", 525, 30000, self.empty)
        cv2.createTrackbar("spec_x(0)", "Parameters", 193, 640, self.empty)
        cv2.createTrackbar("spec_y(0)", "Parameters", 258, 480, self.empty)
        cv2.createTrackbar("spec_x(end)", "Parameters", 378, 640, self.empty)
        cv2.createTrackbar("spec_y(end)", "Parameters", 423, 480, self.empty)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Could not open video capture")

        self.detected_objects = []
        self.object_locations = []
        self.masked_frames = {}

        # Color ranges dictionary
        self.color_ranges = {
            'RED': ((0, 70, 50), (10, 255, 255)),
            'GREEN': ((30, 50, 50), (70, 255, 255)),
            'BLUE': ((90, 50, 50), (130, 255, 255)),
            'YELLOW': ((25, 100, 100), (40, 255, 255)),
        }

    def empty(self, *args):
        pass

    def run(self):

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Copy frame for manipulation
            frame_contour = frame.copy()
            
            # Convert frame to HSV and for color detection
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Convert frame to grayscale for shape detection
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            cv2.imshow("Original Frame", frame)

            self.threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
            self.threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

            self.area_min = cv2.getTrackbarPos("Areamin", "Parameters")
            self.area_max = cv2.getTrackbarPos("Areamax", "Parameters")
            
            self.spec_x_0 = cv2.getTrackbarPos("spec_x(0)", "Parameters")
            self.spec_y_0 = cv2.getTrackbarPos("spec_y(0)", "Parameters")
            self.spec_x_end = cv2.getTrackbarPos("spec_x(end)", "Parameters")
            self.spec_y_end = cv2.getTrackbarPos("spec_y(end)", "Parameters")
            cv2.rectangle(frame_contour, (self.spec_x_0, self.spec_y_0), (self.spec_x_end, self.spec_y_end),
                          (255, 0, 0), 3)
            
            
                        
            frame_canny = cv2.Canny(frame_gray, self.threshold1, self.threshold2)
            #cv2.imshow(color + " Canny", frame_canny)
            kernel = np.ones((5, 5))
            frame_dil = cv2.dilate(frame_canny, kernel, iterations=1)
            self.detect_shape(frame_dil, frame_contour)
            #cv2.imshow(color + " Dilated", frame_dil)
            #self.detect_shape(frame_dil, frame_contour)
            self.detect_color(frame_hsv, frame_contour)


            #self.check_preferred_shapes()

            if cv2.waitKey(1) == 27:
                self.cap.release()
                cv2.destroyAllWindows()
                return self.detected_objects

    def detect_shape(self, frame_dil, frame_contour):
        contours, _ = cv2.findContours(frame_dil[self.spec_y_0:self.spec_y_end, self.spec_x_0:self.spec_x_end], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #self.detected_objects = []  # Clear previous detected objects

        for cnt in contours:
            # Determine lenght of perimeter
            peri = cv2.arcLength(cnt, True)

            # Determine rough shape
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # Determine bounding box
            x, y, w, _ = cv2.boundingRect(approx)

            # Determine shape area
            area = cv2.contourArea(cnt)

            # Determine shape
            if self.area_min < area < self.area_max:
                
                
                M = cv2.moments(cnt)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                
                cv2.circle(frame_contour[self.spec_y_0:self.spec_y_end, self.spec_x_0:self.spec_x_end], (cx, cy),
                           3, (255, 255, 255), -1)
                cv2.putText(frame_contour[self.spec_y_0:self.spec_y_end + 40, self.spec_x_0:self.spec_x_end + 100], "Area:" + str(int(area)),
                            (x + w + 10, y + 35), cv2.FONT_HERSHEY_COMPLEX, .4, (0, 255, 0), 1)
                

                
                if len(approx) == 3:
                    shape = "Triangle"
                elif len(approx) == 4:
                    shape = "Rectangle"
                else:
                    shape = "Circle"
                cv2.putText(frame_contour[self.spec_y_0:self.spec_y_end + 40, self.spec_x_0:self.spec_x_end + 100], shape, (x + w + 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, .4, (0, 255, 0), 1)
                detected_object = DetectedObject(shape, (cx + self.spec_x_0,  cy + self.spec_y_0))
                detected_object.area = area
                detected_object.x = x
                detected_object.y = y
                detected_object.w = w
                self.detected_objects.append(detected_object)

            cv2.drawContours(frame_contour[self.spec_y_0:self.spec_y_end, self.spec_x_0:self.spec_x_end], [cnt], -1, (255, 255, 0), 4)
        # Show contours
        cv2.imshow("Contour", frame_contour)



    def detect_color(self, frame_hsv, frame_contour):
        for color_name, color_range in self.color_ranges.items():
            mask = cv2.inRange(frame_hsv, color_range[0], color_range[1])
            # Apply the mask to the original frame_hsv
            masked = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)
            # Convert the masked frame to grayscale (CV_8UC1)
            masked_gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
            # Store the masked frame for this color
            self.masked_frames[color_name] = masked_gray

            cv2.imshow(color_name + " Masked", masked_gray)

        # Associate detected colors with shapes
        for shape in self.detected_objects:
            # Define area filter
            area_min = cv2.getTrackbarPos("Areamin", "Parameters")
            area_max = cv2.getTrackbarPos("Areamax", "Parameters")
            x, y = shape.position
            for color, mask in self.masked_frames.items():
                pixel_value = mask[y, x]
                if pixel_value != 0:
                    shape.color = color

        if area_min < shape.area < area_max:
            cv2.putText(frame_contour[self.spec_y_0:self.spec_y_end + 140, self.spec_x_0:self.spec_x_end + 200],
                    f"Color: {shape.color}", (shape.x + shape.w + 10, shape.y + 55), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)
        cv2.imshow("Contour", frame_contour)

    # def detect_color(self, frame_hsv, frame_contour):
    #     for color_name, color_range in self.color_ranges.items():
    #         mask = cv2.inRange(frame_hsv, color_range[0], color_range[1])
    #         # Apply the mask to the original frame_hsv
    #         masked = cv2.bitwise_and(frame_hsv, frame_hsv, mask=mask)
    #         # Convert the masked frame to grayscale (CV_8UC1)
    #         masked_gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    #         # Store the masked frame for this color
    #         self.masked_frames[color_name] = masked_gray

    #         cv2.imshow(color_name + " Masked", masked_gray)

    #         # Associate detected colors with shapes
    #         for shape in self.detected_objects:
    #             # Define area filter
    #             area_min = cv2.getTrackbarPos("Areamin", "Parameters")
    #             area_max = cv2.getTrackbarPos("Areamax", "Parameters")
    #             x, y = shape.position
    #             pixel_value = masked_gray[y, x]
    #             #print(pixel_value, color_name)
    #             if pixel_value != 0:
    #                 shape.color = color_name
    #             if area_min < shape.area < area_max:
    #                 cv2.putText(frame_contour[self.spec_y_0:self.spec_y_end + 140, self.spec_x_0:self.spec_x_end + 200],
    #                             f"Color: {shape.color}", (shape.x + shape.w + 10, shape.y + 55), cv2.FONT_HERSHEY_COMPLEX, .4, (0, 255, 0), 1)
    #         cv2.imshow("Contour", frame_contour)

                
                
                    

    def get_color_from_hsv(self, hsv_value):
        for color, (lower_bound, upper_bound) in self.color_ranges.items():
            # Use NumPy element-wise comparison
            if np.all(lower_bound <= hsv_value) and np.all(hsv_value <= upper_bound):
                return color
            else:
                pass

    def check_preferred_shapes(self):
        for detected_obj in self.detected_objects:
            for preferred_obj in self.pref_objects:
                # Check shape and color
                if detected_obj.shape == preferred_obj[0] and detected_obj.color == preferred_obj[1]:
                    # Check shape consistency (uncomment this line if needed)
                    if self.is_shape_consistent(detected_obj.position):
                        # Controleer of de positie al in de lijst staat
                        if detected_obj.position not in self.object_locations:
                            self.object_locations.append(detected_obj.position)


