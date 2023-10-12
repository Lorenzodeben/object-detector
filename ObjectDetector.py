import cv2
import numpy as np

class DetectedObject:
    def __init__(self, shape, color, position):
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

        # Parameters for shape consistency
        self.max_frames_considered = 10
        self.position_history = []

        # Color ranges dictionary
        self.color_ranges = {
            'RED': ((0, 100, 100), (25, 255, 255)),
            'GREEN': ((30, 50, 50), (70, 255, 255)),
            'BLUE': ((90, 50, 50), (130, 255, 255)),
            'YELLOW': ((25, 100, 100), (40, 255, 255)),
        }

    def empty(self, *args):
        pass

    def run(self):
        frame_counter = 0

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame_contour = frame.copy()
            
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            masked_frames = {}
            for color_name, color_range in self.color_ranges.items():
                mask = cv2.inRange(frame_hsv, color_range[0], color_range[1])
                masked = cv2.bitwise_and(frame, frame, mask=mask)
                masked_frames[color_name] = masked

            frame_gray = cv2.cvtColor(masked_frames[color_name], cv2.COLOR_BGR2GRAY)

            threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
            threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
            frame_canny = cv2.Canny(frame_gray, threshold1, threshold2)
            kernel = np.ones((5, 5))
            frame_dil = cv2.dilate(frame_canny, kernel, iterations=1)

            self.spec_x_0 = cv2.getTrackbarPos("spec_x(0)", "Parameters")
            self.spec_y_0 = cv2.getTrackbarPos("spec_y(0)", "Parameters")
            self.spec_x_end = cv2.getTrackbarPos("spec_x(end)", "Parameters")
            self.spec_y_end = cv2.getTrackbarPos("spec_y(end)", "Parameters")
            cv2.rectangle(frame_contour, (self.spec_x_0, self.spec_y_0), (self.spec_x_end, self.spec_y_end),
                          (255, 0, 0), 3)

            self.detect_objects(frame_dil, frame_contour, frame_hsv)
            self.check_preferred_shapes()

            cv2.imshow("Contour", frame_contour)

            frame_counter += 1
            if frame_counter >= self.max_frames_considered:
                frame_counter = 0
                self.position_history = []

            if cv2.waitKey(1) == 27:
                self.cap.release()
                object_locations = self.position_history
                cv2.destroyAllWindows()
                return self.detected_objects, self.object_locations

    def detect_objects(self, frame, frame_contour, frame_hsv):
        contours, hierarchy = cv2.findContours(frame[self.spec_y_0:self.spec_y_end,
                                                      self.spec_x_0:self.spec_x_end],
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.detected_objects = []  # Clear previous detected objects

        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            area = cv2.contourArea(cnt)
            area_min = cv2.getTrackbarPos("Areamin", "Parameters")
            area_max = cv2.getTrackbarPos("Areamax", "Parameters")

            if area_min < area < area_max:
                cv2.drawContours(frame_contour[self.spec_y_0:self.spec_y_end,
                                               self.spec_x_0:self.spec_x_end], [cnt], -1, (255, 0, 255), 4)
                M = cv2.moments(cnt)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                color_center = frame_hsv[cy, cx]
                hsv_value = tuple(color_center)
                
                

                color = self.get_color_from_hsv(hsv_value)

                cv2.putText(frame_contour[self.spec_y_0:self.spec_y_end + 40,
                                          self.spec_x_0:self.spec_x_end + 40], color, (x + w + 10, y + 50),
                            cv2.FONT_HERSHEY_COMPLEX, .4, (0, 255, 0), 1)
                cv2.circle(frame_contour[self.spec_y_0:self.spec_y_end, self.spec_x_0:self.spec_x_end], (cx, cy),
                           3, (255, 255, 255), -1)
                cv2.putText(frame_contour[self.spec_y_0:self.spec_y_end + 40,
                                          self.spec_x_0:self.spec_x_end + 100], "Area:" + str(int(area)),
                            (x + w + 10, y + 35), cv2.FONT_HERSHEY_COMPLEX, .4, (0, 255, 0), 1)

                if len(approx) == 3:
                    shape = "Triangle"
                elif len(approx) == 4:
                    shape = "Rectangle"
                else:
                    shape = "Circle"
                cv2.putText(frame_contour[self.spec_y_0:self.spec_y_end+40,self.spec_x_0:self.spec_x_end+100], shape,(x+w+10,y+20), cv2.FONT_HERSHEY_COMPLEX, .4,(0,255,0),1)

                detected_object = DetectedObject(shape, color, (cx + self.spec_x_0,  cy + self.spec_y_0))
                #print(detected_object.shape, detected_object.color, detected_object.position)
                self.detected_objects.append(detected_object)
                print(hsv_value, shape)

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

    def is_shape_consistent(self, position):
        for hist_position in self.position_history:
            if np.linalg.norm(np.array(position) - np.array(hist_position)) > 10:
                return False
        return True

