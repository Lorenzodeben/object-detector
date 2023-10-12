import DoBotArm as Dbt
import time


class PickPlace:
    z = 50
    item_Height1 = 10
    item_Height2 = -40
    offsett = 25
    offsett2 = 20
    offsett3 = 50

    def Homing(self, homeX, homeY, homeZ):
        self.ctrlDobot = Dbt.DoBotArm("COM5", homeX, homeY, homeZ)

    def Conveyor(self, timer):
        self.ctrlDobot.SetConveyor(enabled = True, speed = 10000)
        time.sleep(timer)
        self.ctrlDobot.SetConveyor(enabled = False, speed = -10000)
        
    def Loading(self, pixel_x, pixel_y, homeX, scalar1, num_items):
        items_x = [x * scalar1 for x in pixel_x]
        items_y = [-y * scalar1 for y in pixel_y]
        print('mm values for X coordinates are:', items_x,'mm values for Y coordinates are:', items_y)

        for i in range(num_items):
            item_x, item_y = homeX - items_x[i] - self.offsett2, (items_y[i] + self.offsett3)
            self.ctrlDobot.moveArmXYZ(item_x, item_y, self.z, wait=True)
            self.ctrlDobot.moveArmXYZ(item_x, item_y, self.item_Height2, wait=True)
            self.ctrlDobot.toggleSuction(True)
            self.ctrlDobot.moveArmXYZ(item_x, item_y, self.z, wait=True)

            place_x, place_y = 200, (i - num_items//2) * 50
            self.ctrlDobot.moveArmXYZ(place_x, place_y, self.z, wait=True)
            self.ctrlDobot.moveArmXYZ(place_x, place_y, self.item_Height1, wait=True)
            self.ctrlDobot.toggleSuction(False)
            self.ctrlDobot.moveArmXYZ(place_x, place_y, self.z, wait=True)
        #conveyor belt to left
        self.ctrlDobot.SetConveyor(enabled = True, speed = -10000)
        time.sleep(5)
        self.ctrlDobot.SetConveyor(enabled = False, speed = -10000)
    
    def Unloading(self, pixel_x, pixel_y, homeX, scalar2, num_items):
        items_x = [x * scalar2 for x in pixel_x]
        items_y = [-y * scalar2 for y in pixel_y]
        print('mm values for X coordinates are:', items_x,'mm values for Y coordinates are:', items_y)
        for i in range(num_items):
            item_x, item_y = homeX - items_x[i] - self.offsett2, (items_y[i] + self.offsett)
            self.ctrlDobot.moveArmXYZ(item_x, item_y, self.z, wait=True)
            self.ctrlDobot.moveArmXYZ(item_x, item_y, self.item_Height1, wait=True)
            self.ctrlDobot.toggleSuction(True)
            self.ctrlDobot.moveArmXYZ(item_x, item_y, self.z, wait=True)

            place_x, place_y = (200 -(i - num_items//2) * 50), -200
            self.ctrlDobot.moveArmXYZ(place_x, place_y, self.z, wait=True)
            self.ctrlDobot.moveArmXYZ(place_x, place_y, self.item_Height2, wait=True)
            self.ctrlDobot.toggleSuction(False)
            self.ctrlDobot.moveArmXYZ(place_x, place_y, self.z, wait=True)

