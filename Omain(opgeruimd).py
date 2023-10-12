import cv2
import numpy
from matplotlib import pyplot


class VisionCamera:


    def empty(self):
        pass


    def __init__(self, threshold1, threshold2, spec_x_0, spec_y_0, spec_x_end, spec_y_end):
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.spec_x_0 = spec_x_0
        self.spec_y_0 = spec_y_0
        self.spec_x_end = spec_x_end
        self.spec_y_end = spec_y_end
        

    def getContours(self, frame,frameContour):
        contours, hierarchy = cv2.findContours(frame[self.spec_y_0:self.spec_y_end,self.spec_x_0:self.spec_x_end],cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            color = "undefined"
            peri = cv2.arcLength(cnt,True) 
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            #print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            area = cv2.contourArea(cnt)
            areamin = cv2.getTrackbarPos("Areamin","Parameters")
            areamax = cv2.getTrackbarPos("Areamax","Parameters")
            
            if area > areamin and area < areamax:
                #print(area)
                cv2.drawContours(frameContour[self.spec_y_0:self.spec_y_end,self.spec_x_0:self.spec_x_end],contours,-1,(255,0,255),4)
                M = cv2.moments(cnt)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                color_center = frameHSV[cy,cx]
                hue_value = color_center[1]
                print(hue_value)
                if  hue_value < 20:
                    color = "Red"
                elif 20 < hue_value < 40:
                    color = "Yellow"
                elif 40 < hue_value < 80:
                    color = "Green"
                elif 80 < hue_value < 131:
                    color = "Blue"
                else:
                    color = "Red"
                        
                #print(color_center)
                cv2.putText(frameContour[self.spec_y_0:self.spec_y_end+60,self.spec_x_0:self.spec_x_end+60], color,(x+w+10,y+50), cv2.FONT_HERSHEY_COMPLEX,.4,(0,255,0),1)
                cv2.circle(frameContour[self.spec_y_0:self.spec_y_end,self.spec_x_0:self.spec_x_end],(cx,cy),3,(255,255,255),-1)

                #cv2.rectangle(frameContour, (x,y),(x+w,y+h),(0,255,0),5) #box around the shape
                cv2.putText(frameContour[self.spec_y_0:self.spec_y_end+60,self.spec_x_0:self.spec_x_end+60], "Area:"+str(int(area)),(x+w+10,y+35), cv2.FONT_HERSHEY_COMPLEX, .4,(0,255,0),1)

                    
                if len(approx) == 3:
                    cv2.putText(frameContour[self.spec_y_0:self.spec_y_end+60,self.spec_x_0:self.spec_x_end+60], "Triangle",(x+w+10,y+20), cv2.FONT_HERSHEY_COMPLEX, .4,(0,255,0),1)
                if len(approx) == 4:
                    cv2.putText(frameContour[self.spec_y_0:self.spec_y_end+60,self.spec_x_0:self.spec_x_end+60], "Rectangle",(x+w+10,y+20), cv2.FONT_HERSHEY_COMPLEX, .4,(0,255,0),1)
                if len(approx) >= 7:
                    cv2.putText(frameContour[self.spec_y_0:self.spec_y_end+60,self.spec_x_0:self.spec_x_end+60], "Circle",(x+w+10,y+20), cv2.FONT_HERSHEY_COMPLEX, .4,(0,255,0),1)

            cv2.namedWindow("preview")
            vc = cv2.VideoCapture(0)
            if vc.isOpened(): # try to get the first frame
                rval, frame = vc.read()
            else:
                rval = False
            while rval:
                #create multiple layers from the frame
                cv2.imshow("preview", frame)
                rval, frame = vc.read()
                frameContour = frame.copy()
                frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                frameCanny = cv2.Canny(frameGray,threshold1,threshold2)
                kernel = numpy.ones((5,5))
                frameDil = cv2.dilate(frameCanny, kernel, iterations=1)
                cv2.imshow("HSV",frameHSV)
                cv2.imshow("Dilated",frameDil)
                cv2.rectangle(frameContour,(spec_x_0,spec_y_0),(spec_x_end,spec_y_end),(255,0,0),3)
                self.getContours(frameDil,frameContour)
                cv2.imshow("Contour",frameContour)


                key = cv2.waitKey(20)





                if key == 27: # exit on ESC
                    break


            vc.release()


            # Interface to set the camera settings
            cv2.namedWindow("Parameters")
            cv2.resizeWindow("Parameters",640,440)
            cv2.createTrackbar("Threshold1","Parameters",255,255,self.empty)
            cv2.createTrackbar("Threshold2","Parameters",195,255,self.empty)
            cv2.createTrackbar("Areamin","Parameters",500,30000,self.empty)
            cv2.createTrackbar("Areamax","Parameters",2920,30000,self.empty)
            cv2.createTrackbar("spec_x(0)","Parameters",276,1048,self.empty)
            cv2.createTrackbar("spec_y(0)","Parameters",87,1048,self.empty)
            cv2.createTrackbar("spec_x(end)","Parameters",458,1048,self.empty)
            cv2.createTrackbar("spec_y(end)","Parameters",299,1048,self.empty)
            cv2.destroyWindow("preview")



##################################################################################################

#set the variables to the interface for the camera
threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")
spec_x_0 = cv2.getTrackbarPos("spec_x(0)","Parameters")
spec_y_0 = cv2.getTrackbarPos("spec_y(0)","Parameters")
spec_x_end = cv2.getTrackbarPos("spec_x(end)","Parameters")
spec_y_end = cv2.getTrackbarPos("spec_y(end)","Parameters")

cam1 = VisionCamera(threshold1, threshold2, spec_x_0, spec_y_0, spec_x_end, spec_y_end)

