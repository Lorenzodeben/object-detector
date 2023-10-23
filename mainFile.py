import tkinter as tk
from tkinter import *
from UI_for_object_detection import DrawingApp
from ObjectDetector import ObjectDetector
from Actuate import PickPlace
import DoBotArm as Dbt

if __name__ == "__main__":
    # Initialize GUI
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

    # Get current color, shape, and direction
    objects = app.send_values()
    shapes, colors, directions = zip(*objects)
    print(objects)

  

    # Initialize object detection
    detector = ObjectDetector(objects)

    # Wait for GUI window to be closed
    detected_objects = detector.run()

    # Print the detected object locations
    for index, object in enumerate(detected_objects, start=1):
        print(f"object {index}: {object.shape}, {object.color}, {object.position}")
        


    # Initialize the actuation
    actuation = PickPlace()

    while True:
        

        # #test if the values are collected
        #print ( 'Selected Combinations:', colors, shapes)
        # print ('direction of process follows:', directions)
        homeX = 200
        homeY = 0
        homeZ = 50
        scalar1 = 0.7
        scalar2 = 0.6
        timer = 5

        for object in objects:
            if object == "unload":
                actuation.Homing(homeX,homeY,homeZ)
                actuation.Conveyor(timer)
                detector.run(colors, shapes)

                if detector.objectDetector == 3:
                    pixel_x, pixel_y, ObjectAmmount = detector.get_pixels()
                    print('Pixel values for X coordinates are:', pixel_x,'Pixel values for Y coordinates are:', pixel_y)
                    actuation.Unloading(pixel_x,pixel_y,homeX, scalar2, ObjectAmmount)
                    
                    #Run the code for actuation with these values

                    #The X and Y coordinates are supposed to be 
                    #Filename.defname(pixel_y, pixel_x, direction)
                    #add an end to the running of this code
                

                
            elif object == "load":
            # when shape and color match, and 3 unser defined objects are detected, run           
                detector.run(colors, shapes)

                if detector.objectDetector == 3:
                    pixel_x, pixel_y, ObjectAmmount = detector.get_pixels()
                    print('Pixel values for X coordinates are:', pixel_x,'Pixel values for Y coordinates are:', pixel_y)
                    actuation.Homing(homeX, homeY, homeZ)
                    actuation.Loading(pixel_x,pixel_y, homeX, scalar1, ObjectAmmount)
        


                
                #Run the code for actuation with these values

                #The X and Y coordinates are supposed to be 
                #Filename.defname(pixel_y, pixel_x, direction)
                #add an end to the running of this code
            
