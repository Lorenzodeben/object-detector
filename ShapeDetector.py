import cv2
import numpy as np

class ObjectDetector:
    def __init__(self):
        self.detected_shapes = []
        self.filter_size = 5

    def get_contours(self, frame_gray, frame_hsv, frame_contour):
        contours, hierarchy = cv2.findContours(frame_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # Trackbar UI values
            filter_size = cv2.getTrackbarPos("Filter Size", "Parameters")

            # Update the filter size if it has changed
            if filter_size != self.filter_size:
                self.filter_size = filter_size

            # Track detected shapes over multiple frames
            self.detected_shapes.append(approx)

            # Apply moving average filter to smooth the detected shapes
            if len(self.detected_shapes) > self.filter_size:
                filtered_shapes = np.mean(self.detected_shapes[-self.filter_size:], axis=0)
                approx = np.asarray(filtered_shapes, dtype=np.int32)

            x, y, w, h = cv2.boundingRect(approx)
            area = cv2.contourArea(cnt)
            areamin = cv2.getTrackbarPos("Areamin", "Parameters")
            areamax = cv2.getTrackbarPos("Areamax", "Parameters")

            if area > areamin and area < areamax:
                cv2.drawContours(frame_contour, [approx], -1, (255, 0, 255), 4)
                M = cv2.moments(cnt)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                color_center = frame_hsv[cy, cx]
                hue_value = color_center[0]

                # Determine color based on hue value
                if hue_value < 5:
                    color = "Red"
                elif hue_value < 33:
                    color = "Yellow"
                elif hue_value < 110:
                    color = "Green"
                elif hue_value < 131:
                    color = "Blue"
                else:
                    color = "Red"

                cv2.putText(frame_contour, color, (x + w + 10, y + 50), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)
                cv2.circle(frame_contour, (cx, cy), 3, (255, 255, 255), -1)
                cv2.putText(frame_contour, "Area:" + str(int(area)), (x + w + 10, y + 35), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)

                if len(approx) == 3:
                    cv2.putText(frame_contour, "Triangle", (x + w + 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)
                if len(approx) == 4:
                    cv2.putText(frame_contour, "Rectangle", (x + w + 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)
                if len(approx) >= 7:
                    cv2.putText(frame_contour, "Circle", (x + w + 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 255, 0), 1)

    def trackbars(self):
        cv2.namedWindow("Parameters")
        cv2.resizeWindow("Parameters", 640, 440)
        cv2.createTrackbar("Threshold1", "Parameters", 255, 255, self.empty)
        cv2.createTrackbar("Threshold2", "Parameters", 255, 255, self.empty)
        cv2.createTrackbar("Areamin", "Parameters", 500, 30000, self.empty)
        cv2.createTrackbar("Areamax", "Parameters", 2200, 30000, self.empty)
        cv2.createTrackbar("Filter Size", "Parameters", 5, 20, self.empty)

    def empty(self, *args):
        pass

    def run(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Failed to open camera")
            return

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture frame")
                break

            frame_contour = frame.copy()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            self.get_contours(frame_gray, frame_hsv, frame_contour)

            cv2.imshow("Contours", frame_contour)

            if cv2.waitKey(1) == 27:  # Exit on ESC
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = ObjectDetector()
    detector.trackbars()
    detector.run()
