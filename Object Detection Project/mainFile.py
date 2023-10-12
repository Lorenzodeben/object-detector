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
    colors, shapes, directions = zip(*objects)
    

    # Initialize object detection
    detector = ObjectDetector(objects)
    
    # Wait for GUI window to be closed
    object_locations = detector.run()
    print("hallo")

    # Print the detected object locations
    print(object_locations)

    

    # Initialize the actuation
    actuation = PickPlace()

    while True:
        
        homeX = 200
        homeY = 0
        homeZ = 50
        scalar1 = 0.7
        scalar2 = 0.6
        timer = 5

        for obj in objects:
            if obj == "unload":
                actuation.Homing(homeX, homeY, homeZ)
                actuation.Conveyor(timer)
                #detector.run(colors, shapes)

                if detector.objectDetector == 3:
                    pixel_x, pixel_y, object_amount = detector.get_pixels()
                    print('Pixel values for X coordinates are:', pixel_x, 'Pixel values for Y coordinates are:', pixel_y)
                    actuation.Unloading(pixel_x, pixel_y, homeX, scalar2, object_amount)
                    
                    #Voer de code uit voor actuation met behulp van deze waarden

                    #De X- en Y-coördinaten zouden moeten zijn
                    #Filename.defname(pixel_y, pixel_x, direction)
                    #Voeg een einde toe aan het uitvoeren van deze code


            elif obj == "load":
                # wanneer vorm en kleur overeenkomen, en 3 door de gebruiker gedefinieerde objecten worden gedetecteerd, voer uit
                #detector.run(colors, shapes)

                if detector.objectDetector == 3:
                    pixel_x, pixel_y, object_amount = detector.get_pixels()
                    print('Pixel values for X coordinates are:', pixel_x, 'Pixel values for Y coordinates are:', pixel_y)
                    actuation.Homing(homeX, homeY, homeZ)
                    actuation.Loading(pixel_x, pixel_y, homeX, scalar1, object_amount)
                    
                #Voer de code uit voor actuation met behulp van deze waarden

                #De X- en Y-coördinaten zouden moeten zijn
                #Filename.defname(pixel_y, pixel_x, direction)
                #Voeg een einde toe aan het uitvoeren van deze code
